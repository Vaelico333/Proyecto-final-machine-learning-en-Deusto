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
        -> Botón: Continuar EDA (pasa a la siguiente pestaña) 
    · mostrar vacíos, NaN, 0, negativos
        -> Mostrar características de los datos
        -> Formulario: elegir columna y mostrar resumen de errores
        -> A continuación: mostrar QLabel con el método usado para corregirlos
        -> Botón: pasar a creación del modelo

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

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from servicios.acciones import *
from servicios.generador_datos import *
from servicios.analisis import *


class PaginaBienvenida(QWidget):
    """Página de bienvenida"""
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()
    
    def init_ui(self):
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setAlignment(Qt.AlignCenter)
        
        # Título
        self.etiqueta_titulo = QLabel("Análisis de datos médicos")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)
        
        # Cuadro de texto 
        self.caja_texto = QLabel(textos.bienvenida())
        self.caja_texto.setWordWrap(True)
        self.caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_texto.setFont(QFont("Noto Serif", 20))
        self.caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        self.area_texto = QScrollArea()
        self.area_texto.setWidgetResizable(True)
        self.area_texto.setWidget(self.caja_texto)
        self.area_texto.setFrameShape(QFrame.Box)
        self.area_texto.setFrameShadow(QFrame.Raised)
        self.area_texto.setLineWidth(4)

        
        # Botón para ir a la página de creación de datos
        self.btn_seguir = QPushButton("Ir a creación de los datos ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_datos)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        # Añadimos los widgets al layout
        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addSpacing(30)
        self.layout_principal.addWidget(self.area_texto)
        self.layout_principal.addSpacing(30)
        self.layout_principal.addWidget(self.btn_seguir)
        self.setLayout(self.layout_principal)
    
    def ir_a_datos(self):
        self.widget_apilado.setCurrentIndex(1)

class CreacionDatos(QWidget):
    """Página de creación de la base de datos"""
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def init_ui(self):

        self.layout_principal = QVBoxLayout()
        
        # Título
        self.etiqueta_titulo = QLabel("Generación de Datos")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)
        
        # Contenedor del contenedor de formulario y la vista de tabla

        self.layout_contenido = QHBoxLayout()

        # Contenedor del formulario y su explicación
        self.layout_formulario = QVBoxLayout()
        
        # Explicación del formulario
        self.caja_texto = QLabel(textos.creacion())
        self.caja_texto.setWordWrap(True)
        self.caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_texto.setFont(QFont("Noto Serif", 14))
        self.caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        self.area_doc = QScrollArea()
        self.area_doc.setWidgetResizable(True)
        self.area_doc.setWidget(self.caja_texto)
        self.area_doc.setFrameShape(QFrame.Box)
        self.area_doc.setFrameShadow(QFrame.Raised)
        self.area_doc.setLineWidth(4)

        # Formulario
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignRight)
        self.form_layout.setFormAlignment(Qt.AlignLeft)
        
        # ComboBox para cantidad de datos
        self.combo_cantidad = QComboBox()
        self.combo_cantidad.addItems(["500", "1000", "5000"])
        self.combo_cantidad.setMinimumWidth(150)
        
        # Slider horizontal (1-100%)
        self.slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(99)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setMinimumWidth(150)
        
        self.slider_label = QLabel("50%")
        self.slider_label.setMinimumWidth(50)
        self.slider.valueChanged.connect(self.update_slider_label)
        
        
        # Botón para generar datos
        self.btn_generar = QPushButton("Generar Datos")
        self.btn_generar.setFont(QFont("Arial", 12))
        self.btn_generar.setMinimumHeight(40)
        self.btn_generar.setMaximumWidth(200)
        self.btn_generar.clicked.connect(self.generar_datos)
        self.btn_generar.clicked.connect(self.cargar_dataframe)
        
        self.btn_contenedor = QHBoxLayout()

        # Vista de tabla de los datos
        self.tabla_muestra = QTableWidget()
        self.tabla_muestra.setAlternatingRowColors(True)
        self.tabla_muestra.horizontalHeader().setStretchLastSection(True)
        self.tabla_muestra.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

                
        # Botón para continuar al EDA
        self.btn_seguir = QPushButton("Ir a análisis exploratorio ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_eda)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;"+"color: #ffcb53;")
        
        # Agregamos las partes a la página
        self.layout_principal.addWidget(self.etiqueta_titulo)

        self.layout_principal.addSpacing(30)

        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.slider_label)
        self.form_layout.addRow("Cantidad de datos:", self.combo_cantidad)
        self.form_layout.addRow("Porcentaje de personas a hospitalizar:", self.slider_layout)
        self.layout_formulario.addLayout(self.form_layout)

        self.layout_formulario.addWidget(self.area_doc)
        self.btn_contenedor.addStretch()
        self.btn_contenedor.addWidget(self.btn_generar)
        self.btn_contenedor.addStretch()
        self.layout_formulario.addLayout(self.btn_contenedor)

        self.layout_contenido.addLayout(self.layout_formulario)
        self.layout_contenido.addWidget(self.tabla_muestra)

        self.layout_principal.addLayout(self.layout_contenido)
                    
        self.layout_principal.addSpacing(30)

        self.layout_principal.addWidget(self.btn_seguir)
        self.setLayout(self.layout_principal)
    
    def update_slider_label(self, value):
        """Actualiza el label del slider con el porcentaje"""
        self.slider_label.setText(f"{value}%")
    
    def info_df(self):
        """Recopila y devuelve información de los datos creados."""
        return info.info_datos_originales()

    def cargar_dataframe(self):
        """Carga un DataFrame en la tabla"""
        df = leer_datos.muestra_df()
        if df is None or df.empty:
            self.tabla_muestra.setRowCount(0)
            self.tabla_muestra.setColumnCount(0)
            return
        
        # Configurar dimensiones
        self.tabla_muestra.setRowCount(df.shape[0])
        self.tabla_muestra.setColumnCount(df.shape[1])
        
        # Configurar encabezados
        self.tabla_muestra.setHorizontalHeaderLabels(df.columns.tolist())
        self.tabla_muestra.setVerticalHeaderLabels([str(i) for i in df.index])
        
        # Llenar la tabla con los datos
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                value = str(df.iloc[i, j])
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                # Hacer las celdas de solo lectura
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tabla_muestra.setItem(i, j, item)
                
        # Recopilar info de los datos
        info = self.info_df()

        # Mostrar información
        self.caja_texto.setText(textos.creacion() + '\n\n' + info)
    
    def generar_datos(self):
        """Llama a la función de generación de datos y muestra el resultado"""
        cantidad = int(self.combo_cantidad.currentText())
        porcentaje = self.slider.value()
        
        # Llamar a tu función (descomenta cuando tengas el módulo)
        generador_datos.generar_datos(cantidad, porcentaje/100)
                    
    def ir_a_eda(self):
        self.widget_apilado.setCurrentIndex(2)


class PaginaEDA(QWidget):
    """Página de análisis EDA"""
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def init_ui(self):
        self.layout_principal = QVBoxLayout()

        self.etiqueta_titulo = QLabel("Análisis Exploratorio")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        self.pestañas = QTabWidget()
        self.transformacion = self.crear_pest("num")
        self.errores = self.crear_pest("err")
        self.pestañas.addTab(self.transformacion, u"Transformación")
        self.pestañas.addTab(self.errores, u"Errores")

        layout = QGridLayout()
        label = QLabel("Página de EDA")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.btn_seguir = QPushButton("Ir a creación del modelo ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_modelo)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addWidget(self.pestañas)
        self.layout_principal.addWidget(self.btn_seguir)
        self.setLayout(self.layout_principal)

    def cargar_dataframe(self, muestra_df: QTableWidget):
        """Carga un DataFrame en la tabla"""
        df = leer_datos.muestra_df()

        if df is None or df.empty:
            muestra_df.setRowCount(0)
            muestra_df.setColumnCount(0)
            return
        
        # Configurar dimensiones
        muestra_df.setRowCount(df.shape[0])
        try:
            muestra_df.setColumnCount(df.shape[1])
        except IndexError:
            muestra_df.setColumnCount(1)
        
        # Configurar encabezados
        muestra_df.setHorizontalHeaderLabels(df.columns.tolist())
        muestra_df.setVerticalHeaderLabels([str(i) for i in df.index])
        
        # Llenar la tabla con los datos
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                value = str(df.iloc[i, j])
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                # Hacer las celdas de solo lectura
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                muestra_df.setItem(i, j, item)
        return muestra_df
    
    def crear_pest(self, nom: str):
        pestaña = QWidget()

        layout_pest = QHBoxLayout()

        layout_izq = QVBoxLayout()

        form_layout = QHBoxLayout()

        form_cols = QComboBox()

        form_accion = QComboBox()

        muestra_df = QTableWidget()
        muestra_df = self.cargar_dataframe(muestra_df)

        llamadas = {"num":"textos.transf_num()",
                    "err":"textos.trat_err()"}

        caja_texto = QLabel(eval(llamadas[nom]))
        caja_texto.setWordWrap(True)
        caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        caja_texto.setFont(QFont("Noto Serif", 14))
        caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        area_doc = QScrollArea()
        area_doc.setWidgetResizable(True)
        area_doc.setWidget(caja_texto)
        area_doc.setFrameShape(QFrame.Box)
        area_doc.setFrameShadow(QFrame.Raised)
        area_doc.setLineWidth(4)

        doc_layout = QHBoxLayout()
        doc_layout.addWidget(area_doc)

        if nom == 'num':
            btn_arreglar = QPushButton(u"Transformar datos")
        elif nom == 'err':
            btn_arreglar = QPushButton(u"Eliminar errores")
        btn_arreglar.clicked.connect(self.ir_a_modelo)

        form_layout.addStretch()
        form_layout.addWidget(form_cols)
        if nom == 'err':
            form_layout.addWidget(form_accion)
        form_layout.addWidget(btn_arreglar)
        form_layout.addStretch()
        layout_izq.addLayout(form_layout)
        layout_izq.addLayout(doc_layout)
        layout_pest.addLayout(layout_izq)
        layout_pest.addWidget(muestra_df)
        if nom == 'num':
            layout_pest.setStretch(0,8)
            layout_pest.setStretch(1,2)
        pestaña.setLayout(layout_pest)

        return pestaña

    def ir_a_modelo(self):
        self.widget_apilado.setCurrentIndex(3)

class CreacionModelo(QWidget):
    """Página de creación del modelo"""
    def __init__(self):
        super().__init__()
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Página de creación del modelo")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.btn_seguir = QPushButton("Ir a evaluación del modelo ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_evaluacion)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")
        layout.addWidget(self.btn_seguir)
        self.setLayout(layout)

    def ir_a_evaluacion(self):
        self.widget_apilado.setCurrentIndex(4)

class EvaluacionModelo(QWidget):
    """Página de evaluación del modelo"""
    def __init__(self):
        super().__init__()
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Página de evaluación del modelo")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.btn_seguir = QPushButton("Ir a gráficas e informes ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_graficos)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")
        layout.addWidget(self.btn_seguir)
        self.setLayout(layout)

    def ir_a_graficos(self):
        self.widget_apilado.setCurrentIndex(5)

class InformeGraficos(QWidget):
    """Página de gráficas e informes"""
    def __init__(self):
        super().__init__()
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Página de gráficas e informes")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.btn_seguir = QPushButton("Volver a creación de la base de datos ⮌")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_datos)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")
        layout.addWidget(self.btn_seguir)
        self.setLayout(layout)

    def ir_a_datos(self):
        self.widget_apilado.setCurrentIndex(1)

class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación"""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Análisis de datos médicos")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central con QStackedWidget para manejar las páginas
        self.widget_apilado = QStackedWidget()
        self.setCentralWidget(self.widget_apilado)
        
        # Crear y agregar páginas
        self.pagina_bienvenida = PaginaBienvenida(self.widget_apilado)
        self.datos = CreacionDatos(self.widget_apilado)
        self.pagina_eda = PaginaEDA(self.widget_apilado)
        self.creacion_modelo = CreacionModelo(self.widget_apilado)
        self.evaluacion_modelo = EvaluacionModelo(self.widget_apilado)
        self.informe_graficos = InformeGraficos(self.widget_apilado)
        
        self.widget_apilado.addWidget(self.pagina_bienvenida)  # índice 0
        self.widget_apilado.addWidget(self.datos)              # índice 1
        self.widget_apilado.addWidget(self.pagina_eda)         # índice 2
        self.widget_apilado.addWidget(self.creacion_modelo)    # índice 3
        self.widget_apilado.addWidget(self.evaluacion_modelo)  # índice 4
        self.widget_apilado.addWidget(self.informe_graficos)   # índice 5

        # Mostrar la página de bienvenida
        self.widget_apilado.setCurrentIndex(0)

        # Paleta de colores 
        paleta_basica = QPalette()
        pinceles = {}
        valores = [(0, 0, 0, 255),(168, 38, 38, 255),(255, 255, 255, 255),
                   (217, 216, 216, 255),(89, 89, 89, 255),(119, 119, 119, 255),
                   (179, 178, 178, 255),(255, 255, 220, 255),(0, 0, 0, 128),
                   (0, 120, 215, 255)]
        for x in range(1,10):
            pincel = QBrush(QColor(*valores[x]), Qt.SolidPattern)
            pinceles[f'{x}'] = pincel # Creamos los pinceles con su RGB 

        pinceles_paleta = {'Active':{'WindowText':0,'Button':1,'Light':2,'Midlight':3,'Dark':4,'Mid':5,
                   'Text':0,'BrightText':2,'ButtonText':0,'Base':2,'Window':6,'Shadow':0,
                   'Highlight':1,'AlternateBase':1,'ToolTipBase':7,'ToolTipText':0,'PlaceholderText':0},

                   'Inactive':{'WindowText':0,'Button':1,'Light':2,'Midlight':3,'Dark':4,'Mid':5,
                   'Text':0,'BrightText':2,'ButtonText':0,'Base':2,'Window':6,'Shadow':0,
                   'Highlight':1,'AlternateBase':3,'ToolTipBase':7,'ToolTipText':0,'PlaceholderText':8},

                   'Disabled':{'WindowText':4,'Button':1,'Light':2,'Midlight':3,'Dark':4,'Mid':5,
                   'Text':4,'BrightText':2,'ButtonText':4,'Base':6,'Window':6,'Shadow':0,
                   'Highlight':9,'AlternateBase':6,'ToolTipBase':7,'ToolTipText':0,'PlaceholderText':8}}
        # Relacionamos cada característica con un pincel de la lista
        # Y aplicamos cada pincel a la paleta:
        for estado in pinceles_paleta.keys():
            for parte in pinceles_paleta[estado].keys():
                eval(f'paleta_basica.setBrush(QPalette.{estado}, QPalette.{parte}, QBrush(QColor(*valores[{pinceles_paleta[estado][parte]}]), Qt.SolidPattern))')

        self.widget_apilado.setPalette(paleta_basica)


def main():
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()