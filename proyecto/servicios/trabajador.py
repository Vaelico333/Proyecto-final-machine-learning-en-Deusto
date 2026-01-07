from PyQt5.QtCore import QRunnable, pyqtSignal, QObject, pyqtSlot

class SeñalesTrabajador(QObject):
    terminado = pyqtSignal(object)
    error = pyqtSignal(str)

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
            resultado = self.funcion(*self.args, **self.kwargs)
            self.señales.terminado.emit(resultado)
        except Exception as e:
            self.señales.error.emit(str(e))