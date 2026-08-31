import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QScrollArea, 
                             QFormLayout, QComboBox, QSlider, QPushButton, QTableWidget, 
                             QHeaderView, QTableWidgetItem, QTabWidget, QGridLayout, QProgressBar,
                             QMessageBox, QMainWindow, QStackedWidget, QApplication)
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QThreadPool
from PyQt5.QtGui import QFont, QPalette, QBrush, QColor
from servicios.textuales import Textos, Info, Informe
from servicios.generador_datos import Generador_Datos
from servicios.analisis import Leer_Datos, Analisis, Limpieza
from servicios.modelos import Modelo, Evaluacion
from servicios.graficos import Eda, GrafModelo, Informes
from servicios.trabajador import Trabajador, ControlEntrenamiento, CapturadorConsola
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
        self.caja_texto = QLabel(Textos.bienvenida())
        self.caja_texto.setWordWrap(True)
        self.caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_texto.setFont(QFont("Noto Serif", 20))
        self.caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")
        
        # Área con barra de desplazamiento para el texto
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
        # Contenedor principal
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
        self.caja_texto = QLabel(Textos.creacion())
        self.caja_texto.setWordWrap(True)
        self.caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_texto.setFont(QFont("Noto Serif", 14))
        self.caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")
        
        # Área con barra de desplazamiento para el texto
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
        self.combo_cantidad.addItems(["500", "1000", "5000", "25000", "50000"])
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
        self.slider.valueChanged.connect(self.actualizar_texto_slider)
        
        
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
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")
        
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
    
    def actualizar_texto_slider(self, value):
        """Actualiza el label del slider con el valor en porcentaje"""
        self.slider_label.setText(f"{value}%")
    
    def info_df(self):
        """Recopila y devuelve información de los datos creados."""
        return Info.info_datos_originales()

    def cargar_dataframe(self):
        """Carga un DataFrame en la tabla"""
        df = Leer_Datos.muestra_df()
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
        self.caja_texto.setText(Textos.creacion() + '\n\n' + info)
        self.caja_texto.adjustSize()
    
    def generar_datos(self):
        """Llama a la función de generación de datos y muestra el resultado"""
        cantidad = int(self.combo_cantidad.currentText())
        porcentaje = self.slider.value()
        
        Generador_Datos.generar_datos(cantidad, porcentaje/100)
                    
    def ir_a_eda(self):
        self.widget_apilado.setCurrentIndex(2)

class PaginaEDA(QWidget):
    """Página de análisis EDA"""
    from pandas import DataFrame
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def init_ui(self):
        # Contenedor principal
        self.layout_principal = QVBoxLayout()

        # Título
        self.etiqueta_titulo = QLabel("Análisis Exploratorio")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        # Widget de pestañas con sus tres pestañas
        self.pestañas = QTabWidget()
        self.transformacion = self.crear_pest("num")
        self.errores = self.crear_pest("err")
        self.graficas = self.crear_pest_graf()
        self.pestañas.addTab(self.transformacion, u"Transformación")
        self.pestañas.addTab(self.errores, u"Errores")
        self.pestañas.addTab(self.graficas, u"Representación gráfica")

        # Añadimos el título y las pestañas
        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addWidget(self.pestañas)
        self.setLayout(self.layout_principal)

    def cargar_dataframe(self, df: DataFrame, muestra_df: QTableWidget) -> QTableWidget:
        """Carga un DataFrame en la tabla"""
        df = Leer_Datos.muestra_df(df=df)

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
    
    def crear_pest(self, nom: str) -> QWidget:
        """Crea las pestañas de conversión a numérico y tratamiento de errores"""
        # Pestaña es el QWidget que contendrá todo
        pestaña = QWidget()
        # Pestaña necesita un layout que contenga los layouts y widgets:
        layout_pest = QHBoxLayout()
        # Contenedor de la parte izquierda de la pestaña
        layout_izq = QVBoxLayout()
        # Contenedor de la parte derecha de la pestaña
        layout_dcha = QVBoxLayout()
        # Texto explicativo y widget para visualización del DataFrame
        df_label = QLabel()
        muestra_df = QTableWidget()

        def boton_transf():
            """
            Al pulsar el botón, genera información de la columna seleccionada, muéstrala en caja_texto
            y genera y muestra las 15 primeras y últimas entradas de dicha columna.
            """
            col = form_cols.currentText()
            if col != 'Elige una columna':
                info = Info.info_datos_num(col)
                caja_texto.setText(eval(switch[nom]) + info)
                caja_texto.adjustSize()
                df_num = Limpieza.cadena_a_numero(cols=[col], modo='columna')
                self.cargar_dataframe(df_num, muestra_df)

        def boton_err():
            """
            Al pulsar el botón, genera información de errores de la columna seleccionada, muéstrala en caja_texto 
            y carga y muestra las primeras y últimas 15 filas del DataFrame libre de errores.
            """
            col = form_cols.currentText()
            if col != 'Elige una columna':
                df_num = Limpieza.cadena_a_numero(modo='num')
                df_err = Limpieza.limpiar_errores(df=df_num)
                self.cargar_dataframe(df_err, muestra_df)
                info = Info.info_datos_noerr(col)
                caja_texto.setText(eval(switch[nom]) + info)
                caja_texto.adjustSize()

        # Cargamos los datos
        df = Leer_Datos.abrir_csv()

        # Contenedor y formulario para seleccionar el nombre de la columna a explorar
        form_layout = QHBoxLayout()
        form_cols = QComboBox()

        # Generamos los objetos de la ComboBox según qué pestaña sea
        btn_arreglar = QPushButton()
        if nom == 'num':
            columnas = [col for col in df.columns if df[col].dtype == 'str' and col != 'hospitalizacion']
            form_cols.addItems(['Elige una columna'] + columnas)
            df_label.setText("Columna transformada")
            btn_arreglar.setText(u"Transformar datos")
            btn_arreglar.clicked.connect(boton_transf)

        elif nom == 'err':
            df_num = Limpieza.cadena_a_numero()
            columnas = [col for col in df_num.columns if col != 'id']
            form_cols.addItems(['Elige una columna'] + columnas)
            df_label.setText("DataFrame libre de errores")
            btn_arreglar.setText(u"Eliminar errores")
            btn_arreglar.clicked.connect(boton_err)

        # Diccionario que nos devuelve la llamada a una función según el nombre de la pestaña
        switch = {"num":"Textos.transf_num()",
                    "err":"Textos.trat_err()"}

        # Texto explicativo
        caja_texto = QLabel()
        caja_texto.setText(eval(switch[nom]))
        caja_texto.adjustSize()
        caja_texto.setWordWrap(True)
        caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        caja_texto.setFont(QFont("Noto Serif", 14))
        caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        # Área con barra de desplazamiento para el texto
        area_doc = QScrollArea()
        area_doc.setWidgetResizable(True)
        area_doc.setWidget(caja_texto)
        area_doc.setFrameShape(QFrame.Box)
        area_doc.setFrameShadow(QFrame.Raised)
        area_doc.setLineWidth(4)

        doc_layout = QHBoxLayout()

        # Agregamos las partes a la pestaña
        form_layout.addWidget(form_cols)
        form_layout.addWidget(btn_arreglar)
        form_layout.addStretch()
        layout_izq.addLayout(form_layout)
        layout_izq.addLayout(doc_layout)
        doc_layout.addWidget(area_doc)
        layout_pest.addLayout(layout_izq)
        layout_dcha.addWidget(df_label)
        layout_dcha.addWidget(muestra_df)
        layout_pest.addLayout(layout_dcha)
        if nom == 'num':
            layout_pest.setStretch(0,9)
            layout_pest.setStretch(1,1)
        elif nom == 'err':
            layout_pest.setStretch(0,69)
            layout_pest.setStretch(1,31)
        pestaña.setLayout(layout_pest)

        return pestaña
    
    def crear_pest_graf(self):
        """Crea la pestaña de gráficas"""
        # Contenedor principal
        pestaña = QWidget()
        layout_pest = QVBoxLayout()

        # Cargamos el DataFrame
        df_num = Limpieza.cadena_a_numero()
        columnas = [col for col in df_num.columns if col != 'id']
        # Creamos y poblamos el formulario desplegable
        layout_form = QHBoxLayout()
        form_cols = QComboBox()
        form_cols.addItems(['Elige una columna'] + columnas)

        # Creamos la figura, y la dibujamos al pulsar el botón
        figura = Figure()
        area_graf = FigureCanvas(figura)
        def btn_graf():
            col =  form_cols.currentText()
            if col != 'Elige una columna':
                # Limpiamos figura anterior
                figura.clear()

                # Hacemos llamada según la columna
                if col != 'hospitalizacion':
                    Eda.cols_num(figura, col)
                else:
                    Eda.col_hosp(figura)

                # Actualizamos el lienzo
                area_graf.draw()

        # Botón para crear la gráfica
        btn_mostrar = QPushButton('Generar gráfica')
        btn_mostrar.clicked.connect(btn_graf)

        # Botón para continuar 
        btn_seguir = QPushButton("Ir a creación del modelo ➢")
        btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        btn_seguir.setMinimumHeight(40)
        btn_seguir.clicked.connect(self.ir_a_modelo)
        btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        # Agregamos todo a la pestaña
        layout_form.addWidget(form_cols)
        layout_form.addWidget(btn_mostrar)
        layout_form.addStretch(7)
        layout_pest.addLayout(layout_form)
        layout_pest.addWidget(area_graf)
        layout_pest.addWidget(btn_seguir)
        pestaña.setLayout(layout_pest)

        return pestaña


    def ir_a_modelo(self):
        self.widget_apilado.setCurrentIndex(3)

class CreacionModelo(QWidget):
    """Página de creación del modelo"""
    # Señal para enviar el modelo que creemos
    enviar_modelo = pyqtSignal(object)
        
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        # Colección de hilos de procesamiento
        self.threadpools = dict()
        self.init_ui()

    def init_ui(self):
        # Contenedor principal
        self.layout_principal = QVBoxLayout()

        # Título
        self.etiqueta_titulo = QLabel("Selección del modelo")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        # Widget de pestañas con sus tres pestañas
        self.pestañas = QTabWidget()
        self.reglog = self.crear_pest("reglog")
        self.bosque = self.crear_pest("bosque")
        self.xgb = self.crear_pest("xgb")
        self.pestañas.addTab(self.reglog, u"Regresión Logística")
        self.pestañas.addTab(self.bosque, u"Bosque aleatorio")
        self.pestañas.addTab(self.xgb, u"Potenciación Extrema del Gradiente")
        # Recogemos los modelos creados en el siquiente diccionario
        self.modelos = {}
        # NOTA: si se crean dos modelos del mismo tipo, el último sobreescribirá al anterior. 
        # Sólo puede haber un modelo de cada tipo en un momento dado.

        # Añadimos el título y las pestañas
        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addWidget(self.pestañas)
        self.setLayout(self.layout_principal)

    def crear_pest(self, nom: str) -> QWidget:
        """ 
        Crea una pestaña según el modelo a crear, utilizando multihilo.
        """
        # Añadimos el hilo de esta pestaña al diccionario
        self.threadpools[nom] = QThreadPool()
        # Creamos variable de control para la barra de progreso
        control_entrenamiento = ControlEntrenamiento()

        # Contenedor general
        pestaña = QWidget()
        layout_pest = QHBoxLayout()
        # Contenedor izquierdo
        layout_izq = QVBoxLayout()
        # Contenedor derecho
        layout_dcha = QVBoxLayout()


        # Botón para continuar a la siguiente página: 
        # lo creamos oculto para asegurar que sólo se pueda pulsar si hay un modelo ya creado
        btn_seguir = QPushButton("Continuar con este modelo ➢")
        btn_seguir.setHidden(True)
        btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        btn_seguir.setMinimumHeight(40)
        btn_seguir.clicked.connect(lambda: self.ir_a_evaluacion(self.modelos[nom]))
        btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        # Formulario de selección de parámetros
        form_layout = QVBoxLayout()
        params_layout = QHBoxLayout()
        params_layout, parametros = self.crear_combos(params_layout, nom)

        switch = {"reglog":"Textos.modelo_reglog()",
                    "bosque":"Textos.modelo_bosque()",
                    "xgb":"Textos.modelo_xgb()"}

        doc_layout = QHBoxLayout()
        # Texto explicativo del modelo
        caja_texto = QLabel()
        caja_texto.setText(eval(switch[nom]))
        caja_texto.setWordWrap(True)
        caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        caja_texto.setFont(QFont("Noto Serif", 14))
        caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")
        caja_texto.adjustSize()
        # Área con barra de desplazamiento para el texto
        area_doc = QScrollArea()
        area_doc.setWidgetResizable(True)
        area_doc.setWidget(caja_texto)
        area_doc.setFrameShape(QFrame.Box)
        area_doc.setFrameShadow(QFrame.Raised)
        area_doc.setLineWidth(4)

        # Creamos las barras de progreso y las etiquetas de iteración y candidato, y las ocultamos
        barra_progreso_total = QProgressBar()
        barra_progreso_parcial = QProgressBar()
        etiqueta_progreso_iter = QLabel()
        etiqueta_progreso_cand = QLabel()
        barra_progreso_total.setHidden(True)
        barra_progreso_parcial.setHidden(True)
        etiqueta_progreso_iter.setHidden(True)
        etiqueta_progreso_cand.setHidden(True)

        def boton_modelo(nom: str, gcsv: bool = False):
            """
            Genera el modelo escogido al pulsar el botón asociado y realiza varias acciones menores asociadas.
            
            :param nom: Nombre del modelo escogido.
            :type nom: str
            :param gcsv: Define si se creará un modelo con los hiperparámetros recibidos, o se optimizará usando GridSearchCV
            :type gcsv: bool
            """
            barra_progreso_total.setHidden(False)  # Mostramos la barra de progreso general
            btn_seguir.setEnabled(False) # Desactivamos el botón para evitar que se pulse a mitad de creación de un nuevo modelo

            if gcsv:
                # Mostramos las barras y etiquetas de progreso
                barra_progreso_parcial.setHidden(False)
                etiqueta_progreso_iter.setHidden(False)
                etiqueta_progreso_cand.setHidden(False)
                btn_crear.setEnabled(False)
                btn_optim.setEnabled(False) # Para evitar dobles clicks accidentales
                btn_optim.setStyleSheet(u"background-color: #00b300;") # Color verde
                btn_crear.setStyleSheet(u"background-color: #68c5d8;") # Color azulado
                self.capturador_actual = CapturadorConsola() # Captura progreso mediante verbose en consola
                trabajador = Trabajador(Modelo.gs_cv, nom, capturador=self.capturador_actual) # Gestiona el entrenamiento del modelo

                # Conectamos el capturador con las barras de progreso
                self.capturador_actual.progreso_total.connect(barra_progreso_total.setValue)
                self.capturador_actual.progreso_parcial.connect(barra_progreso_parcial.setValue)

                def texto_progreso(datos: dict):
                    """
                    Genera el texto de progreso actual y actualiza las etiquetas de progreso
                    
                    :param datos: Datos de la iteración y candidato actuales.
                    :type datos: dict
                    """
                    if datos['iter'] and datos['iter'] > 0:
                        mensaje = f'''Iteración nº: {datos['iter']}'''
                        etiqueta_progreso_iter.setText(mensaje)
                    if datos['cand'] and datos['cand'] > 0:
                        mensaje = f'''Candidato nº {datos['cand']} de {datos['cand_total']}'''
                        etiqueta_progreso_cand.setText(mensaje)

                self.capturador_actual.mensaje_status.connect(texto_progreso) # Actualizamos las etiquetas de progreso            
                trabajador.señales.terminado.connect(terminar_entrenamiento) # Señal de finalización 
                trabajador.señales.error.connect(error_entrenamiento) # Señal de error

                self.threadpools[nom].start(trabajador) # Ejecuta el trabajador en su hilo correspondiente

            else:
                btn_optim.setEnabled(False)
                btn_crear.setEnabled(False) # Para evitar dobles clicks accidentales
                btn_crear.setStyleSheet(u"background-color: #00b300;") # Color verde
                btn_optim.setStyleSheet(u"background-color: #68c5d8;") # Color azulado

                params = [] # Recogemos los parámetros seleccionados en los formularios
                for k, v in parametros.items():
                    params.append(v.currentData())
                
                if nom == 'reglog':
                    control_entrenamiento.total_pasos = parametros['max_iter'].currentData() # El número total de pasos de la barra de progreso será "max_iter"
                    trabajador = Trabajador(Modelo.reglog, *params, objeto_control=control_entrenamiento) # Gestiona el entrenamiento del modelo

                elif nom == 'bosque':
                    control_entrenamiento.total_pasos = parametros['n_estimators'].currentData() # El número total de pasos de la barra de progreso será "n_estimators"
                    trabajador = Trabajador(Modelo.bosque, *params, objeto_control=control_entrenamiento) # Gestiona el entrenamiento del modelo

                elif nom == 'xgb':
                    control_entrenamiento.total_pasos = parametros['n_estimators'].currentData() # El número total de pasos de la barra de progreso será "n_estimators"
                    trabajador = Trabajador(Modelo.xgb, *params, objeto_control=control_entrenamiento) # Gestiona el entrenamiento del modelo

                trabajador.señales.progreso.connect(barra_progreso_total.setValue) # El trabajador emite una señal de progreso que conectamos con la barra de progreso
                trabajador.señales.terminado.connect(terminar_entrenamiento) # Señal de finalización 
                trabajador.señales.error.connect(error_entrenamiento) # Señal de error

                self.threadpools[nom].start(trabajador) # Ejecuta el trabajador en su hilo correspondiente

        # Contenedor y botones para crear el modelo: usando los parámetros elegidos o GridSearchCV
        btn_layout = QHBoxLayout()
        btn_crear = QPushButton()
        btn_crear.setStyleSheet(u"background-color: #68c5d8;")
        btn_optim = QPushButton()
        btn_optim.setStyleSheet(u"background-color: #68c5d8;")
        btn_optim.setText(u"Crear modelo optimizado con validación cruzada")
        modelo_label = QLabel()

        if nom == 'reglog':
            modelo_label.setText("Modelo de Regresión Logística")
            btn_crear.setText(u"Crear modelo de Regresión Logística")
            btn_crear.clicked.connect(lambda: boton_modelo(nom, False))
            btn_optim.clicked.connect(lambda: boton_modelo(nom, True))

        elif nom == 'bosque':
            modelo_label.setText("Modelo de Bosque Aleatorio")
            btn_crear.setText(u"Crear modelo de Bosque Aleatorio")
            btn_crear.clicked.connect(lambda: boton_modelo(nom, False))
            btn_optim.clicked.connect(lambda: boton_modelo(nom, True))

        elif nom == 'xgb':
            modelo_label.setText("Modelo de Potenciación Extrema del Gradiente")
            btn_crear.setText(u"Crear modelo XGBoost")
            btn_crear.clicked.connect(lambda: boton_modelo(nom, False))
            btn_optim.clicked.connect(lambda: boton_modelo(nom, True))

        # Figura que mostrará la gráfica creada y su contenedor
        figura = Figure()
        repr_modelo = FigureCanvas(figura)

        def generar_grafica(modelo: dict, X, y) -> None:
            """
            Limpia la gráfica anterior, genera y muestra una nueva gráfica con los datos del modelo.
            
            :param modelo: Diccionario con los datos del modelo
            :type modelo: dict
            :param X: Corresponde a X_test
            :param y: Corresponde a y_test
            """
            # Limpiamos figura anterior
            figura.clear()
            ax = figura.add_subplot(111)

            modelo['y_pred'] = modelo['modelo'].predict(X) # Creamos y añadimos al diccionario la predicción
            GrafModelo.graf_muestra(y, modelo['y_pred'], ax) # Dibujamos la gráfica en el eje que ya creamos

            nom_modelo = type(modelo['modelo']).__name__
            ax.set_title(f'{nom_modelo} de hospitalización de pacientes')

            # Actualizamos el lienzo
            repr_modelo.draw()

        params_label = QLabel()
        params_label.setHidden(True)

        def terminar_entrenamiento(modelo: dict) -> None:
            """
            Realiza las operaciones necesarias al recibir la señal de finalización con éxito del trabajador.
            
            :param modelo: Diccionario que contiene el modelo y los datos de testeo. 
            :type modelo: dict
            """
            self.modelos[nom] = modelo
            print(self.modelos)
            X_test = modelo['X_test']
            y_test = modelo['y_test']

            generar_grafica(self.modelos[nom], X_test, y_test)

            btn_seguir.setHidden(False)
            btn_seguir.setEnabled(True) # Activamos el botón para continuar

            btn_crear.setEnabled(True)
            btn_optim.setEnabled(True) # Activamos los botones de creación del modelo
            barra_progreso_parcial.setHidden(True)
            barra_progreso_total.setHidden(True)
            etiqueta_progreso_iter.setHidden(True)
            etiqueta_progreso_cand.setHidden(True) # Escondemos las barras y etiquetas de progreso

            # Mostramos los parámetros usados en el entrenamiento
            parametros = modelo['modelo'].get_params()
            specs = '<br><u>Parámetros del modelo entrenado</u>:\n<ul>'
            for k in parametros:
                if parametros[k] and parametros[k] != 0:
                    specs += f'<li><b>{k}</b>: {parametros[k]}\n</li>'
            specs += '</ul>'
                
            params_label.setText(specs)
            params_label.setHidden(False)
            params_label.adjustSize()
        
        def error_entrenamiento(mensaje: str) -> None:
            """
            Muestra el error recibido del trabajador en una caja de mensaje, oculta las barras y etiquetas de progreso 
            y activa los botones de nuevo.
            
            :param mensaje: Mensaje de error.
            :type mensaje: str
            """
            QMessageBox.critical(self, 'Error de entrenamiento: ', mensaje)
            barra_progreso_parcial.setHidden(True)
            barra_progreso_total.setHidden(True)
            etiqueta_progreso_iter.setHidden(True)
            etiqueta_progreso_cand.setHidden(True)# Escondemos las barras y etiquetas de progreso
            btn_crear.setEnabled(True)
            btn_optim.setEnabled(True) # Activamos los botones de creación del modelo

        # Agregamos las partes a la pestaña 
        btn_layout.addStretch()
        btn_layout.addWidget(btn_crear)
        btn_layout.addWidget(btn_optim)
        btn_layout.addStretch()
        form_layout.addLayout(params_layout)
        form_layout.addLayout(btn_layout)
        layout_izq.addLayout(form_layout)
        doc_layout.addWidget(area_doc)
        layout_izq.addLayout(doc_layout)
        layout_izq.addWidget(params_label)
        layout_pest.addLayout(layout_izq)
        layout_dcha.addWidget(modelo_label, stretch=1)
        layout_dcha.addWidget(barra_progreso_total)
        layout_dcha.addWidget(barra_progreso_parcial)
        layout_dcha.addWidget(etiqueta_progreso_iter)
        layout_dcha.addWidget(etiqueta_progreso_cand)
        layout_dcha.addWidget(repr_modelo, stretch=9)
        layout_dcha.addWidget(btn_seguir)
        layout_pest.addLayout(layout_dcha)
        layout_pest.setStretch(0,58)
        layout_pest.setStretch(1,42)
        pestaña.setLayout(layout_pest)

        return pestaña
    
    def crear_combos(self, params_layout: QHBoxLayout, nom: str) -> tuple[QHBoxLayout, dict]:
        """
        Crea los formularios según los parámetros disponibles según el modelo, 
        y agrégalos a un layout con su título. 
        Finalmente, agrega dicho layout a un layout que será devuelto por la función.
        
        :param params_layout: Layout que contendrá los formularios.
        :type params_layout: QHBoxLayout
        :param nom: Nombre del modelo cuyos parámetros se van a seleccionar.
        :type nom: str
        :return: Layout con sus formularios y diccionario que contiene dichos formularios.
        :rtype: tuple[QHBoxLayout, dict]
        """
        params = Modelo.params(nom) # Recuperamos los parámetros del modelo actual
        parametros = {}
        params_layout.addStretch()
        for k, v in params.items():
            form_layout = QVBoxLayout()
            titulo = QLabel(k.capitalize())

            combo = QComboBox()
            for valor in v:
                combo.addItem(str(valor), userData=valor)
            parametros[k] = combo

            form_layout.addWidget(titulo)
            form_layout.addWidget(combo)
            params_layout.addLayout(form_layout)
        params_layout.addStretch()
        return params_layout, parametros
    
    def ir_a_evaluacion(self, modelo):
        """Envía el diccionario con el modelo a la siguiente página y muestra dicha página."""
        self.enviar_modelo.emit(modelo)
        self.widget_apilado.setCurrentIndex(4)

class EvaluacionModelo(QWidget):
    """Página de evaluación del modelo"""
    enviar_modelo = pyqtSignal(object) # Señal para enviar el modelo
    modelo =  None # Para evitar errores tipo UnboundError

    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def recibir_modelo(self, modelo: dict) -> None:
        """
        Recibe el modelo, modifica el título de la página y crea los KPIs y las gráficas.
        
        :param modelo: Diccionario que contiene el modelo entrenado, X_test, y_test e y_pred.
        :type modelo: dict
        """
        self.modelo = modelo
        print(self.modelo)
        self.etiqueta_titulo.setText(f"Evaluación del modelo {type(self.modelo['modelo']).__name__}")
        self.crear_kpis()
        self.crear_graficas()

    def init_ui(self):
        self.layout_principal = QVBoxLayout()
        self.layout_contenido = QHBoxLayout()

        self.layout_izda = QVBoxLayout()
        self.layout_kpis = QHBoxLayout()

        self.layout_dcha = QVBoxLayout()
        # Creamos las figuras para las tres gráficas
        self.figura_matriz_conf = Figure()
        self.graf_matriz_conf = FigureCanvas(self.figura_matriz_conf)
        self.figura_custom = Figure()
        self.graf_custom = FigureCanvas(self.figura_custom)
        self.figura_roc = Figure()
        self.graf_roc = FigureCanvas(self.figura_roc)

        # Título
        self.etiqueta_titulo = QLabel(f"Evaluación del modelo")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 50, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        # Texto explicativo
        self.caja_texto = QLabel()
        self.caja_texto.setText('')
        self.caja_texto.setWordWrap(True)
        self.caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_texto.setFont(QFont("Noto Serif", 14))
        self.caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        # Área con barra de desplazamiento para el texto explicativo
        self.area_doc = QScrollArea()
        self.area_doc.setWidgetResizable(True)
        self.area_doc.setWidget(self.caja_texto)
        self.area_doc.setFrameShape(QFrame.Box)
        self.area_doc.setFrameShadow(QFrame.Raised)
        self.area_doc.setLineWidth(4)

        # Botón para continuar a la siguiente página
        self.btn_seguir = QPushButton("Ir a gráficas e informes ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_graficos)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        # Agregamos todas las partes a la página
        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addLayout(self.layout_contenido)
        self.layout_contenido.addLayout(self.layout_izda)
        self.layout_izda.addLayout(self.layout_kpis)
        self.layout_izda.addWidget(self.area_doc)
        self.layout_dcha.addWidget(self.graf_matriz_conf)
        self.layout_dcha.addWidget(self.graf_custom)
        self.layout_dcha.addWidget(self.graf_roc)
        self.layout_contenido.addLayout(self.layout_dcha)
        self.layout_principal.addWidget(self.btn_seguir)
        self.setLayout(self.layout_principal)

    def crear_kpis(self) -> None:
        """
        Borra los KPIs que puedan haber quedado de modelos anteriores, 
        crea cada KPI como un título sobre una cifra en porcentaje,
        y los añade a la página. 
        
        """
        # Mecánica de limpieza de KPIs anteriores:
        while self.layout_kpis.count():
            objeto = self.layout_kpis.takeAt(0)
            widget = objeto.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        y_test = self.modelo['y_test'] 
        y_pred = self.modelo['y_pred'] 

        # Evaluamos el modelo
        self.modelo['kpis'] = Evaluacion.kpis(y_test, y_pred)
        self.layout_kpis.addStretch()
        # Creamos los KPIs como cajitas con un título y debajo la métrica en porcentaje
        for titulo, kpi in self.modelo['kpis'].items():
            contenedor = QWidget()
            caja_kpi = QVBoxLayout(contenedor)
            titulo_kpi = QLabel(titulo)
            fuente = QFont("Noto Serif", 14)

            titulo_kpi.setStyleSheet(u"padding: 15px;"
                                    "background-color: #777777;"
                                    "color: #ffffff;")
            titulo_kpi.setFont(fuente)
            titulo_kpi.setAlignment(Qt.AlignCenter)

            metrica = QLabel(f'{kpi:.2%}')
            metrica.setStyleSheet(u"padding: 15px;"
                                    "background-color:#000000;"
                                    "color:#ffffff;")
            metrica.setFont(fuente)
            metrica.setAlignment(Qt.AlignCenter)

            caja_kpi.addWidget(titulo_kpi)
            caja_kpi.addWidget(metrica)
            self.layout_kpis.addWidget(contenedor)
        self.layout_kpis.addStretch()
            
    def crear_graficas(self):
        """
        Limpia las figuras, crea las gráficas pertinentes y añade los datos al diccionario del modelo.
        
        """
        # Borra las figuras si había y crea las nuevas gráficas
        figuras = [self.figura_matriz_conf, self.figura_custom, self.figura_roc]
        axes = []
        for fig in figuras:
            fig.clear()
            ax = fig.add_subplot(111)
            axes.append(ax)
            fig.tight_layout(w_pad=1.15)
        nom = type(self.modelo["modelo"]).__name__
        axes, metricas = Evaluacion.eval_modelo(self.modelo, axes, nom)
        self.modelo['metricas'] = metricas # Añade los KPIs al diccionario del modelo

        self.graf_matriz_conf.draw()
        self.graf_roc.draw()
        self.graf_custom.draw() # Dibuja las tres gráficas

        texto_eval = Informe.informe_eval(nom, self.modelo['metricas'], self.modelo['kpis'])
        self.caja_texto.setText(texto_eval) # Generamos y mostramos la evaluación en función de los KPIs
        self.caja_texto.adjustSize()

    def ir_a_graficos(self):
        self.enviar_modelo.emit(self.modelo) # Enviamos el diccionario con el modelo, X_test, y_test, y_pred, metricas y KPIs
        self.widget_apilado.setCurrentIndex(5) # Cambiamos a la siquiente página

class InformeFinal(QWidget):
    """Página del informe final"""
    modelo = None
    kpis = dict()
    metricas = dict() # Para evitar UnboundError

    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def recibir_datos(self, modelo: dict) -> None:
        """
        Recibe los datos del modelo y sus métricas,
        guárdalos como variables locales y
        genera el texto del pie de la gráfica y el informe final.
        
        :param modelo: Diccionario que contiene el modelo entrenado, X_test, y_test, y_pred, las métricas y los kpis
        :type modelo: dict
        """
        self.modelo = modelo
        nom_modelo = type(self.modelo["modelo"]).__name__
        self.etiqueta_titulo.setText(f"Informe del modelo {nom_modelo}")

        print("Datos del modelo:\n",self.modelo)
        self.kpis = modelo["kpis"]
        print("Indicadores clave de rendimiento:\n", self.kpis)
        self.metricas = modelo["metricas"]

        texto_pie = Informe.pie_final(nom_modelo, self.metricas, self.kpis)
        self.caja_info.setText(texto_pie)
        self.caja_info.adjustSize()

        texto_informe = Informe.informe_final(nom_modelo, self.modelo['metricas'], self.modelo['kpis'])
        self.caja_texto.setText(texto_informe)
        self.caja_texto.adjustSize()

        self.grafica_resultado()

    def init_ui(self):
        self.layout_principal = QVBoxLayout()
        self.layout_contenido = QHBoxLayout()

        # Título
        self.etiqueta_titulo = QLabel(f"Informe del modelo")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 50, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        # Parte izquierda
        self.layout_izda = QVBoxLayout()

        # Texto del informe
        self.caja_texto = QLabel()
        self.caja_texto.setWordWrap(True)
        self.caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_texto.setFont(QFont("Noto Serif", 14))
        self.caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")
       
        # Área con barra de desplazamiento
        self.area_doc = QScrollArea()
        self.area_doc.setWidgetResizable(True)
        self.area_doc.setWidget(self.caja_texto)
        self.area_doc.setFrameShape(QFrame.Box)
        self.area_doc.setFrameShadow(QFrame.Raised)
        self.area_doc.setLineWidth(4)

        # Botón para guardar el modelo
        self.btn_guardar = QPushButton(u"💾 Guardar modelo")
        self.btn_guardar.setFont(QFont("System", 20))
        self.btn_guardar.setMinimumHeight(40)
        self.btn_guardar.clicked.connect(self.guardar_modelo)
        self.btn_guardar.setStyleSheet(u"background-color: #7cb51f;""color: #efdd52;")
        
        # Parte derecha
        self.layout_dcha = QVBoxLayout()

        # Área de la gráfica
        self.figura = Figure()
        self.area_graf = FigureCanvas(self.figura)

        # Texto resumen del modelo
        self.caja_info = QLabel()
        self.caja_info.setWordWrap(True)
        self.caja_info.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.caja_info.setFont(QFont("System", 14))
        self.caja_info.setStyleSheet(u"padding: 15px;"
                                      "background-color: #777777;"
                                      "color: #8cd124;")

        # Área con barra de desplazamiento
        self.area_info = QScrollArea()
        self.area_info.setWidgetResizable(True)
        self.area_info.setWidget(self.caja_info)
        self.area_info.setFrameShape(QFrame.Box)
        self.area_info.setFrameShadow(QFrame.Raised)
        self.area_info.setLineWidth(4)

        # Layout para los botones inferiores
        self.seguir_layout = QHBoxLayout()

        # Botón para volver a la página de creación del modelo
        self.btn_seguir_modelo = QPushButton("Volver a creación del modelo ⮌")
        self.btn_seguir_modelo.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir_modelo.setMinimumHeight(40)
        self.btn_seguir_modelo.clicked.connect(self.ir_a_modelo)
        self.btn_seguir_modelo.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        # Botón para volver al inicio de la aplicación
        self.btn_seguir = QPushButton("Volver al inicio ⮌")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_inicio)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        # Agregamos todas las partes a la página
        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addLayout(self.layout_contenido)
        self.layout_contenido.addLayout(self.layout_izda)
        self.layout_contenido.addLayout(self.layout_dcha)
        self.layout_izda.addWidget(self.area_doc)
        self.layout_izda.addWidget(self.btn_guardar)
        self.layout_principal.addLayout(self.layout_dcha)
        self.layout_dcha.addWidget(self.area_graf, 8)
        self.layout_dcha.addWidget(self.area_info, 2)
        self.seguir_layout.addWidget(self.btn_seguir_modelo)
        self.seguir_layout.addWidget(self.btn_seguir)
        self.layout_principal.addLayout(self.seguir_layout)
        self.setLayout(self.layout_principal)

    def guardar_modelo(self) -> None:
        """Guarda el modelo y sus especificaciones."""
        mensaje = ''
        try:
            mensaje = Modelo.guardar_modelo(modelo=self.modelo['modelo'],
                                kpis= self.modelo['kpis'])
            QMessageBox.information(self, 'Guardado del modelo', mensaje)
        except Exception as e:
            print('Error:', e)
            QMessageBox.critical(self, 'Error brutal', f'Encontramos la razón: {e}')

    def grafica_resultado(self) -> None:
        """Limpia y crea la gráfica correspondiente."""
        self.figura.clear()
        ax = self.figura.add_subplot(111)
        nom = type(self.modelo["modelo"]).__name__
        Informes.grafico_final(self.modelo, ax, nom)
        self.figura.tight_layout(w_pad=1.15)
        self.area_graf.draw()

    def ir_a_modelo(self) -> None:
        """Cambia la página a la de creación del modelo."""
        self.widget_apilado.setCurrentIndex(3)

    def ir_a_inicio(self) -> None:
        """Cambia la página a la de bienvenida."""
        self.widget_apilado.setCurrentIndex(0)

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
        self.informe_graficos = InformeFinal(self.widget_apilado)
        
        self.widget_apilado.addWidget(self.pagina_bienvenida)  # índice 0
        self.widget_apilado.addWidget(self.datos)              # índice 1
        self.widget_apilado.addWidget(self.pagina_eda)         # índice 2
        self.widget_apilado.addWidget(self.creacion_modelo)    # índice 3
        self.widget_apilado.addWidget(self.evaluacion_modelo)  # índice 4
        self.widget_apilado.addWidget(self.informe_graficos)   # índice 5
        
        self.creacion_modelo.enviar_modelo.connect(self.evaluacion_modelo.recibir_modelo)
        self.evaluacion_modelo.enviar_modelo.connect(self.informe_graficos.recibir_datos)

        # Mostrar la página de bienvenida
        self.widget_apilado.setCurrentIndex(0)

        # Paleta de colores 
        self.paleta_basica = QPalette()
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
                eval(f'self.paleta_basica.setBrush(QPalette.{estado}, QPalette.{parte}, QBrush(QColor(*valores[{pinceles_paleta[estado][parte]}]), Qt.SolidPattern))')

        self.widget_apilado.setPalette(self.paleta_basica)


def main():
    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()