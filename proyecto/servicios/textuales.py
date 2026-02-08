from servicios.analisis import Leer_Datos, Analisis

class Textos:
    def bienvenida() -> str:
        """Devuelve el texto de la página de bienvenida de la aplicación."""
        texto = u'''Bienvenido a este ejercicio de final de curso de Machine Learning con Deusto, realizado por Darío Zoreda.
El objetivo es crear y analizar un conjunto de datos ficticios relativos a la salud de un número de personas. 

De manera aleatoria, crearemos un número n de pacientes ficticios, con un ID, y datos de edad, peso, altura, presión arterial y glucosa.
Dado que la intención del ejercicio es ponernos las cosas un poquito complicadas, crearé esos datos como cadenas de caracteres, con el número y su unidad, y en distintas unidades de medida, cuando sea posible.
Una vez creados estos datos, crearé la columna "hospitalización", que será la columna objetivo a predecir por el modelo.
Finalmente, introduciré errores en la base de datos: números negativos, 0 y NaN.

Habiendo ya creado los datos, pasaremos al análisis: primero, un EDA básico.
Veremos cómo transformo las columnas de cadenas de caracteres a números, y cómo homogeneizo las unidades.
Entonces, pasaremos a ver las características de los datos, los errores y cómo los corregiré.

Ya tendremos los datos listos para entrenar un modelo.
Se ofrecen tres opciones a probar: árbol de decisión, bosque aleatorio y potenciación extrema del gradiente. Asimismo, se ofrece la posibilidad de optimizarlos mediante GridSearchCV (validación cruzada en cuadrícula).
Según el modelo elegido, se mostrará una gráfica que represente su capacidad predictiva.
Ahora vamos a evaluar el rendimiento del modelo, con una matriz de confusión, la curva ROC-AUC y las puntuaciones de precisión y recuperación.

Finalmente, veremos una gráfica representativa del modelo, y un informe basado en sus métricas.'''
        return texto
    
    def creacion() -> str:
        """Devuelve el texto de explicación de la creación de los datos."""
        texto = u'''En este paso, crearemos la base de datos.
Primero, estableceré unos rangos de peligro basados en lo que la ciencia médica dice, para el IMC, la presión arterial y la glucosa, y todo ello relacionado con unos rangos de edad.
Para agregar complejidad a los datos, creé las columnas de altura, peso y glucosa con dos tipos de unidad de medida cada una, distribuida de manera aleatoria.
Para asegurar una distribución realista, utilizaré una distribución normal o de campana de Gauss, estableciendo una desviación estándar tal que produzca datos extremos más o menos realistas, que nos permitan crear esos datapoints en los que el paciente debe ser hospitalizado.
El siguiente paso es revisar si se cumple alguna condición para la hospitalización (con una basta), y agregar la columna correspondiente.
Una vez los datos están completos y coherentes, agregamos errores: de manera aleatoria, se cambian datos por 0, NaN o se cambian de signo a negativo.
Finalmente, guardamos los datos en un archivo de formato csv: datos_forjados.csv
P.D.: invito a quien lo use a jugar con la proporción de pacientes hospitalizados o no, ya que produce efectos interesantes en el desempeño de los modelos.'''
        return texto
    
    def transf_num() -> str:
        """Devuelve el texto de explicación de la transformación a numérico de los datos."""
        texto = u'''Debido al formato en que hemos recibido los datos, hay varias columnas que son de tipo "string", y por tanto, incompatibles con un modelo de clasificación o regresión.
Además, hay columnas con más de un tipo de unidad, lo cual es un gran problema, ya que al tener diferentes escalas, desvirtuarían mucho la capacidad predictiva del modelo.
Por tanto, en el backend realizaremos dos operaciones fundamentales:
- Quitar el nombre de la unidad, dejando sólo el número.
- Convertir el número a una unidad estándar, y cambiar su tipo a float.

Con esto, tendremos un DataFrame compuesto de 7 características, 6 de ellas numéricas y una categórica (hospitalización)'''
        return texto
    
    def trat_err() -> str:
        """Devuelve el texto de explicación del tratamiento de errores de los datos."""
        texto = '''Ahora pasamos a eliminar los errores que introdujimos en los datos previamente.
Como no sabemos cuál era el dato original, he decidido que los ceros y NaN serán sustituidos por la media aritmética, y todos los datos que estén en signo negativo serán convertidos en valor absoluto usando la función abs().

Además, durante la creación de datos introdujimos como condición de hospitalización el IMC, pero es un dato que no existe en nuestra base de datos de manera explícita.
Durante la creación de este programa, probé a crear los modelos con los datos tal cual están, y su sensibilidad se veía muy reducida, cosa que es crítica para un problema como este, ya que dejaría a muchas personas necesitadas sin hospitalización.
Pero al crear e introducir la columna IMC, todas las métricas de los modelos subieron mucho, hasta una nota sobresaliente. Por ello, decidí introducirla en este paso. 
También eliminaremos la columna "id" para evitar confundir al modelo.

Con estas operaciones, los datos ya están listos para ser utilizados en el entrenamiento de nuestro modelo.

A continuación, se muestra un recuento de los errores en la columna seleccionada, y el DataFrame resultado de la limpieza:'''
        return texto
    
    def modelo_reglog() -> str:
        """Devuelve el texto explicativo del modelo de regresión logística."""
        ecuacion_logit = u"ln(P / (1 - P)) = β₀ + β₁X₁ + ... + βₙXₙ" 
        ecuacion_sigmoide = u"P = 1 / (1 + e^-(β₀ + β₁X₁ + ... + βₙXₙ))"
        texto = f'''<h2>Modelo de Regresión Logística</h2>
<p>Este es el modelo más sencillo que vamos a crear. No es el más recomendado, pero es un buen comienzo para empezar a analizar y entender nuestros datos.
Es un modelo basado en la función logística o sigmoide, que transforma una combinación lineal de variables en una probabilidad.
La ecuación del modelo se crea al igualar la ecuación Logit a una combinación lineal de los predictores (X):<br>
<i>{ecuacion_logit}</i></p>

<p>Finalmente, obtenemos la probabilidad directa (P) a partir de la ecuación anterior.
Para ello, se despeja la fórmula resultando en la función logística o inversa del logit:<br>
<i>{ecuacion_sigmoide}</i></p>

<p>Con esto, obtenemos un rango de probabilidad entre 0 y 1, y nuestro modelo intentará asignar una de las dos categorías objetivo a cada entrada (sí o no).
Como podemos ver en la gráfica de la derecha, el ajuste a los datos reales bastante bajo.</p>

<p>En la página siguiente veremos los datos de evaluación del modelo.</p>

Parámetros:
<ul>
<li><u><b>Penalty</b></u>: es la regularización que se aplica al modelo, que castiga los coeficientes demasiado grandes para evitar el overfitting. Opciones:</li>
    <ul>
    <li><i>l2</i>: la llamada técnica <i>Ridge</i>, es la predeterminada, y penaliza la suma de los cuadrados de los coeficientes.</li>
    <li><i>l1</i>: conocida como <i>Lasso</i>, penaliza el valor absoluto de los coeficientes, pudiendo llevar algunos valores a 0, y actuando así como una herramienta de selección de variables.</li>
    <li><i>None</i>: no aplica ninguna regularización</li>
    </ul>
<li><u><b>C</b></u>: controla cómo de fuerte es la penalización aplicada. Consiste en un número de tipo "float" positivo.</li>
<ul>
    <li>Valor bajo: presentará una regularización fuerte. Se evita el overfitting, pero el modelo podría perder capacidad de ajuste.</li>
    <li>Valor alto: regularización débil, que permite mayor ajuste a los datos de entrenamiento, y perjudicando la capacidad predictiva del modelo.</li>
</ul>
<li><u><b>Solver</b></u>: se trata del algoritmo que encuentra los mejores coeficientes para el modelo y minimiza la función de pérdida. Las opciones son:
<ul>
    <li><i>newton-cg</i>: o Newton Conjugate Gradient, usa información de la curvatura de la función de pérdida para encontrar el mínimo. Soporta nativamente la clasificación de más de dos clases. Sólo es compatible con regularización l2 o ninguna. Es bastante robusto, y converge en menos iteraciones que otros métodos, aunque cada iteración es más costosa. Se recomienda usarlo  cuando el tamaño de los datos es de pequeño a mediano.</li>
    <li><i>liblinear</i>: utiliza una técnica de descenso de coordenadas. Es muy eficiente con datasets pequeños con una alta dimensionalidad. Soporta tanto regularización l1 como l2, pero no elasticnet.</li>
    <li><i>saga</i>: se le considera el algoritmo de optimización más versátil y avanzado dentro de los modelos lineales de sklearn. Utiliza una técnica de gradiente estocástico promediado, utilizando subconjuntos de datos que usa para actualizar los pesos del modelo, y acelerando así la convergencia. Soporta todas las penalizaciones. Es muy rápido incluso con datasets masivos.</li>
</ul>
<li><u><b>Max iter</b></u>: indica el número máximo de iteraciones que podrá ejecutar el modelo para buscar la convergencia. Si es muy bajo, los coeficientes no serán los más ideales y se reducirá la precisión del modelo.</li>
</ul>'''
        return texto

    def modelo_bosque() -> str:
        """Devuelve el texto explicativo del modelo de bosque aleatorio."""
        texto = '''<h2>Modelo de Bosque Aleatorio</h2>
<p>Es el modelo más típicamente usado para este tipo de problema, y el que se recomendó en la documentación del proyecto.
Se trata de un modelo de aprendizaje supervisado que combina varios árboles de decisión (los que se definan en el parámetro <i>n_estimators</i>) para obtener un resultado más consistente y preciso.
Utiliza una técnica llamada <i>bagging</i>, que consiste en entrenar cada árbol con un subconjunto aleatorio de los datos y de las características.
Una vez entrenados los árboles, se realiza una predicción final basada en el promedio (si el problema es de regresión) o en la mayoría de votos (si es de clasificación, como el que nos ocupa).</p>

<p>Es un tipo de modelo bastante robusto y versátil, y como se puede ver en la gráfica, se ajusta mejor a los datos que un modelo de regresión logística.</p>

Parámetros:
<ul>
<li><u><b>N estimators</b></u>: indica el número total de árboles en el bosque. A mayor número, será un modelo más estable y potente, pero requerirá más tiempo de cómputo y memoria.</li>
<li><u><b>Max depth</b></u>: Define la profundidad máxima de cada árbol (la distancia entre el nodo raíz y la hoja más lejana). Si es muy alto, lleva al sobreajuste; si es muy bajo, al hipoajuste.</li>
<li><u><b>Min samples split</b></u>: es el número mínimo de muestrar que debe tener un nodo para que se le permita dividirse en dos nodos hijos. Aumentarlo evita que el modelo cree reglas basadas en pocos datos, reduciendo el sobreajuste.</li>
<li><u><b>Min samples leaf</b></u>: es el número mínimo de muestras que debe presentar un nodo terminal u hoja. Aumentarlo evita que se creen hojas demasiado específicas, reduciendo el sobreajuste.</li>
<li><u><b>Max features</b></u>: indica la cantidad máxima de características que el algoritmo considera al buscar la mejor división en cada nodo. Introduce aleatoriedad, ayudando a crear árboles más diversos.</li>
<li><u><b>Bootstrap</b></u>: indica si se usarán muestras aleatorias con reemplazo para entrenar cada árbol. Por defecto está activada, pero desactivarla reduce la generalización del bosque.</li>
</ul>'''
        return texto

    def modelo_xgb() -> str:
        """Devuelve el texto explicativo del modelo de potenciación extrema del gradiente."""
        texto = '''<h2>Modelo Potenciación Extrema del Gradiente</h2>
<p>El <i>Extreme Gradient Boosting</i> es una versión optimizada del algoritmo de <i>Gradient Boosting</i>, que, al igual que en el modelo de Bosque Aleatorio, funciona mediante árboles de decisión, pero con una diferencia clave:
en este modelo, los árboles se construyen de manera secuencial, de tal manera que cada nuevo árbol intentará corregir los errores del anterior.</p>
<p>Es un modelo bastante preciso y veloz, ya que optimiza el uso de la CPU para hacer procesamiento en paralelo. </p>
Parámetros:
<ul>
<li><u><b>n estimators</b></u>: es el número total de árboles que se construirán. Si es muy alto, podría sobreajustar. En este caso, hemos añadido el parámetro <i>early stopping</i> para detener el modelo cuando el error de validación deja de bajar.</li>
<li><u><b>Learning rate</b></u>: determina el tamaño del paso que se da en cada iteración. Un valor bajo aumenta la robustez del modelo pero requiere más árboles.</li>
<li><u><b>Max depth</b></u>: controla la complejidad del modelo, limitando la profundidad de los árboles. Si es muy alta, captura interacciones complejas, pero aumenta la tendencia al sobreajuste.</li>
<li><u><b>Min child weight</b></u>: define la suma mínima de pesos necesaria para poder definir un nodo como nodo hijo. Aumentarlo evita que el algoritmo cree nodos demasiado específicos o debidos al ruido.</li>
<li><u><b>Subsample</b></u>: es la fracción de los datos de entrenamiento que se seleccionan para construir cada árbol. Cuanto menor sea, más aleatoriedad añadirá.</li>
<li><u><b>Colsample bytree</b></u>: es el porcentaje de características que se seleccionan para entrenar cada árbol. Al igual que el anterior, añade aleatoriedad.</li>
<li><u><b>Reg alpha</b></u>: regularización equivalente a <i>Lasso</i>: penaliza en base a los valores absolutos de los pesos, pudiendo reducir los pesos de las menos importantes a cero.</li>
<li><u><b>Reg lambda</b></u>: regularización equivalente a <i>Ridge</i>: penaliza en base al cuadrado de los pesos, aumentando la estabilidad del modelo al reducir la varianza.</li>
</ul>'''
        return texto
    
class Info:
    from pandas import DataFrame
    def extraer_info(info: list) -> tuple[list]:
        """
        Devuelve el nombre de la columna, los valores no nulos y el tipo de datos de una llamada a Dataframe.info() en forma de tres listas.
        
        :param info: Lista de cadenas de texto obtenida de la función crear_info().
        :type info: list
        :return: Tupla que contiene tres listas: nombre de la columna, datos no nulos y tipo de dato.
        :rtype: tuple[list]
        """
        import re
        col_nom = []
        non_null = []
        dtype = []
        # Creamos un patrón con los grupos que nos interesa filtrar
        patron = r'\s+\d+\s+(\w+)\s+(\d+)\s+non-null\s+(\w+)'
        for palabra in info:
            grupos = re.search(patron, palabra)
            if grupos:
                re_col = grupos.group(1)
                re_null = grupos.group(2)
                re_dtype = grupos.group(3)

                col_nom.append(re_col)
                non_null.append(re_null)
                dtype.append(re_dtype)
            else:
                continue
        return col_nom, non_null, dtype
    
    def crear_info(df: DataFrame) -> list[str]:
        """
        Recoge el texto de una llamada a Dataframe.info() y lo devuelve.
        
        :param df: DataFrame del que extraer la información.
        :type df: DataFrame
        :return: Lista de cadenas de texto, cada una de las cuales es una línea impresa por df.info().
        :rtype: list[str]
        """
        import io
        # Creamos un buffer para poder recoger la información del método .info()
        buffer = io.StringIO()
        df.info(buf=buffer, memory_usage=False)
        # Lo dividimos por líneas
        lista_texto = buffer.getvalue().split('\n')
        return lista_texto

    def extraer_descripcion_columna(df: DataFrame) -> list:
        """Devuelve los contenidos de Dataframe.describe() como una lista de cadenas de texto."""
        info = df.describe()
        col = info.columns
        iterador = info[col].items()

        # Iteramos sobre el iterador y agregamos el contenido a la lista
        descripcion = []
        for label, content in iterador:
            for linea in content:
                descripcion.append(linea)
        return descripcion

    def info_datos_originales(url: str = 'datos_forjados.csv') -> str:
        """
        Abre los datos originales y 
        devuelve un resumen de las características en texto.
        """
        # Leemos el archivo csv para crear un Dataframe
        df = Leer_Datos.abrir_csv(url)

        lista_texto = Info.crear_info(df)

        # Extraemos las listas de datos que necesitamos y se los aplicamos a un texto
        col_nom, non_null, dtype = Info.extraer_info(lista_texto)
        texto = '''\nCantidad de datos no nulos y tipo de dato por columna:\n'''
        for n, col in enumerate(col_nom):
            texto_col = f'''Columna "{col}":
    - Datos no nulos: {non_null[n]}
    - Datos nulos: {len(df) - int(non_null[n])}
    - Tipo de dato: {dtype[n]}
********************************
'''
        # Unimos los textos y los devolvemos 
            texto += texto_col
        return texto
    
    def info_datos_num(col: str, url: str = 'datos_forjados.csv') -> str:
        """
        Abre los datos, los convierte a numérico y extrae la información de ellos.
        
        :param col: Columna a inspeccionar.
        :type col: str
        :param url: Nombre del archivo de datos.
        :type url: str
        :return: Texto formateado con las características de la columna seleccionada.
        :rtype: str
        """
        # Extraemos los datos
        df = Leer_Datos.abrir_csv(url)
        df_num = Analisis.cadena_a_numero(df=df, cols=[col], modo='columna')

        # Creamos la info como una lista
        lista_texto = Info.crear_info(df_num)

        # Extraemos la info y la descripción
        col_nom, non_null, dtype = Info.extraer_info(lista_texto)
        descripcion = Info.extraer_descripcion_columna(df_num)
        # Se lo aplicamos al texto
        texto = f'''
Al realizar el tratamiento de los datos, vamos viendo el progreso en la coherencia de estos:

Cantidad de datos y tipo de dato en {col_nom[0]}:
    - Datos no nulos: {non_null[0]}
    - Datos nulos: {len(df) - int(non_null[0])}
    - Tipo de dato: {dtype[0]}

Características de la columna:
    - Media aritmética: {descripcion[1]:.2f}
    - Desviación estándar: {descripcion[2]:.2f}
    - Valor mínimo: {descripcion[3]}
    - Mediana: {descripcion[5]}
    - Valor máximo: {descripcion[7]}

'''

        return texto
    
    def info_datos_noerr(col: str, url: str = 'datos_forjados.csv') -> str:
        """
        Analiza la columna seleccionada para buscar errores y crea un texto formateado con el resultado.
        
        :param col: Columna a inspeccionar.
        :type col: str
        :param url: Nombre del archivo de origen de los datos.
        :type url: str
        :return: Texto con el recuento de errores de la columna seleccionada.
        :rtype: str
        """
        # Diccionario con las columnas nuevas y las antiguas
        columnas = {'presion_sistolica':'presion_arterial',
                    'glucosa_mg_dL':'glucosa'}
        df = Leer_Datos.abrir_csv(url) # Leemos los datos
        if col in columnas.keys(): # Analizamos la columna original
            df_num = Analisis.cadena_a_numero(df=df, cols=[columnas[col]], modo='columna')
            df_noerr = Analisis.limpiar_errores(df=df_num, cols=col, modo='columna')
        elif col == 'hospitalizacion': # Hospitalización está siempre libre de errores
            df_noerr = ('', (0,0,0))
        else: # No cambia (edad) o no hay original (IMC)
            df_num = Analisis.cadena_a_numero(cols=[col], modo='columna')
            df_noerr = Analisis.limpiar_errores(df=df_num, cols=col, modo='columna')
        
        texto = f'''
Recuento de errores en la columna {col}:
    - NaN: {df_noerr[1][0]}
    - 0: {df_noerr[1][1]}
    - Negativos: {df_noerr[1][2]}'''
        return texto

class Informe:
    def eval_kpis(kpis: dict[str, float]) -> str:
        """
        Crea y devuelve un texto en función del desempaño del modelo en base a cuatro métricas: exactitud, precisión, sensibilidad y F1.
        
        :param kpis: Diccionario que contiene las cuatro métricas.
        :type kpis: dict[str, float]
        :return: Texto formateado con la evaluación.
        :rtype: str
        """
        texto = '<p>Las cuatro métricas que vamos a explicar a continuación son las más utilizadas para evaluar modelos de clasificación, ya que nos dan una idea general del desempeño, puntos fuertes y débiles del modelo.</p><ul>'

        # Exactitud
        texto_exac = '<li><p>La exactitud nos indica cuál es el porcentaje de aciertos sobre el total de predicciones correctas. Es una medida general de la <b>capacidad de predicción</b> del modelo.</p>'
        exac = kpis['Exactitud']
        if exac < 0.6:
            texto_exac += f'<p>Con un {exac:.2%}, la exactitud del modelo es <u><b>muy pobre</b></u>, similar al azar. El modelo no es fiable.</p></li>'
        elif exac < 0.8:
            texto_exac += f'<p>Con un {exac:.2%}, la exactitud del modelo es <u><b>moderada</b></u>, con utilidad en fases iniciales. El modelo no es útil para triaje serio.</p></li>'
        elif exac < 1:
            texto_exac += f'<p>Con un {exac:.2%}, la exactitud del modelo es <u><b>muy alta</b></u>. El modelo es de alta calidad.</p></li>'
        else:
            texto_exac += f'<p>Con un {exac:.2%}, la exactitud del modelo es <u><b>perfecta</b></u>, con riesgo de sobreajuste.</p></li>'
        texto += texto_exac
        
        # Precisión
        texto_prec = '<li><p>La precisión nos muestra los aciertos a la hora de marcar un dato como positivo, sobre el total de datos marcados como positivo. Mide el <b>entusiasmo</b> del modelo para marcar como positivos datos que realmente son negativos.</p></li>'
        prec = kpis['Precisión']
        if prec < 0.6:
            texto_prec += f'<p>Con un {prec:.2%}, la precisión del modelo es <u><b>muy baja</u></b>, generando un exceso de falsos positivos.</p></li>'
        elif prec < 0.8:
            texto_prec += f'<p>Con un {prec:.2%}, la precisión del modelo es <u><b>aceptable</u></b>: está lejos de ser perfecto, pero es funcional.</p></li>'
        elif prec < 1:
            texto_prec += f'<p>Con un {prec:.2%}, la precisión del modelo es <u><b>alta</u></b>, lo que asegura un mínimo de falsos positivos.</p></li>'
        else:
            texto_prec += f'<p>Con un {prec:.2%}, la precisión del modelo es <u><b>perfecta</u></b>: no hay falsos positivos.</p></li>'
        texto += texto_prec
        
        # Sensibilidad
        texto_sens = '<li><p>La sensibilidad nos indica cuántos aciertos se cometieron al intentar detectar positivos, respecto a los datos que quedaron marcados como negativos pero no lo eran. Podría decirse que mide la <b>precaución</b> del modelo a la hora de afirmar que un dato es positivo.</p>'
        sens = kpis['Sensibilidad']
        if sens < 0.6:
            texto_sens += f'<p>Con un {sens:.2%}, la sensibilidad del modelo es <u><b>muy baja</u></b>, generando un exceso de falsos negativos, lo cual es peligroso, ya que ignora potenciales pacientes graves.</p></li>'
        elif sens < 0.8:
            texto_sens += f'<p>Con un {sens:.2%}, la sensibilidad del modelo es <u><b>moderada</u></b>, generando falsos negativos, lo cual es peligroso, ya que ignora potenciales pacientes graves.</p></li>'
        elif sens < 1:
            texto_sens += f'<p>Con un {sens:.2%}, la sensibilidad del modelo es <u><b>alta</u></b>, detectando la mayoría de pacientes necesitados de hospitalización.</p></li>'
        else:
            texto_sens += f'<p>Con un {sens:.2%}, la sensibilidad del modelo es <u><b>perfecta</u></b>, detectando todos los pacientes que necesitan hospitalización.</p></li>'
        texto += texto_sens
        
        # F1
        texto_f1 = '<li><p>La puntuación F1 resulta de la media armónica entre la precisión y la sensibilidad. Nos indica el <b>desempeño general</b> del modelo.</p>'
        f1 = kpis['F1']
        if f1 < 0.6:
            texto_f1 += f'<p>Con un {f1:.2%}, la capacidad de distinción del modelo es <u><b>nula</u></b>, confundiendo una clase con otra sin ningún criterio.</p></li>'
        elif f1 < 0.8:
            texto_f1 += f'<p>Con un {f1:.2%}, la capacidad de distinción del modelo es <u><b>aceptable</u></b>, existiendo bastante solapamiento entre ambos grupos.</p></li>'
        elif f1 < 1:
            texto_f1 += f'<p>Con un {f1:.2%}, la capacidad de distinción del modelo es <u><b>alta</u></b>, separando ambas clases sin problema.</p></li>'
        else:
            texto_f1 += f'<p>Con un {f1:.2%}, la capacidad de distinción del modelo es <u><b>perfecta</u></b>, separando las dos clases sin ninguna duda.</p></li>'
        texto += texto_f1

        return texto

    def eval_metricas(metricas: dict) -> str:
        """Evalúa las métricas y devuelve un texto acorde."""
        import math
        from pandas import DataFrame
        import re

        if 'log_losses' in metricas:
            log_loss = metricas['log_losses'][0]
            texto = f"""<li><p>La pérdida logarítmica o entropía cruzada binaria es la métrica principal para evaluar la capacidad de predecir probabilidades de un modelo de regresión logística.
Es una métrica que castiga la incertidumbre y el exceso de confianza al predecir erróneamente.</p>
<p>En el modelo actual, tenemos una pérdida logarítmica para ambas clases del {log_loss:.2%}."""
            excelente = ' Presenta una <u><b>alta confianza</b></u> en la respuesta correcta: es el escenario ideal.</p>'
            bueno = ' Presenta <u><b>bastante seguridad</b></u>, aunque no total: es un buen modelo, pero mejorable.</p>'
            dudoso = ' Presenta <u><b>incertidumbre</b></u>. Es un modelo mediocre, en el mejor de los casos.</p>'
            ambiguo = ' Presenta <u><b>indecisión</b></u>: el modelo no sabe distinguir entre las dos clases.</p>'
            incorrecto = ' El modelo es <u><b>incorrecto</b></u>: comete más errores que aciertos.</p>'
            rangos = [excelente, excelente, excelente, 
                      bueno, bueno, 
                      dudoso, dudoso, 
                      ambiguo, ambiguo, 
                      incorrecto, incorrecto]
            try:
                texto += rangos[int(math.floor(log_loss*10))]
            except IndexError:
                texto += rangos[10]
            texto += '</li>'

        elif 'importancia_carac' in metricas:
            texto = f"""<li><p>La importancia de características nos informa del peso de cada característica en el modelo a la hora de tomar decisiones y hacer predicciones.</p>
<p>El orden de importancia en este modelo es:</p><ol>"""
            importancia: DataFrame = metricas['importancia_carac'].sort_values(by='importancia', ascending=False).reset_index(drop=True)
            for dato in importancia.index:
                for n, i in enumerate(importancia.iloc[dato]):
                    if n % 2 == 0:
                        texto += f"<li>{i}: "
                    else:
                        texto += f"{i:.2%}</li>"
            texto += '</ol>'

            patron = r'IMC:\s(\d+\.\d+)'
            imc_patron = re.search(patron, texto)
            imc_cifra = float(imc_patron.group(1))
            if imc_cifra >= 50:
                texto += """<p><i>NOTA</i>: el IMC recibe una sobrerrepresentación en la importancia debido a cómo han sido fabricados los datos: al provenir de dos características aleatorias con distribución normal igual que el resto, se producen combinaciones extremas en ocasiones, lo que lleva a hospitalizaciones. Jugando con los rangos de generación de los datos, quizá se pueda mitigar o arreglar.</p>"""
            texto += '</li>'

        roc_auc = metricas['auc']
        texto_auc = f'''<li><p>La métrica <b>ROC-AUC</b> (<i>Receiver Operating Characteristic - Area Under the Curve</i>) se utiliza para comparar la tasa de falsos positivos con la de verdaderos positivos a lo largo de diferentes umbrales de clasificación, y así extraer la capacidad de diferenciación de clases del modelo, y por tanto, su capacidad predictiva.</p>
<p>La curva ideal estaría lo más alejada posible de la diagonal, formando un ángulo recto. La diagonal representa una incertidumbre total: las probabilidades de elegir una u otra clase son las mismas, el 50%.</p>
<p>En el caso que nos ocupa, la ROC-AUC es del <b>{roc_auc:.2%}</b>. '''
        if roc_auc < 0.6:
            texto_auc += 'El modelo <u><b>no tiene capacidad de discriminación o predicción</b></u>. Necesita un ajuste de hiperparámetros o una distribución más equitativa de las clases.</p>'
        elif roc_auc < 0.8:
            texto_auc += 'El modelo tiene una capacidad de distinción <u><b>aceptable</b></u>, pero aún hay solapamiento entre grupos.</p>'
        elif roc_auc < 1:
            texto_auc += 'El modelo tiene una <u><b>muy buena capacidad</b></u> de clasificación. Es un modelo casi ideal.'
        else:
            texto_auc += 'El modelo es <u><b>perfecto</b></u>: distingue entre ambas clases sin ninguna duda.'
        texto += texto_auc
        texto += '</li>'
        
        return texto
    
    def informe_eval(nom: str, metricas: dict, kpis: dict) -> str:
        """
        Muestra una explicación de a qué corresponden los rangos observados en los KPIs.
        
        :param nom: Nombre del tipo de modelo a evaluar.
        :type nom: str
        :param metricas: Description
        :type metricas: dict
        :param kpis: Description
        :type kpis: dict
        :return: Description
        :rtype: str
        """
        texto = f'''<h2>Informe de evaluación de {nom}</h2>
<p><h3>Métricas:</h3> <ol>{Informe.eval_metricas(metricas)}</ol></p>
<p><h3>Indicadores clave:</h3></p> {Informe.eval_kpis(kpis)}'''
        return texto

    def final(kpis: dict[str, float], metricas: dict) -> str:
        """
        Docstring for final
        
        :param kpis: Description
        :type kpis: dict[str, float]
        :param metricas: Description
        :type metricas: dict
        :return: Description
        :rtype: str
        """
        texto = ''
        exactitud = kpis['Exactitud']
        precision = kpis['Precisión']
        sensibilidad = kpis['Sensibilidad']
        f1 = kpis['F1']
        auc = metricas['auc']

        estrategia_sensibilidad = f'''<p>En problemas de clasificación como este, donde un falso negativo es muy peligroso, conviene maximizar la sensibilidad, que en este caso es del {sensibilidad:.2%}, mostrando un desbalance con la precisión, del {precision:.2%}. Algunas estrategias útiles son:
<ul><li>Ajuste del umbral de clasificación mediante hiperparámetros: bajarlo implica menos falsos negativos.</li>
<li>Balanceo de clases: si hay pocos casos de hospitalización, es posible que el modelo los ignore. En este programa, se pueden crear datos sintéticos con cualquier proporción entre las dos clases, pero si no fuera así, se podría asignar pesos a las clases o usar técnicas de remuestreo para añadir datos y rebalancear las clases.</li>
<li>Selección de algoritmo: XGBoost es el mejor, ya que podríamos definir funciones de pérdida que castiguen más los falsos negativos que los falsos positivos.</li></ul></p>'''
        
        estrategia_precision = f'''<p>La precisión es importante, ya que si es muy baja podría colapsar nuestro hospital con pacientes sanos, pero es menos crucial que la sensibilidad. En nuestro caso, con una precisión del {precision:.2%}, y una sensibilidad del {sensibilidad:.2%}, vemos un desequilibrio en favor de la sensibilidad. No es un gran problema, pero si queremos solucionarlo, hay varias estrategias:
<ul><li>Ajuste del umbral de clasificación mediante hiperparámetros: subirlo implica menos falsos positivos.</li>
<li>Regularización del modelo: utilizando regularización Ridge.</li>
<li>Balanceo de clases: si hay demasiados casos de hospitalización, el modelo podría aprender patrones inservibles de ellos.</li>
<li>Selección de algoritmo: XGBoost o Random Forest son los mejores modelos para evitar una precisión baja, ya que los datos atípicos no les afectan tanto.</li></ul></p>
'''
        def estrategia(texto, sensibilidad, precision):
            if sensibilidad * 1.2 < precision:
                texto += estrategia_sensibilidad
            elif sensibilidad > precision * 1.2:
                texto += estrategia_precision
            return texto

        sum_metricas = exactitud + precision + sensibilidad + f1 + auc
        if sum_metricas == 5.0:
            texto += '<p>El modelo es <b><u>perfecto</b></u>. Todas las métricas están al 100%, lo cual indica un desempeño impecable, pero cuidado con la posibilidad de esté sobreajustado. Recomiendo guardarlo para su posterior uso.</p>'
        elif exactitud >= 0.9 and f1 >= 0.9:
            texto += '<p>El modelo es de <b><u>alta calidad</b></u>, mostrando escasos errores en la predicción. Su margen de mejora será, en el mejor de los casos, marginal.</p>'
            texto = estrategia(texto, sensibilidad, precision)
            if sensibilidad >= 0.9 and precision >= 0.9:
                texto += '<p><b>Recomiendo guardarlo para su posterior uso.</b></p>'
        elif exactitud >= 0.8 and f1 >= 0.8:
            texto += '<p>El modelo es de <b><u>buena calidad</b></u>, mostrando pocos errores en la predicción. Existe margen de mejora: conviene examinar los hiperparámetros, aumentar la cantidad de datos de entrenamiento o buscar una distribución de clases objetivo más uniforme.</p>'
            texto = estrategia(texto, sensibilidad, precision)
        elif exactitud >= 0.6 and f1 >= 0.6:
            texto += '<p>El modelo es de <b><u>calidad media</b></u>, mostrando errores en la predicción. Debería considerarse una revisión: conviene examinar los hiperparámetros, aumentar la cantidad de datos de entrenamiento o buscar una distribución de clases objetivo más uniforme.</p>'
            texto = estrategia(texto, sensibilidad, precision)
        elif exactitud >= 0.5 and f1 >= 0.5:
            texto += '<p>El modelo es de <b><u>baja calidad</b></u>, mostrando muchos errores en la predicción. Recomiendo revisar los datos: conviene examinar los hiperparámetros, aumentar la cantidad de datos de entrenamiento o buscar una distribución de clases objetivo más uniforme</p>'
            texto = estrategia(texto, sensibilidad, precision)
        elif exactitud < 0.5 or f1 < 0.5:
            texto += '<p>El modelo es de <b><u>calidad nula</b></u>, mostrando más errores que aciertos en la predicción. Es imperativo revisar los datos y reentrenar el modelo: conviene examinar los hiperparámetros, aumentar la cantidad de datos de entrenamiento o buscar una distribución de clases objetivo más uniforme.</p>'
        
        
        return texto
    
    def informe_final(nom, metricas, kpis) -> str:
        """
        Da una explicación final del modelo, sus características y su utilidad en el contexto de un triaje médico.
        
        :param nom: Description
        :param metricas: Description
        :param kpis: Description
        :return: Description
        :rtype: str
        """
        texto_final = '''<br><p>Y con este informe sobre la viabilidad del modelo, llegamos al final del proyecto. Debajo de este recuadro hay 3 botones, que permiten guardar el modelo, volver a creación del modelo para probar otras opciones, o volver a la página de bienvenida, por si fuera necesario crear los datos de 0.</p>
<p>Si decido expandir la funcionalidad de esta aplicación como proyecto personal, añadiré la posibilidad de cargar un modelo guardado y más gráficas de diagnóstico, quizá incluso más opciones de modelos a crear. De momento, para este trabajo me pareció suficiente.</p>
<p>Tardé 53 días en crear este programa, incluidas casi dos semanas en las que no pude hacer gran cosa por causas personales.</p>
<br>Fdo.:<br><h3>Darío Zoreda Gallego</h3>'''

        texto = f'''<h2>Informe final de {nom}</h2>
{Informe.final(kpis, metricas)}'''
        
        texto += texto_final
        return texto
    
    def pie_final(nom: str, metricas: dict, kpis: dict[str, float]) -> str:
        """
        Docstring for pie_final
        
        :param nom: Description
        :type nom: str
        :param metricas: Description
        :type metricas: dict
        :param kpis: Description
        :type kpis: dict[str, float]
        :return: Description
        :rtype: str
        """
        str_kpis = ''
        for kpi in kpis:
            if kpi == 'F1':
                str_kpis += f' {kpi}: {kpis[kpi]:.2%}'
            else:
                str_kpis += f' {kpi}: {kpis[kpi]:.2%} |'
        if nom == 'LogisticRegression':
            texto = (f'<h3>{nom} recibido.<br> Datos del modelo:</h3>'
                     f'<ul><li>KPIs: {str_kpis}</li>'
                     f'<li>AUC: {metricas["auc"]:.2%}</li>'
                     f'<li>Pérdida logarítmica:\nNo: {metricas["log_losses"][0]:.2%} | Sí: {metricas["log_losses"][1]:.2%}</li></ul>')
        else:
            str_importancia = ''
            df_importancia = metricas['importancia_carac'].sort_values(by='importancia', ascending=False).reset_index(drop=True)
            for n, i in enumerate(df_importancia.index):
                if n == df_importancia.index[-1]:
                    str_importancia += f' {n+1}º {df_importancia.iloc[i, 0]}: {df_importancia.iloc[i, 1]:.2%}'
                else:
                    str_importancia += f' {n+1}º {df_importancia.iloc[i, 0]}: {df_importancia.iloc[i, 1]:.2%} |'
            texto = (f'<h3>{nom} recibido.<br> Datos del modelo:</h3>'
                     f'<ul><li>KPIs: {str_kpis}</li>'
                     f'<li>AUC: {metricas["auc"]:.2%}</li>'
                     f'<li>Importancia de características:{str_importancia}</li></ul>')
        
        return texto
    
