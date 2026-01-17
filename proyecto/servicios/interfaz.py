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
    Tipo dashboard
    · matriz de confusión
        -> QCanvas
    · puntuaciones: precisión, recuperación 
        -> QLabel tipo KPI
    · curva ROC-AUC
        -> Gráfica en un QCanvas, QLabel con explicación
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
from servicios.textuales import *
from servicios.generador_datos import *
from servicios.analisis import *
from servicios.modelos import *
from servicios.graficos import *
from servicios.trabajador import Trabajador, ControlEntrenamiento
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

        '''# Botón modo oscuro
        self.btn_oscuro = QPushButton()
        self.btn_oscuro.setCheckable(True)
        if self.btn_oscuro.isChecked():
            VentanaPrincipal().widget_apilado.setPalette(VentanaPrincipal().paleta_oscura)
        else:
            VentanaPrincipal().widget_apilado.setPalette(VentanaPrincipal().paleta_basica)'''
        
        # Cuadro de texto 
        self.caja_texto = QLabel(Textos.bienvenida())
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
        #self.layout_principal.addWidget(self.btn_oscuro)
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
        self.caja_texto = QLabel(Textos.creacion())
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
    
    def actualizar_texto_slider(self, value):
        """Actualiza el label del slider con el porcentaje"""
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
    
    def generar_datos(self):
        """Llama a la función de generación de datos y muestra el resultado"""
        cantidad = int(self.combo_cantidad.currentText())
        porcentaje = self.slider.value()
        
        # Llamar a tu función (descomenta cuando tengas el módulo)
        Generador_Datos.generar_datos(cantidad, porcentaje/100)
                    
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
        self.graficas = self.crear_pest_graf()
        self.pestañas.addTab(self.transformacion, u"Transformación")
        self.pestañas.addTab(self.errores, u"Errores")
        self.pestañas.addTab(self.graficas, u"Representación gráfica")

        layout = QGridLayout()
        label = QLabel("Página de EDA")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addWidget(self.pestañas)
        self.setLayout(self.layout_principal)

    def cargar_dataframe(self, df, muestra_df: QTableWidget):
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
    
    def crear_pest(self, nom: str):

        pestaña = QWidget()
        layout_pest = QHBoxLayout()
        layout_izq = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_cols = QComboBox()
        df_layout = QVBoxLayout()
        df_label = QLabel()
        muestra_df = QTableWidget()
        caja_texto = QLabel()
        area_doc = QScrollArea()
        doc_layout = QHBoxLayout()
        btn_arreglar = QPushButton()

        df = Leer_Datos.abrir_csv()
        if nom == 'num':
            columnas = [col for col in df.columns if df[col].dtype == 'object' and col != 'hospitalizacion']
            form_cols.addItems(['Elige una columna'] + columnas)
            df_label.setText("Columna transformada")
        elif nom == 'err':
            df_num = Analisis.cadena_a_numero()
            columnas = [col for col in df_num.columns if col != 'id']
            form_cols.addItems(['Elige una columna'] + columnas)
            df_label.setText("DataFrame libre de errores")


        switch = {"num":"Textos.transf_num()",
                    "err":"Textos.trat_err()"}

        caja_texto.setText(eval(switch[nom]))
        caja_texto.setWordWrap(True)
        caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        caja_texto.setFont(QFont("Noto Serif", 14))
        caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        area_doc.setWidgetResizable(True)
        area_doc.setWidget(caja_texto)
        area_doc.setFrameShape(QFrame.Box)
        area_doc.setFrameShadow(QFrame.Raised)
        area_doc.setLineWidth(4)

        doc_layout.addWidget(area_doc)

        def boton_transf():
            col = form_cols.currentText()
            if col != 'Elige una columna':
                info = Info.info_datos_num(col)
                caja_texto.setText(eval(switch['num']) + info)
                df_num, datos = Analisis.cadena_a_numero(cols=[col], modo='columna')
                self.cargar_dataframe(df_num, muestra_df)

        def boton_err():
            col = form_cols.currentText()
            if col != 'Elige una columna':
                df_num = Analisis.cadena_a_numero(modo='num')
                df_err = Analisis.limpiar_errores(df=df_num)
                self.cargar_dataframe(df_err, muestra_df)
                info = Info.info_datos_noerr(col)
                caja_texto.setText(eval(switch['err']) + info)

        if nom == 'num':
            btn_arreglar.setText(u"Transformar datos")
            btn_arreglar.clicked.connect(boton_transf)

        elif nom == 'err':
            btn_arreglar.setText(u"Eliminar errores")
            btn_arreglar.clicked.connect(boton_err)


        form_layout.addWidget(form_cols)
        form_layout.addWidget(btn_arreglar)
        form_layout.addStretch()
        layout_izq.addLayout(form_layout)
        layout_izq.addLayout(doc_layout)
        layout_pest.addLayout(layout_izq)
        df_layout.addWidget(df_label)
        df_layout.addWidget(muestra_df)
        layout_pest.addLayout(df_layout)
        if nom == 'num':
            layout_pest.setStretch(0,9)
            layout_pest.setStretch(1,1)
        elif nom == 'err':
            layout_pest.setStretch(0,65)
            layout_pest.setStretch(1,35)
        pestaña.setLayout(layout_pest)

        return pestaña
    
    def crear_pest_graf(self):

        # Creamos todos los widgets y layouts
        pestaña = QWidget()
        layout_pest = QVBoxLayout()
        layout_form = QHBoxLayout()
        form_cols = QComboBox()
        btn_mostrar = QPushButton('Generar gráfica')
        figura = Figure()
        area_graf = FigureCanvas(figura)
        btn_seguir = QPushButton("Ir a creación del modelo ➢")

        df_num = Analisis.cadena_a_numero()
        columnas = [col for col in df_num.columns if col != 'id']
        form_cols.addItems(['Elige una columna'] + columnas)

        def btn_graf():
            col =  form_cols.currentText()
            if col != 'Elige una columna':
                generar_grafica(col)

        btn_mostrar.clicked.connect(btn_graf)

        btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        btn_seguir.setMinimumHeight(40)
        btn_seguir.clicked.connect(self.ir_a_modelo)
        btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

    
        def generar_grafica(col):
            # Limpiamos figura anterior
            figura.clear()

            # Hacemos llamada según la columna
            if col != 'hospitalizacion':
                Eda.cols_num(figura, col)
            else:
                Eda.col_hosp(figura)

            # Actualizamos el lienzo
            area_graf.draw()

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
    enviar_modelo = pyqtSignal(object)
        
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.threadpools = dict()
        self.init_ui()

    def init_ui(self):

        self.layout_principal = QVBoxLayout()

        self.etiqueta_titulo = QLabel("Selección del modelo")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        self.pestañas = QTabWidget()
        self.reglog = self.crear_pest("reglog")
        self.bosque = self.crear_pest("bosque")
        self.xgb = self.crear_pest("xgb")
        self.pestañas.addTab(self.reglog, u"Regresión Logística")
        self.pestañas.addTab(self.bosque, u"Bosque aleatorio")
        self.pestañas.addTab(self.xgb, u"Aumento Extremo del Gradiente")
        self.modelos = {}

        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addWidget(self.pestañas)
        self.setLayout(self.layout_principal)

    def crear_pest(self, nom: str):

        self.threadpools[nom] = QThreadPool()
        pestaña = QWidget()
        layout_pest = QHBoxLayout()
        layout_izq = QVBoxLayout()
        params_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()
        form_layout = QVBoxLayout()
        modelo_layout = QVBoxLayout()
        modelo_label = QLabel()
        barra_progreso = QProgressBar()
        figura = Figure()
        repr_modelo = FigureCanvas(figura)
        caja_texto = QLabel()
        area_doc = QScrollArea()
        doc_layout = QHBoxLayout()
        btn_crear = QPushButton()
        btn_optim = QPushButton()
        btn_seguir = QPushButton("Continuar con este modelo ➢")

        barra_progreso.setHidden(True)

        btn_seguir.setHidden(True)
        btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        btn_seguir.setMinimumHeight(40)
        btn_seguir.clicked.connect(lambda: self.ir_a_evaluacion(self.modelos[nom]))
        btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        btn_crear.setStyleSheet(u"background-color: #68c5d8;")

        btn_optim.setStyleSheet(u"background-color: #68c5d8;")
        btn_optim.setText(u"Crear modelo optimizado con validación cruzada")

        params_layout, parametros = self.crear_combos(params_layout, nom)

        switch = {"reglog":"Textos.modelo_reglog()",
                    "bosque":"Textos.modelo_bosque()",
                    "xgb":"Textos.modelo_xgb()"}

        caja_texto.setText(eval(switch[nom]))
        caja_texto.setWordWrap(True)
        caja_texto.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        caja_texto.setFont(QFont("Noto Serif", 14))
        caja_texto.setStyleSheet(u"padding: 15px;"
                                      "background-color:#777777;"
                                      "color:#ffffff;")

        area_doc.setWidgetResizable(True)
        area_doc.setWidget(caja_texto)
        area_doc.setFrameShape(QFrame.Box)
        area_doc.setFrameShadow(QFrame.Raised)
        area_doc.setLineWidth(4)

        doc_layout.addWidget(area_doc)

        control_entrenamiento = ControlEntrenamiento()


        def boton_modelo(nom: str, gcsv: bool = False):
            barra_progreso.setHidden(False)
            barra_progreso.setValue(0)

            if gcsv:
                btn_optim.setEnabled(False)
                btn_optim.setStyleSheet(u"background-color: #00b300;")
                btn_crear.setStyleSheet(u"background-color: #68c5d8;")
                print('creando modelo gscv')
                trabajador = Trabajador(Modelo.gs_cv, nom, objeto_control=control_entrenamiento)

                trabajador.señales.progreso.connect(barra_progreso.setValue)
                trabajador.señales.terminado.connect(terminar_entrenamiento)
                trabajador.señales.error.connect(error_entrenamiento)

                self.threadpools[nom].start(trabajador)

            else:
                btn_crear.setEnabled(False)
                btn_crear.setStyleSheet(u"background-color: #00b300;")
                btn_optim.setStyleSheet(u"background-color: #68c5d8;")
                btn_crear.setEnabled(False)

                params = []
                for k, v in parametros.items():
                    params.append(v.currentText())
                
                if nom == 'reglog':
                    control_entrenamiento.total_pasos = int(parametros['max_iter'].currentText())
                    trabajador = Trabajador(Modelo.reglog, params, objeto_control=control_entrenamiento)
                    trabajador.señales.progreso.connect(barra_progreso.setValue)

                elif nom == 'bosque':
                    control_entrenamiento.total_pasos = int(parametros['n_estimators'].currentText())
                    trabajador = Trabajador(Modelo.bosque, *params, objeto_control=control_entrenamiento)

                elif nom == 'xgb':
                    control_entrenamiento.total_pasos = int(parametros['n_estimators'].currentText())
                    trabajador = Trabajador(Modelo.xgb, *params, objeto_control=control_entrenamiento)

                trabajador.señales.progreso.connect(barra_progreso.setValue)
                trabajador.señales.terminado.connect(terminar_entrenamiento)
                trabajador.señales.error.connect(error_entrenamiento)

                self.threadpools[nom].start(trabajador)

        if nom == 'reglog':
            modelo_label.setText("Modelo de Regresión Logística")
            btn_crear.setText(u"Crear modelo de Regresión Logística")
            btn_crear.clicked.connect(lambda: boton_modelo(nom))

            btn_optim.clicked.connect(lambda: boton_modelo(nom, True))

        elif nom == 'bosque':
            modelo_label.setText("Modelo de Bosque Aleatorio")
            btn_crear.setText(u"Crear modelo de Bosque Aleatorio")
            btn_crear.clicked.connect(lambda: boton_modelo(nom))

            btn_optim.clicked.connect(lambda: boton_modelo(nom, True))

        elif nom == 'xgb':
            modelo_label.setText("Modelo de Incremento Extremo del Gradiente")
            btn_crear.setText(u"Crear modelo XGB")
            btn_crear.clicked.connect(lambda: boton_modelo(nom))

            btn_optim.clicked.connect(lambda: boton_modelo(nom, True))

        def generar_grafica(modelo, X, y):
            # Limpiamos figura anterior
            figura.clear()
            ax = figura.add_subplot(111)

            y_pred = modelo['modelo'].predict(X)
            GrafModelo.graf_reglog(y, y_pred, ax)


            # Actualizamos el lienzo
            repr_modelo.draw()


        def terminar_entrenamiento(modelo):
            self.modelos[nom] = modelo
            print(self.modelos)
            X_test = modelo['X_test']
            y_test = modelo['y_test']

            generar_grafica(self.modelos[nom], X_test, y_test)

            btn_seguir.setHidden(False)
            btn_crear.setEnabled(True)
            btn_optim.setEnabled(True)
            barra_progreso.setHidden(True)

            caja_texto.setText(eval(switch[nom]) + str(modelo['modelo']))
        
        def error_entrenamiento(mensaje):
            QMessageBox.critical(self, 'Error de entrenamiento: ', mensaje)
            barra_progreso.setHidden(True)
            btn_crear.setEnabled(True)

        btn_layout.addStretch()
        btn_layout.addWidget(btn_crear)
        btn_layout.addWidget(btn_optim)
        btn_layout.addStretch()
        form_layout.addLayout(params_layout)
        form_layout.addLayout(btn_layout)
        layout_izq.addLayout(form_layout)
        layout_izq.addLayout(doc_layout)
        layout_pest.addLayout(layout_izq)
        modelo_layout.addWidget(modelo_label, stretch=1)
        modelo_layout.addWidget(barra_progreso)
        modelo_layout.addWidget(repr_modelo, stretch=9)
        modelo_layout.addWidget(btn_seguir)
        layout_pest.addLayout(modelo_layout)
        layout_pest.setStretch(0,58)
        layout_pest.setStretch(1,42)
        pestaña.setLayout(layout_pest)

        return pestaña
    
    def crear_combos(self, params_layout, nom):
        params = Modelo.params(nom)
        parametros = {}
        params_layout.addStretch()
        for k, v in params.items():
            form_layout = QVBoxLayout()
            titulo = QLabel(k.capitalize())

            combo = QComboBox()
            combo.addItems(v)
            parametros[k] = combo

            form_layout.addWidget(titulo)
            form_layout.addWidget(combo)
            params_layout.addLayout(form_layout)
        params_layout.addStretch()
        return params_layout, parametros
    
    def ir_a_evaluacion(self, modelo):
        self.enviar_modelo.emit(modelo)

        self.widget_apilado.setCurrentIndex(4)

class EvaluacionModelo(QWidget):
    """Página de evaluación del modelo"""
    modelo = None
    def __init__(self, widget_apilado):
        super().__init__()
        self.widget_apilado = widget_apilado
        self.init_ui()

    def recibir_modelo(self, modelo):
        self.modelo = modelo
        print(self.modelo)
        self.label.setText(f'{self.modelo["modelo"]} recibido')
        if self.modelo:
            QMessageBox.information(self, 'Envío exitoso', f'{self.modelo["modelo"]} recibido')

    def init_ui(self):
        '''Estructura más sencilla:
        - VBox con título 
        - HBox con la info:
            · Izda: VBox con KPIs y texto
                + Arriba: (KPIs -> (HBox -> (VBox -> (título + métrica))))
                    -> accuracy, precision, recall, F1
                + Abajo: Descripción QScrollArea
            · Dcha: VBox con gráficas
                if reglog:
                    ROC-AUC
                    Matriz de confusión
                    Log loss
                    
                if bosque:
                    ROC-AUC
                    Matriz de confusión
                    importancia de caracteristicas

                if xgb:
                    ROC
                    Matriz de confusión
                    importancia de caracteristicas'''
        self.layout_principal = QVBoxLayout()
        self.etiqueta_titulo = QLabel(f"Evaluación del modelo")
        self.etiqueta_titulo.setGeometry(QRect(165, 50, 850, 100))
        self.fuente_titulo = QFont("OCR A Extended", 72, 50)
        self.etiqueta_titulo.setFont(self.fuente_titulo)
        self.etiqueta_titulo.setStyleSheet(u"background-color: rgb(0, 255, 255);""")
        self.etiqueta_titulo.setFrameShape(QFrame.Panel)
        self.etiqueta_titulo.setFrameShadow(QFrame.Raised)
        self.etiqueta_titulo.setLineWidth(5)
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)

        self.label = QLabel(f"Modelo no recibido")
        self.label.setFont(QFont("Arial", 16))
        self.label.setAlignment(Qt.AlignCenter)
        self.btn_seguir = QPushButton("Ir a gráficas e informes ➢")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_graficos)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")

        self.layout_principal.addWidget(self.etiqueta_titulo)
        self.layout_principal.addWidget(self.label)
        self.layout_principal.addWidget(self.btn_seguir)
        self.setLayout(self.layout_principal)

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
        self.btn_seguir = QPushButton("Volver al inicio ⮌")
        self.btn_seguir.setFont(QFont("Eras Medium ITC", 12))
        self.btn_seguir.setMinimumHeight(40)
        self.btn_seguir.clicked.connect(self.ir_a_datos)
        self.btn_seguir.setStyleSheet(u"background-color: #a82626;""color: #ffcb53;")
        layout.addWidget(self.btn_seguir)
        self.setLayout(layout)

    def ir_a_datos(self):
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
        self.informe_graficos = InformeGraficos(self.widget_apilado)
        
        self.widget_apilado.addWidget(self.pagina_bienvenida)  # índice 0
        self.widget_apilado.addWidget(self.datos)              # índice 1
        self.widget_apilado.addWidget(self.pagina_eda)         # índice 2
        self.widget_apilado.addWidget(self.creacion_modelo)    # índice 3
        self.widget_apilado.addWidget(self.evaluacion_modelo)  # índice 4
        self.widget_apilado.addWidget(self.informe_graficos)   # índice 5
        
        self.creacion_modelo.enviar_modelo.connect(self.evaluacion_modelo.recibir_modelo)

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