'''
Interfaz: tipo dashboard
- Menú principal
    · Explicación del trabajo
        -> Botón: Comenzar análisis - Crear base de datos
- Creación de datos: 
    · opciones 500, 2000 o 10.000 entradas
        -> Formulario desplegable (500, 2000 o 10.000) con botón de creación
        -> Widget de tabla mostrando el principio y el final del df del csv creado
        -> Botón abajo: Continuar - Análisis Exploratorio de los Datos (EDA)
- Página de EDA: 
    · mostrar homogeneización y transformación de datos en numérico
        -> Formulario: elegir columna y mostrar resumen de unidades existentes y unidades objetivo
        -> A continuación: mostrar QLabel con el método usado para transformarlos
        -> Botón: Continuar EDA (pasa a la siguiente pestaña) ç
    · mostrar vacíos, NaN, 0, negativos
        -> Mostrar características de los datos
        -> Formulario: elegir columna y mostrar resumen de errores
        -> A continuación: mostrar QLabel con el método usado para corregirlos
        -> Botón: Continuar EDA (pasa a la siguiente pestaña) 

    ---> NO <---
    · crear y mostrar IMC
        -> Explicación en QLabel
        -> Botón para creación
        -> QTable que muestre peso, altura e IMC
        -> Botón: Continuar análisis - Creación del modelo
    ---><----

- Página de creación del modelo:
    -> Formulario con opciones de modelos: árbol, bosque aleatorio y SVC
    -> Botón: Creación del modelo (pasa al widget que muestra los 3 árboles y una QLabel con explicación)
    · imagen de 3 árboles al azar 
        -> QCanvas
        -> QLabel con explicación del tipo de modelo 
        -> Botón: Continuar análisis - Evaluación del modelo
- Página de evaluación del modelo:
    · matriz de confusión
        -> QCanvas
    · puntuaciones: precisión, recuperación 
        -> QLabel tipo KPI
    · curva ROC-AUC
        -> Gráfica en un QCanvas, QLabel con explicación
    · Si puntuaciones bajas -> Botón: ofrecer podado del bosque -> página alternativa de creación del modelo
- Página de gráficas:
    -> TabWidget con las siguientes pestañas:
    · importancia de las características +  informe
        -> QCanvas para la gráfica, QLabel para el informe
    · densidad de probabilidades + informe
        -> QCanvas para la gráfica, QLabel para el informe
    · dispersión por clase predicha/real + informe
        -> QCanvas para la gráfica, QLabel para el informe
    · ganancias y pérdidas (gain and lift) + informe
        -> QCanvas para la gráfica, QLabel para el informe
'''



'''import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QStackedWidget, QLabel, QTextEdit,
                             QLineEdit, QFormLayout, QTableWidget, QTableWidgetItem, 
                             QScrollArea, QFrame, QHBoxLayout, QToolBar)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

class BarraLateral(QWidget):
    """Barra lateral de navegación"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Título de la barra lateral
        titulo = QLabel('Navegación')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            font-size: 18px;
            font-weight: bold;
        """)
        
        # Botón para volver al menú principal
        btn_inicio = QPushButton('🏠 Menú Principal')
        btn_inicio.clicked.connect(self.parent_window.mostrar_menu_principal)
        
        # Botones de navegación
        btn_opcion1 = QPushButton('📊 Gráficas')
        btn_opcion1.clicked.connect(lambda: self.parent_window.cambiar_contenido('graficas'))
        
        btn_opcion2 = QPushButton('📋 Tablas')
        btn_opcion2.clicked.connect(lambda: self.parent_window.cambiar_contenido('tablas'))
        
        btn_opcion3 = QPushButton('📝 Formularios')
        btn_opcion3.clicked.connect(lambda: self.parent_window.cambiar_contenido('formularios'))
        
        btn_opcion4 = QPushButton('⚙️ Configuración')
        btn_opcion4.clicked.connect(lambda: self.parent_window.cambiar_contenido('configuracion'))
        
        # Estilo para los botones
        estilo_boton = """
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """
        
        btn_inicio.setStyleSheet(estilo_boton + "border-bottom: 2px solid #2c3e50;")
        btn_opcion1.setStyleSheet(estilo_boton)
        btn_opcion2.setStyleSheet(estilo_boton)
        btn_opcion3.setStyleSheet(estilo_boton)
        btn_opcion4.setStyleSheet(estilo_boton)
        
        # Añadir widgets al layout
        layout.addWidget(titulo)
        layout.addWidget(btn_inicio)
        layout.addWidget(btn_opcion1)
        layout.addWidget(btn_opcion2)
        layout.addWidget(btn_opcion3)
        layout.addWidget(btn_opcion4)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #34495e;")
        self.setFixedWidth(250)


class MenuPrincipal(QWidget):
    """Menú principal con opciones"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Título principal
        titulo = QLabel('Bienvenido a la Aplicación')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            margin: 30px;
        """)
        
        subtitulo = QLabel('Selecciona una sección para comenzar')
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            margin-bottom: 40px;
        """)
        
        # Botones del menú principal
        btn_seccion1 = QPushButton('📊 Sección de Gráficas')
        btn_seccion1.clicked.connect(lambda: self.parent_window.entrar_seccion('graficas'))
        
        btn_seccion2 = QPushButton('📋 Sección de Tablas')
        btn_seccion2.clicked.connect(lambda: self.parent_window.entrar_seccion('tablas'))
        
        btn_seccion3 = QPushButton('📝 Sección de Formularios')
        btn_seccion3.clicked.connect(lambda: self.parent_window.entrar_seccion('formularios'))
        
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
        
        btn_seccion1.setStyleSheet(estilo_boton_menu)
        btn_seccion2.setStyleSheet(estilo_boton_menu.replace('#3498db', '#27ae60').replace('#2980b9', '#229954').replace('#21618c', '#1e8449'))
        btn_seccion3.setStyleSheet(estilo_boton_menu.replace('#3498db', '#e67e22').replace('#2980b9', '#d35400').replace('#21618c', '#ba4a00'))
        
        # Añadir widgets al layout
        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addWidget(btn_seccion1, alignment=Qt.AlignCenter)
        layout.addWidget(btn_seccion2, alignment=Qt.AlignCenter)
        layout.addWidget(btn_seccion3, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")


class ContenidoGraficas(QWidget):
    """Contenido de la sección de gráficas"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botón para volver
        btn_volver = QPushButton('← Volver al Menú')
        btn_volver.clicked.connect(self.volver_menu)

        # Crear gráfica
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        ax = self.figure.add_subplot(111)
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        ax.plot(x, y, 'b-o', linewidth=2)
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_title('Gráfica de Ejemplo')
        ax.grid(True, alpha=0.3)

        layout.addWidget(btn_volver)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def volver_menu(self):
        self.parent().parent().mostrar_menu_principal()

class ContenidoTablas(QWidget):
    """Contenido de la sección de tablas"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botón para volver
        btn_volver = QPushButton('← Volver al Menú')
        btn_volver.clicked.connect(self.volver_menu)

        label = QLabel('Visualización de DataFrame')
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        self.tabla = QTableWidget()
        self.cargar_dataframe()

        layout.addWidget(btn_volver)
        layout.addWidget(label)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

    def cargar_dataframe(self):
        df = pd.DataFrame({
            'Nombre': ['Ana', 'Juan', 'María', 'Pedro'],
            'Edad': [25, 30, 28, 35],
            'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla'],
            'Salario': [30000, 45000, 38000, 52000]
        })

        self.tabla.setRowCount(len(df))
        self.tabla.setColumnCount(len(df.columns))
        self.tabla.setHorizontalHeaderLabels(df.columns)

        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                self.tabla.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

        self.tabla.resizeColumnsToContents()

    def volver_menu(self):
        self.parent().parent().mostrar_menu_principal()


class ContenidoFormularios(QWidget):
    """Contenido de la sección de formularios"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botón para volver
        btn_volver = QPushButton('← Volver al Menú')
        btn_volver.clicked.connect(self.volver_menu)

        label = QLabel('Formulario de Cálculo')
        label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")

        form_layout = QFormLayout()
        self.input_num1 = QLineEdit()
        self.input_num2 = QLineEdit()
        form_layout.addRow('Número 1:', self.input_num1)
        form_layout.addRow('Número 2:', self.input_num2)

        btn_ejecutar = QPushButton('Calcular Suma')
        btn_ejecutar.clicked.connect(self.ejecutar_funcion)

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setMaximumHeight(100)

        layout.addWidget(btn_volver)
        layout.addWidget(label)
        layout.addLayout(form_layout)
        layout.addWidget(btn_ejecutar)
        layout.addWidget(QLabel('Resultado:'))
        layout.addWidget(self.resultado)
        layout.addStretch()

        self.setLayout(layout)

    def ejecutar_funcion(self):
        try:
            num1 = float(self.input_num1.text())
            num2 = float(self.input_num2.text())

            resultado = self.mi_funcion(num1, num2)

            self.resultado.setText(f'La suma de {num1} + {num2} = {resultado}')
        except ValueError:
            self.resultado.setText('Error: Por favor ingresa números válidos')

    def mi_funcion(self, a, b):
        return a + b

    def volver_menu(self):
        self.parent().parent().mostrar_menu_principal()


class ContenidoConfiguracion(QWidget):
    """Contenido de la sección de configuración"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('⚙️ Configuración')
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        
        descripcion = QLabel('Aquí puedes ajustar las preferencias de la aplicación.\nUsa la barra lateral para navegar entre secciones.')
        descripcion.setStyleSheet("font-size: 14px; margin: 10px;")
        
        layout.addWidget(titulo)
        layout.addWidget(descripcion)
        layout.addStretch()
        
        self.setLayout(layout)


class VistaPrincipal(QWidget):
    """Vista que contiene la barra lateral y el contenido"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        # Layout horizontal principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear barra lateral
        self.barra_lateral = BarraLateral(self.parent_window)
        
        # Crear área de contenido con StackedWidget
        self.stack_contenido = QStackedWidget()
        self.stack_contenido.setStyleSheet("background-color: white;")
        
        # Crear widgets de contenido
        self.contenido_graficas = ContenidoGraficas()
        self.contenido_tablas = ContenidoTablas()
        self.contenido_formularios = ContenidoFormularios()
        self.contenido_configuracion = ContenidoConfiguracion()
        
        # Añadir contenidos al stack
        self.stack_contenido.addWidget(self.contenido_graficas)
        self.stack_contenido.addWidget(self.contenido_tablas)
        self.stack_contenido.addWidget(self.contenido_formularios)
        self.stack_contenido.addWidget(self.contenido_configuracion)
        
        # Añadir widgets al layout principal
        main_layout.addWidget(self.barra_lateral)
        main_layout.addWidget(self.stack_contenido)
        
        self.setLayout(main_layout)
    
    def cambiar_contenido(self, seccion):
        """Cambia el contenido mostrado según la sección"""
        if seccion == 'graficas':
            self.stack_contenido.setCurrentWidget(self.contenido_graficas)
        elif seccion == 'tablas':
            self.stack_contenido.setCurrentWidget(self.contenido_tablas)
        elif seccion == 'formularios':
            self.stack_contenido.setCurrentWidget(self.contenido_formularios)
        elif seccion == 'configuracion':
            self.stack_contenido.setCurrentWidget(self.contenido_configuracion)


class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Aplicación con Barra Lateral')
        self.setGeometry(100, 100, 1200, 700)
        
        # Stack principal para cambiar entre menú y vista con barra lateral
        self.stack_principal = QStackedWidget()
        self.setCentralWidget(self.stack_principal)
        
        # Crear menú principal
        self.menu_principal = MenuPrincipal(self)
        
        # Crear vista principal (con barra lateral)
        self.vista_principal = VistaPrincipal(self)
        
        # Añadir widgets al stack principal
        self.stack_principal.addWidget(self.menu_principal)
        self.stack_principal.addWidget(self.vista_principal)
        
        # Mostrar menú principal al inicio
        self.stack_principal.setCurrentWidget(self.menu_principal)
    
    def entrar_seccion(self, seccion):
        """Entra en una sección y muestra la barra lateral"""
        self.stack_principal.setCurrentWidget(self.vista_principal)
        self.vista_principal.cambiar_contenido(seccion)
    
    def cambiar_contenido(self, seccion):
        """Cambia el contenido dentro de la vista con barra lateral"""
        self.vista_principal.cambiar_contenido(seccion)
    
    def mostrar_menu_principal(self):
        """Vuelve al menú principal y oculta la barra lateral"""
        self.stack_principal.setCurrentWidget(self.menu_principal)


def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()'''

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QStackedWidget, QLabel,
                             QToolBox, QLineEdit, QFormLayout, QTextEdit,
                             QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

class MenuPrincipal(QWidget):
    """Menú principal con opciones"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Título principal
        titulo = QLabel('Bienvenido a la Aplicación')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            margin: 30px;
        """)
        
        subtitulo = QLabel('Selecciona una sección para comenzar')
        subtitulo.setAlignment(Qt.AlignCenter)
        subtitulo.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            margin-bottom: 40px;
        """)
        
        # Botones del menú principal
        btn_seccion1 = QPushButton('📊 Sección de Gráficas')
        btn_seccion1.clicked.connect(lambda: self.parent_window.entrar_seccion('graficas'))
        
        btn_seccion2 = QPushButton('📋 Sección de Tablas')
        btn_seccion2.clicked.connect(lambda: self.parent_window.entrar_seccion('tablas'))
        
        btn_seccion3 = QPushButton('📝 Sección de Formularios')
        btn_seccion3.clicked.connect(lambda: self.parent_window.entrar_seccion('formularios'))
        
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
        
        btn_seccion1.setStyleSheet(estilo_boton_menu)
        btn_seccion2.setStyleSheet(estilo_boton_menu.replace('#3498db', '#27ae60').replace('#2980b9', '#229954').replace('#21618c', '#1e8449'))
        btn_seccion3.setStyleSheet(estilo_boton_menu.replace('#3498db', '#e67e22').replace('#2980b9', '#d35400').replace('#21618c', '#ba4a00'))
        
        # Añadir widgets al layout
        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addWidget(btn_seccion1, alignment=Qt.AlignCenter)
        layout.addWidget(btn_seccion2, alignment=Qt.AlignCenter)
        layout.addWidget(btn_seccion3, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")

# ==================== WIDGETS DE GRÁFICAS ====================

class GraficaLineas(QWidget):
    """Gráfica de líneas"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('📈 Gráfica de Líneas')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        # Crear gráfica
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        ax = self.figure.add_subplot(111)
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        ax.plot(x, y1, 'b-', label='Seno', linewidth=2)
        ax.plot(x, y2, 'r-', label='Coseno', linewidth=2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Funciones Trigonométricas')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        layout.addWidget(titulo)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class GraficaBarras(QWidget):
    """Gráfica de barras"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('📊 Gráfica de Barras')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        # Crear gráfica
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        ax = self.figure.add_subplot(111)
        categorias = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo']
        valores = [23, 45, 56, 78, 32]
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        ax.bar(categorias, valores, color=colores)
        ax.set_xlabel('Meses')
        ax.set_ylabel('Ventas (miles €)')
        ax.set_title('Ventas Mensuales')
        ax.grid(True, alpha=0.3, axis='y')
        
        layout.addWidget(titulo)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class GraficaDispersion(QWidget):
    """Gráfica de dispersión"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('🔵 Gráfica de Dispersión')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        # Crear gráfica
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        ax = self.figure.add_subplot(111)
        np.random.seed(42)
        x = np.random.randn(100)
        y = 2 * x + np.random.randn(100) * 0.5
        ax.scatter(x, y, c='#3498db', alpha=0.6, s=50)
        ax.set_xlabel('Variable X')
        ax.set_ylabel('Variable Y')
        ax.set_title('Correlación entre Variables')
        ax.grid(True, alpha=0.3)
        
        layout.addWidget(titulo)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


class GraficaPastel(QWidget):
    """Gráfica de pastel"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('🥧 Gráfica de Pastel')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        # Crear gráfica
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        ax = self.figure.add_subplot(111)
        categorias = ['Producto A', 'Producto B', 'Producto C', 'Producto D']
        valores = [30, 25, 20, 25]
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        ax.pie(valores, labels=categorias, colors=colores, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribución de Ventas por Producto')
        
        layout.addWidget(titulo)
        layout.addWidget(self.canvas)
        self.setLayout(layout)


# ==================== WIDGETS DE TABLAS ====================

class TablaEmpleados(QWidget):
    """Tabla de empleados"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('👥 Tabla de Empleados')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        self.tabla = QTableWidget()
        df = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'Nombre': ['Ana García', 'Juan Pérez', 'María López', 'Pedro Sánchez', 'Laura Martín'],
            'Departamento': ['Ventas', 'IT', 'Marketing', 'IT', 'Ventas'],
            'Salario': [35000, 45000, 38000, 52000, 33000],
            'Antigüedad': [3, 5, 2, 8, 1]
        })
        
        self.cargar_dataframe(df)
        
        layout.addWidget(titulo)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
    
    def cargar_dataframe(self, df):
        self.tabla.setRowCount(len(df))
        self.tabla.setColumnCount(len(df.columns))
        self.tabla.setHorizontalHeaderLabels(df.columns)
        
        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                self.tabla.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        
        self.tabla.resizeColumnsToContents()


class TablaVentas(QWidget):
    """Tabla de ventas"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('💰 Tabla de Ventas')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        self.tabla = QTableWidget()
        df = pd.DataFrame({
            'Fecha': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
            'Producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Laptop'],
            'Cantidad': [2, 5, 3, 1, 1],
            'Precio Unit.': [899, 25, 45, 299, 899],
            'Total': [1798, 125, 135, 299, 899]
        })
        
        self.cargar_dataframe(df)
        
        layout.addWidget(titulo)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
    
    def cargar_dataframe(self, df):
        self.tabla.setRowCount(len(df))
        self.tabla.setColumnCount(len(df.columns))
        self.tabla.setHorizontalHeaderLabels(df.columns)
        
        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                self.tabla.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        
        self.tabla.resizeColumnsToContents()


class TablaInventario(QWidget):
    """Tabla de inventario"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('📦 Tabla de Inventario')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        self.tabla = QTableWidget()
        df = pd.DataFrame({
            'Código': ['A001', 'A002', 'A003', 'A004', 'A005'],
            'Producto': ['Laptop Dell', 'Mouse Logitech', 'Teclado Mecánico', 'Monitor LG', 'Webcam HD'],
            'Stock': [15, 45, 23, 8, 32],
            'Precio': [899, 25, 75, 299, 49],
            'Estado': ['Disponible', 'Disponible', 'Disponible', 'Bajo Stock', 'Disponible']
        })
        
        self.cargar_dataframe(df)
        
        layout.addWidget(titulo)
        layout.addWidget(self.tabla)
        self.setLayout(layout)
    
    def cargar_dataframe(self, df):
        self.tabla.setRowCount(len(df))
        self.tabla.setColumnCount(len(df.columns))
        self.tabla.setHorizontalHeaderLabels(df.columns)
        
        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                self.tabla.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
        
        self.tabla.resizeColumnsToContents()


# ==================== WIDGETS DE FORMULARIOS ====================

class FormularioCalculadora(QWidget):
    """Formulario calculadora simple"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('🔢 Calculadora')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        form_layout = QFormLayout()
        self.input_num1 = QLineEdit()
        self.input_num2 = QLineEdit()
        self.combo_operacion = QComboBox()
        self.combo_operacion.addItems(['Suma', 'Resta', 'Multiplicación', 'División'])
        
        form_layout.addRow('Número 1:', self.input_num1)
        form_layout.addRow('Número 2:', self.input_num2)
        form_layout.addRow('Operación:', self.combo_operacion)
        
        btn_calcular = QPushButton('Calcular')
        btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_calcular.clicked.connect(self.calcular)
        
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setMaximumHeight(80)
        
        layout.addWidget(titulo)
        layout.addLayout(form_layout)
        layout.addWidget(btn_calcular)
        layout.addWidget(QLabel('Resultado:'))
        layout.addWidget(self.resultado)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def calcular(self):
        try:
            num1 = float(self.input_num1.text())
            num2 = float(self.input_num2.text())
            operacion = self.combo_operacion.currentText()
            
            if operacion == 'Suma':
                resultado = num1 + num2
            elif operacion == 'Resta':
                resultado = num1 - num2
            elif operacion == 'Multiplicación':
                resultado = num1 * num2
            elif operacion == 'División':
                if num2 == 0:
                    self.resultado.setText('Error: División por cero')
                    return
                resultado = num1 / num2
            
            self.resultado.setText(f'{operacion}: {num1} y {num2} = {resultado:.2f}')
        except ValueError:
            self.resultado.setText('Error: Ingresa números válidos')


class FormularioRegistro(QWidget):
    """Formulario de registro de usuario"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('📝 Registro de Usuario')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        form_layout = QFormLayout()
        self.input_nombre = QLineEdit()
        self.input_email = QLineEdit()
        self.input_telefono = QLineEdit()
        self.combo_departamento = QComboBox()
        self.combo_departamento.addItems(['Ventas', 'IT', 'Marketing', 'Recursos Humanos', 'Finanzas'])
        
        form_layout.addRow('Nombre completo:', self.input_nombre)
        form_layout.addRow('Email:', self.input_email)
        form_layout.addRow('Teléfono:', self.input_telefono)
        form_layout.addRow('Departamento:', self.combo_departamento)
        
        btn_registrar = QPushButton('Registrar Usuario')
        btn_registrar.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        btn_registrar.clicked.connect(self.registrar)
        
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setMaximumHeight(120)
        
        layout.addWidget(titulo)
        layout.addLayout(form_layout)
        layout.addWidget(btn_registrar)
        layout.addWidget(QLabel('Estado del registro:'))
        layout.addWidget(self.resultado)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def registrar(self):
        nombre = self.input_nombre.text()
        email = self.input_email.text()
        telefono = self.input_telefono.text()
        departamento = self.combo_departamento.currentText()
        
        if not nombre or not email or not telefono:
            self.resultado.setText('❌ Error: Todos los campos son obligatorios')
            return
        
        mensaje = f"""✅ Usuario registrado exitosamente:
        
Nombre: {nombre}
Email: {email}
Teléfono: {telefono}
Departamento: {departamento}"""
        
        self.resultado.setText(mensaje)
        
        # Limpiar campos
        self.input_nombre.clear()
        self.input_email.clear()
        self.input_telefono.clear()


class FormularioConversion(QWidget):
    """Formulario de conversión de unidades"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('🔄 Conversor de Unidades')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        form_layout = QFormLayout()
        self.input_valor = QLineEdit()
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(['Temperatura', 'Distancia', 'Peso'])
        self.combo_tipo.currentTextChanged.connect(self.actualizar_unidades)
        
        self.combo_desde = QComboBox()
        self.combo_hasta = QComboBox()
        
        form_layout.addRow('Valor:', self.input_valor)
        form_layout.addRow('Tipo:', self.combo_tipo)
        form_layout.addRow('De:', self.combo_desde)
        form_layout.addRow('A:', self.combo_hasta)
        
        # Inicializar unidades
        self.actualizar_unidades()
        
        btn_convertir = QPushButton('Convertir')
        btn_convertir.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        btn_convertir.clicked.connect(self.convertir)
        
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setMaximumHeight(80)
        
        layout.addWidget(titulo)
        layout.addLayout(form_layout)
        layout.addWidget(btn_convertir)
        layout.addWidget(QLabel('Resultado:'))
        layout.addWidget(self.resultado)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def actualizar_unidades(self):
        self.combo_desde.clear()
        self.combo_hasta.clear()
        
        tipo = self.combo_tipo.currentText()
        
        if tipo == 'Temperatura':
            unidades = ['Celsius', 'Fahrenheit', 'Kelvin']
        elif tipo == 'Distancia':
            unidades = ['Metros', 'Kilómetros', 'Millas', 'Pies']
        elif tipo == 'Peso':
            unidades = ['Kilogramos', 'Gramos', 'Libras', 'Onzas']
        
        self.combo_desde.addItems(unidades)
        self.combo_hasta.addItems(unidades)
    
    def convertir(self):
        try:
            valor = float(self.input_valor.text())
            tipo = self.combo_tipo.currentText()
            desde = self.combo_desde.currentText()
            hasta = self.combo_hasta.currentText()
            
            if tipo == 'Temperatura':
                resultado = self.convertir_temperatura(valor, desde, hasta)
            elif tipo == 'Distancia':
                resultado = self.convertir_distancia(valor, desde, hasta)
            elif tipo == 'Peso':
                resultado = self.convertir_peso(valor, desde, hasta)
            
            self.resultado.setText(f'{valor} {desde} = {resultado:.2f} {hasta}')
        except ValueError:
            self.resultado.setText('Error: Ingresa un valor numérico válido')
    
    def convertir_temperatura(self, valor, desde, hasta):
        # Convertir a Celsius primero
        if desde == 'Fahrenheit':
            celsius = (valor - 32) * 5/9
        elif desde == 'Kelvin':
            celsius = valor - 273.15
        else:
            celsius = valor
        
        # Convertir de Celsius a la unidad deseada
        if hasta == 'Fahrenheit':
            return celsius * 9/5 + 32
        elif hasta == 'Kelvin':
            return celsius + 273.15
        else:
            return celsius
    
    def convertir_distancia(self, valor, desde, hasta):
        # Convertir a metros primero
        if desde == 'Kilómetros':
            metros = valor * 1000
        elif desde == 'Millas':
            metros = valor * 1609.34
        elif desde == 'Pies':
            metros = valor * 0.3048
        else:
            metros = valor
        
        # Convertir de metros a la unidad deseada
        if hasta == 'Kilómetros':
            return metros / 1000
        elif hasta == 'Millas':
            return metros / 1609.34
        elif hasta == 'Pies':
            return metros / 0.3048
        else:
            return metros
    
    def convertir_peso(self, valor, desde, hasta):
        # Convertir a kilogramos primero
        if desde == 'Gramos':
            kg = valor / 1000
        elif desde == 'Libras':
            kg = valor * 0.453592
        elif desde == 'Onzas':
            kg = valor * 0.0283495
        else:
            kg = valor
        
        # Convertir de kilogramos a la unidad deseada
        if hasta == 'Gramos':
            return kg * 1000
        elif hasta == 'Libras':
            return kg / 0.453592
        elif hasta == 'Onzas':
            return kg / 0.0283495
        else:
            return kg


class FormularioEstadisticas(QWidget):
    """Formulario para calcular estadísticas"""
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        titulo = QLabel('📊 Calculadora de Estadísticas')
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        
        instrucciones = QLabel('Ingresa números separados por comas (ej: 5, 10, 15, 20, 25)')
        instrucciones.setStyleSheet("font-size: 12px; color: #7f8c8d; margin: 5px;")
        
        form_layout = QFormLayout()
        self.input_numeros = QLineEdit()
        form_layout.addRow('Números:', self.input_numeros)
        
        btn_calcular = QPushButton('Calcular Estadísticas')
        btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        btn_calcular.clicked.connect(self.calcular_estadisticas)
        
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setMaximumHeight(150)
        
        layout.addWidget(titulo)
        layout.addWidget(instrucciones)
        layout.addLayout(form_layout)
        layout.addWidget(btn_calcular)
        layout.addWidget(QLabel('Resultados:'))
        layout.addWidget(self.resultado)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def calcular_estadisticas(self):
        try:
            texto = self.input_numeros.text()
            numeros = [float(x.strip()) for x in texto.split(',')]
            
            if len(numeros) == 0:
                self.resultado.setText('Error: Ingresa al menos un número')
                return
            
            media = np.mean(numeros)
            mediana = np.median(numeros)
            desviacion = np.std(numeros)
            minimo = np.min(numeros)
            maximo = np.max(numeros)
            
            resultado_texto = f"""📈 Estadísticas calculadas:

Cantidad de números: {len(numeros)}
Media: {media:.2f}
Mediana: {mediana:.2f}
Desviación estándar: {desviacion:.2f}
Mínimo: {minimo:.2f}
Máximo: {maximo:.2f}"""
            
            self.resultado.setText(resultado_texto)
        except ValueError:
            self.resultado.setText('Error: Formato incorrecto. Usa números separados por comas.')


# ==================== TOOLBOX DE NAVEGACIÓN ====================

class ToolBoxNavegacion(QWidget):
    """ToolBox de navegación con múltiples opciones por sección"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Botón para volver al menú principal
        btn_inicio = QPushButton('🏠 Volver al Menú Principal')
        btn_inicio.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        btn_inicio.clicked.connect(self.parent_window.mostrar_menu_principal)
        
        # Crear ToolBox
        self.toolbox = QToolBox()
        estilo_toolbox = """
            QToolBox::tab {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 24px;
                min-height: 100px;
            }
            QToolBox::tab:selected {
                background-color: #3498db;
            }
        """
        self.toolbox.setStyleSheet(estilo_toolbox)
        # Crear widgets para cada sección del toolbox
        self.crear_seccion_graficas()
        self.crear_seccion_tablas()
        self.crear_seccion_formularios()
        
        layout.addWidget(btn_inicio)
        layout.addWidget(self.toolbox)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #34495e;")
        self.setFixedWidth(280)
    
    def crear_seccion_graficas(self):
        """Crea la sección de gráficas en el toolbox"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        btn_lineas = QPushButton('📈 Gráfica de Líneas')
        btn_lineas.clicked.connect(lambda: self.parent_window.cambiar_contenido('grafica_lineas'))
        
        btn_barras = QPushButton('📊 Gráfica de Barras')
        btn_barras.clicked.connect(lambda: self.parent_window.cambiar_contenido('grafica_barras'))
        
        btn_dispersion = QPushButton('🔵 Gráfica de Dispersión')
        btn_dispersion.clicked.connect(lambda: self.parent_window.cambiar_contenido('grafica_dispersion'))
        
        btn_pastel = QPushButton('🥧 Gráfica de Pastel')
        btn_pastel.clicked.connect(lambda: self.parent_window.cambiar_contenido('grafica_pastel'))


        
        estilo_boton = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 12px;
                text-align: center;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """
        
        btn_lineas.setStyleSheet(estilo_boton)
        btn_barras.setStyleSheet(estilo_boton)
        btn_dispersion.setStyleSheet(estilo_boton)
        btn_pastel.setStyleSheet(estilo_boton)
        
        layout.addWidget(btn_lineas)
        layout.addWidget(btn_barras)
        layout.addWidget(btn_dispersion)
        layout.addWidget(btn_pastel)
        
        widget.setLayout(layout)
        widget.setMinimumHeight(400)
        self.toolbox.addItem(widget, "📊 Gráficas")
    
    def crear_seccion_tablas(self):
        """Crea la sección de tablas en el toolbox"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        btn_empleados = QPushButton('👥 Tabla de Empleados')
        btn_empleados.clicked.connect(lambda: self.parent_window.cambiar_contenido('tabla_empleados'))
        
        btn_ventas = QPushButton('💰 Tabla de Ventas')
        btn_ventas.clicked.connect(lambda: self.parent_window.cambiar_contenido('tabla_ventas'))
        
        btn_inventario = QPushButton('📦 Tabla de Inventario')
        btn_inventario.clicked.connect(lambda: self.parent_window.cambiar_contenido('tabla_inventario'))
        
        estilo_boton = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """
        
        btn_empleados.setStyleSheet(estilo_boton)
        btn_ventas.setStyleSheet(estilo_boton)
        btn_inventario.setStyleSheet(estilo_boton)
        
        layout.addWidget(btn_empleados)
        layout.addWidget(btn_ventas)
        layout.addWidget(btn_inventario)
        
        widget.setLayout(layout)
        self.toolbox.addItem(widget, "📋 Tablas")
    
    def crear_seccion_formularios(self):
        """Crea la sección de formularios en el toolbox"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        btn_calculadora = QPushButton('🔢 Calculadora')
        btn_calculadora.clicked.connect(lambda: self.parent_window.cambiar_contenido('formulario_calculadora'))
        
        btn_registro = QPushButton('📝 Registro de Usuario')
        btn_registro.clicked.connect(lambda: self.parent_window.cambiar_contenido('formulario_registro'))
        
        btn_conversion = QPushButton('🔄 Conversor de Unidades')
        btn_conversion.clicked.connect(lambda: self.parent_window.cambiar_contenido('formulario_conversion'))
        
        btn_estadisticas = QPushButton('📊 Calculadora de Estadísticas')
        btn_estadisticas.clicked.connect(lambda: self.parent_window.cambiar_contenido('formulario_estadisticas'))
        
        estilo_boton = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 12px;
                text-align: left;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """
        
        btn_calculadora.setStyleSheet(estilo_boton)
        btn_registro.setStyleSheet(estilo_boton)
        btn_conversion.setStyleSheet(estilo_boton)
        btn_estadisticas.setStyleSheet(estilo_boton)
        
        layout.addWidget(btn_calculadora)
        layout.addWidget(btn_registro)
        layout.addWidget(btn_conversion)
        layout.addWidget(btn_estadisticas)
        
        widget.setLayout(layout)
        self.toolbox.addItem(widget, "📝 Formularios")


# ==================== CLASES PRINCIPALES ====================

class VistaPrincipal(QWidget):
    """Vista que contiene la barra lateral y el contenido"""
    def __init__(self, parent):
        super().__init__()
        self.parent_window = parent
        self.initUI()
    
    def initUI(self):
        # Layout horizontal principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear barra lateral
        self.barra_lateral = ToolBoxNavegacion(self.parent_window)
        
        # Crear área de contenido con StackedWidget
        self.stack_contenido = QStackedWidget()
        self.stack_contenido.setStyleSheet("background-color: white;")
        
        # Crear widgets de contenido
        self.contenido_graficas = QWidget()  # Placeholder
        self.contenido_tablas = QWidget()
        self.contenido_formularios = QWidget()
        self.contenido_configuracion = QWidget()
        
        # Añadir contenidos al stack
        self.stack_contenido.addWidget(self.contenido_graficas)
        self.stack_contenido.addWidget(self.contenido_tablas)
        self.stack_contenido.addWidget(self.contenido_formularios)
        self.stack_contenido.addWidget(self.contenido_configuracion)
        
        # Añadir widgets al layout principal
        main_layout.addWidget(self.barra_lateral)
        main_layout.addWidget(self.stack_contenido)
        
        self.setLayout(main_layout)
    
    def cambiar_contenido(self, seccion):
        """Cambia el contenido mostrado según la sección"""
        if seccion == 'grafica_lineas':
            self.stack_contenido.setCurrentWidget(GraficaLineas())
        elif seccion == 'grafica_barras':
            self.stack_contenido.setCurrentWidget(GraficaBarras())
        elif seccion == 'grafica_dispersion':
            self.stack_contenido.setCurrentWidget(GraficaDispersion())
        elif seccion == 'grafica_pastel':
            self.stack_contenido.setCurrentWidget(GraficaPastel())
        elif seccion == 'tabla_empleados':
            self.stack_contenido.setCurrentWidget(TablaEmpleados())
        elif seccion == 'tabla_ventas':
            self.stack_contenido.setCurrentWidget(TablaVentas())
        elif seccion == 'tabla_inventario':
            self.stack_contenido.setCurrentWidget(TablaInventario())
        elif seccion == 'formulario_calculadora':
            self.stack_contenido.setCurrentWidget(FormularioCalculadora())
        elif seccion == 'formulario_registro':
            self.stack_contenido.setCurrentWidget(FormularioRegistro())
        elif seccion == 'formulario_conversion':
            self.stack_contenido.setCurrentWidget(FormularioConversion())
        elif seccion == 'formulario_estadisticas':
            self.stack_contenido.setCurrentWidget(FormularioEstadisticas())
        else:
            self.stack_contenido.setCurrentWidget(QWidget())

class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación"""
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
        
        # Crear vista principal (con barra lateral)
        self.vista_principal = VistaPrincipal(self)
        
        # Añadir widgets al stack principal
        self.stack_principal.addWidget(self.menu_principal)
        self.stack_principal.addWidget(self.vista_principal)
        
        # Mostrar menú principal al inicio
        self.stack_principal.setCurrentWidget(self.menu_principal)
    
    def entrar_seccion(self, seccion):
        """Entra en una sección y muestra la barra lateral"""
        self.stack_principal.setCurrentWidget(self.vista_principal)
        self.vista_principal.cambiar_contenido(seccion)
    
    def cambiar_contenido(self, seccion):
        """Cambia el contenido dentro de la vista con barra lateral"""
        self.vista_principal.cambiar_contenido(seccion)
    
    def mostrar_menu_principal(self):
        """Vuelve al menú principal y oculta la barra lateral"""
        self.stack_principal.setCurrentWidget(self.menu_principal)


def main():
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()