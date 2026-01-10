from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, pyqtSlot

class ControlEntrenamiento:
    def __init__(self, iteraciones_iniciales=100):
        self.total_pasos = iteraciones_iniciales

class SeñalesTrabajador(QObject):
    terminado = pyqtSignal(object)
    error = pyqtSignal(str)
    progreso = pyqtSignal(int)

class Trabajador(QRunnable):
    def __init__(self, funcion, *args, **kwargs):
        super().__init__()
        self.funcion = funcion
        self.args = args
        self.kwargs = kwargs
        self.señales = SeñalesTrabajador()

    @pyqtSlot()
    def run(self):
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
