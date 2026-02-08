import sys
import re
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot

class ControlEntrenamiento:
    def __init__(self, iteraciones_iniciales=100):
        self.total_pasos = iteraciones_iniciales

class SeñalesTrabajador(QObject):
    terminado = pyqtSignal(object)
    error = pyqtSignal(str)
    progreso = pyqtSignal(int)

class CapturadorConsola(QObject):
    """Procesa el verbose de Scikit-learn para extraer progreso."""
    progreso_total = pyqtSignal(int)   # Para Barra Global (iteraciones)
    progreso_parcial = pyqtSignal(int)  # Para Barra Parcial (fits/candidatos)
    mensaje_status = pyqtSignal(dict)    # Para QLabel informativo

    def __init__(self):
        super().__init__()
        self.total_etapas = 1
        self.fits_totales_etapa = 0
        self.fits_actuales_etapa = 0
        self.etapa_actual = 0
        self.candidatos = 0
        self.recuento_cv = 1

    def write(self, text):
        # Si no hay texto o es todo espacios, terminamos la función de inmediato
        if not text or text.isspace(): return

        # Extraemos el número de iteraciones totales
        if 'n_iterations:' in text:
            m = re.search(r'n_iterations: (\d+)', text)
            if m:
                max_iter = int(m.group(1))
                self.total_etapas = max_iter

        # Extraemos el número de iteración actual y se lo enviamos a la barra de progreso total
        if "iter:" in text:
            m = re.search(r'iter: (\d+)', text)
            if m:
                self.recuento_cv = 0
                # +1 porque las iteraciones empiezan en 0
                self.etapa_actual = int(m.group(1)) + 1
                prog_t = int((self.etapa_actual / self.total_etapas) * 100)
                self.progreso_total.emit(min(prog_t, 100))
        
        # Contamos el número de candidatos totales y los fits, que serán el número de pasos de nuestra barra parcial
        if "totalling" in text and "fits" in text:
            m = re.search(r'Fitting (\d+) folds for each of (\d+) candidates, totalling (\d+) fits', text)
            if m:
                self.candidatos = int(m.group(2))
                entrenamientos = int(m.group(3))
                self.fits_totales_etapa = entrenamientos
                self.fits_actuales_etapa = 0
                self.progreso_parcial.emit(0)

        # Contamos cuántos candidatos se han analizado (cambiar si se cambian los "folds")
        if "[CV 3/3" in text:
            self.recuento_cv += 1

        # Contamos cada fit finalizado
        conteo_fits = text.count("[CV")
        if conteo_fits > 0:
            self.fits_actuales_etapa += conteo_fits
            if self.fits_totales_etapa > 0:
                prog_p = int((self.fits_actuales_etapa / self.fits_totales_etapa) * 100)
                self.progreso_parcial.emit(min(prog_p, 100))
        
        mensaje = {}
        mensaje['iter'] = self.etapa_actual
        mensaje['cand'] = self.recuento_cv
        mensaje['cand_total'] = self.candidatos
        self.mensaje_status.emit(mensaje)
    
    def flush(self): pass

class Trabajador(QRunnable):
    def __init__(self, funcion, *args, capturador=None, **kwargs):
        super().__init__()
        self.funcion = funcion
        self.args = args
        self.kwargs = kwargs
        self.capturador = capturador        
        self.señales = SeñalesTrabajador()

    @pyqtSlot()
    def run(self):
        import traceback
        stdout_original = sys.stdout
        if self.capturador:
            sys.stdout = self.capturador 
            try:
                resultado = self.funcion(*self.args, **self.kwargs)
                self.señales.terminado.emit(resultado)
            except Exception as e:
                self.señales.error.emit(str(e))
                traceback.print_exc()
            finally:
                sys.stdout = stdout_original
        else:
            try:
                self.kwargs['señal_progreso'] = self.señales.progreso.emit
                resultado = self.funcion(*self.args, **self.kwargs)
                self.señales.terminado.emit(resultado)

            except Exception as e:
                import traceback
                traceback.print_exc() 
                self.señales.error.emit(str(e))

class Decorador():

    def progreso(func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            llamada = kwargs.get('señal_progreso')
            control = kwargs.get('objeto_control')

            def reporte(paso_actual):
                if llamada and control:
                    porcentaje = int((paso_actual / control.total_pasos) * 100)
                    llamada(min(porcentaje, 100))

            kwargs['reporte_progreso'] = reporte
            return func(*args, **kwargs)
        return wrapper
