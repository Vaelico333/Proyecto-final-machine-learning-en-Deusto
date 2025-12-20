import sys
from acciones import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5 import FigureCanvasQT as FigureCanvas
class DataCreationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Opciones de creación de datos
        self.option_label = QLabel("Selecciona el número de entradas:")
        self.option_combo = QComboBox()
        self.option_combo.addItems(["500", "2000", "10000"])
        self.layout.addWidget(self.option_label)
        self.layout.addWidget(self.option_combo)

        # Botón de creación
        self.create_button = QPushButton("Crear Base de Datos")
        self.create_button.clicked.connect(self.create_data)
        self.layout.addWidget(self.create_button)

        # Tabla de visualización
        self.data_table = QTableWidget()
        self.layout.addWidget(self.data_table)

        # Botón de continuación
        self.continue_button = QPushButton("Continuar - Análisis Exploratorio de los Datos (EDA)")
        self.continue_button.clicked.connect(self.go_to_eda)
        self.layout.addWidget(self.continue_button)

    def create_data(self):
        # Lógica para crear el DataFrame y mostrarlo en la tabla
        num_entries = int(self.option_combo.currentText())
        # Generar datos de ejemplo
        data = {'col1': np.random.rand(num_entries),
                'col2': np.random.randint(0, 100, num_entries),
                'col3': np.random.choice(['A', 'B', 'C'], num_entries)}
        df = pd.DataFrame(data)

        # Mostrar el principio y el final del DataFrame
        self.data_table.setRowCount(2)
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(df.columns)

        # Mostrar las primeras filas
        self.data_table.setRow(0, df.head(1))

        # Mostrar las últimas filas
        self.data_table.setRow(1, df.tail(1))

    def go_to_eda(self):
        # Lógica para pasar a la página de EDA
        pass
class EDAPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Vacíos, NaN, 0, Negativos
        self.vacios_label = QLabel("Análisis de Valores Faltantes, NaN, 0 y Negativos")
        self.layout.addWidget(self.vacios_label)

        self.columna_combo = QComboBox()
        self.layout.addWidget(self.columna_combo)

        self.resumen_button = QPushButton("Mostrar Resumen de Errores")
        self.resumen_button.clicked.connect(self.mostrar_resumen)
        self.layout.addWidget(self.resumen_button)

        self.metodo_label = QLabel("")
        self.layout.addWidget(self.metodo_label)

        # Homogeneización y Transformación
        self.homogeneizacion_label = QLabel("Homogeneización y Transformación de Datos Numéricos")
        self.layout.addWidget(self.homogeneizacion_label)

        self.columna_combo_transform = QComboBox()
        self.layout.addWidget(self.columna_combo_transform)

        self.transform_button = QPushButton("Mostrar Resumen de Unidades")
        self.transform_button.clicked.connect(self.mostrar_transformacion)
        self.layout.addWidget(self.transform_button)

        self.transform_metodo_label = QLabel("")
        self.layout.addWidget(self.transform_metodo_label)

        # IMC
        self.imc_label = QLabel("Creación del Índice de Masa Corporal (IMC)")
        self.layout.addWidget(self.imc_label)

        self.imc_button = QPushButton("Crear IMC")
        self.imc_button.clicked.connect(self.crear_imc)
        self.layout.addWidget(self.imc_button)

        self.imc_table = QTableWidget()
        self.layout.addWidget(self.imc_table)

    def mostrar_resumen(self):
        # Lógica para mostrar el resumen de errores de la columna seleccionada
        pass

    def mostrar_transformacion(self):
        # Lógica para mostrar el resumen de la transformación
        pass

    def crear_imc(self):
        # Lógica para crear el IMC y mostrarlo en la tabla
        pass
class ModelCreationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Formulario con opciones de modelos
        self.modelo_combo = QComboBox()
        self.modelo_combo.addItems(["Regresión Lineal", "Árbol de Decisión", "Bosque Aleatorio", "SVM"])
        self.layout.addWidget(self.modelo_combo)

        # Botón de creación
        self.crear_button = QPushButton("Crear Modelo")
        self.crear_button.clicked.connect(self.crear_modelo)
        self.layout.addWidget(self.crear_button)

    def crear_modelo(self):
        # Lógica para crear el modelo seleccionado
        pass
class EvaluationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        # Matriz de confusión
        self.canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.canvas)

        # Puntuaciones
        self.precision_label = QLabel("Precisión: 0.85")
        self.layout.addWidget(self.precision_label)

        # Curva ROC-AUC
        self.roc_canvas = FigureCanvas(plt.figure())
        self.layout.addWidget(self.roc_canvas)

        # Botón de podado del bosque
        self.podar_button = QPushButton("Ofrecer Podado del Bosque")
        self.podar_button.clicked.connect(self.mostrar_podado)
        self.layout.addWidget(self.podar_button)

    def mostrar_podado(self):
        # Lógica para mostrar la página alternativa de creación del modelo
        pass
class GraphPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab_widget = QTabWidget()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tab_widget)

        # Pestaña de Importancia de Características
        self.importancia_tab = QWidget()
        self.importancia_canvas = FigureCanvas(plt.figure())
        self.importancia_layout = QVBoxLayout(self.importancia_tab)
        self.importancia_layout.addWidget(self.importancia_canvas)
        self.tab_widget.addTab(self.importancia_tab, "Importancia de Características")

        # Pestaña de Densidad de Probabilidades
        self.densidad_tab = QWidget()
        self.densidad_canvas = FigureCanvas(plt.figure())
        self.densidad_layout = QVBoxLayout(self.densidad_tab)
        self.densidad_layout.addWidget(self.densidad_canvas)
        self.tab_widget.addTab(self.densidad_tab, "Densidad de Probabilidades")

        # Pestaña de Dispersión por Clase
        self.dispersion_tab = QWidget()
        self.dispersion_canvas = FigureCanvas(plt.figure())
        self.dispersion_layout = QVBoxLayout(self.dispersion_tab)
        self.dispersion_layout.addWidget(self.dispersion_canvas)
        self.tab_widget.addTab(self.dispersion_tab, "Dispersión por Clase")

        # Pestaña de Ganancias y Pérdidas
        self.ganancias_tab = QWidget()
        self.ganancias_canvas = FigureCanvas(plt.figure())
        self.ganancias_layout = QVBoxLayout(self.ganancias_tab)
        self.ganancias_layout.addWidget(self.ganancias_canvas)
        self.tab_widget.addTab(self.ganancias_tab, "Ganancias y Pérdidas")

class MenuPrincipal(QWidget):
    """Menú principal con opciones"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Título principal
        self.EtiquetaTitulo = QLabel('Análisis de datos médicos')
        self.EtiquetaTitulo.setAlignment(Qt.AlignCenter)
        self.EtiquetaTitulo.setGeometry(QRect(165, 50, 850, 100))
        font = QFont()
        font.setFamily(u"Matura MT Script Capitals")
        font.setPointSize(48)
        font.setBold(False)
        font.setWeight(50)
        self.EtiquetaTitulo.setFont(font)
        self.EtiquetaTitulo.setStyleSheet(u"font-size:48pt;"
        "background-color: rgb(0, 255, 255);""")
        self.EtiquetaTitulo.setFrameShape(QFrame.Panel)
        self.EtiquetaTitulo.setFrameShadow(QFrame.Raised)
        self.EtiquetaTitulo.setLineWidth(5)

        subtitulo = QLabel('Curso de Machine Learning de Deusto')
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            margin-bottom: 40px;
        """)

        # Cuadro de texto

        
        # Botón para continuar
        #self.BotonComenzar = QToolButton(self.pagina_1)
        #self.BotonComenzar.setObjectName(u"BotonComenzar")
        #self.BotonComenzar.setGeometry(QRect(400, 650, 400, 50))
        
        # Estilo para los botones del menú principal
        estilo_boton_menu = """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 20px;
                font-size: 18px;
                border-radius: 10px;
                min-width: 400px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """
        
        '''btn_seccion1.setStyleSheet(estilo_boton_menu)
        btn_seccion2.setStyleSheet(estilo_boton_menu.replace('#3498db', '#27ae60').replace('#2980b9', '#229954').replace('#21618c', '#1e8449'))
        btn_seccion3.setStyleSheet(estilo_boton_menu.replace('#3498db', '#e67e22').replace('#2980b9', '#d35400').replace('#21618c', '#ba4a00'))
        '''
        # Añadir widgets al layout
        '''        layout.addStretch()
        layout.addWidget(self.EtiquetaTitulo)
        layout.addWidget(subtitulo)
        layout.addWidget(btn_seccion1, alignment=Qt.AlignCenter)
        layout.addWidget(btn_seccion2, alignment=Qt.AlignCenter)
        layout.addWidget(btn_seccion3, alignment=Qt.AlignCenter)
        layout.addStretch()'''
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
   
class MainWindow(QMainWindow):
    '''    def __init__(self):
        super().__init__()

        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

        self.show()'''
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Aplicación con Barra Lateral')
        self.setGeometry(100, 100, 800, 600)
        
        # Stack principal para cambiar entre menú y vista con barra lateral
        self.stack_principal = QStackedWidget()
        self.setCentralWidget(self.stack_principal)
        
        # Crear menú principal
        self.menu_principal = MenuPrincipal(self)
        self.data_creation = DataCreationPage(self)
        self.eda = EDAPage(self)
        self.model = ModelCreationPage(self)
        self.evaluation = EvaluationPage(self)
        self.graph = GraphPage(self)
        
        # Crear vista principal (con barra lateral)
        #self.vista_principal = VistaPrincipal(self)
        
        # Añadir widgets al stack principal
        self.stack_principal.addWidget(self.menu_principal)
        self.stack_principal.addWidget(self.data_creation)
        self.stack_principal.addWidget(self.eda)
        self.stack_principal.addWidget(self.model)
        self.stack_principal.addWidget(self.evaluation)
        self.stack_principal.addWidget(self.graph)
        #self.stack_principal.addWidget(self.vista_principal)
        
        # Mostrar menú principal al inicio
        self.stack_principal.setCurrentWidget(self.menu_principal)

        # Paleta de colores
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 154, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(0, 231, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(0, 192, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(0, 77, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(0, 103, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush6 = QBrush(QColor(255, 255, 255, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush6)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        brush7 = QBrush(QColor(127, 204, 127, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush7)
        brush8 = QBrush(QColor(255, 255, 220, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush8)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush9 = QBrush(QColor(0, 0, 0, 128))
        brush9.setStyle(Qt.SolidPattern)
        MainWindow.setPalette(self, palette)

    def entrar_seccion(self, seccion):
        """Entra en una sección y muestra la barra lateral"""
        #self.stack_principal.setCurrentWidget(self.vista_principal)
        #self.vista_principal.cambiar_contenido(seccion)
    
    def cambiar_contenido(self, seccion):
        """Cambia el contenido dentro de la vista con barra lateral"""
        #self.vista_principal.cambiar_contenido(seccion)
    
    def mostrar_menu_principal(self):
        """Vuelve al menú principal y oculta la barra lateral"""
        self.stack_principal.setCurrentWidget(self.menu_principal)


def main():
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()