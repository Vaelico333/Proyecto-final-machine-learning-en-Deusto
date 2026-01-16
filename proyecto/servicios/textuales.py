from servicios.analisis import *

class Textos:
    def bienvenida():
        """Devuelve el texto de la página de bienvenida de la aplicación."""
        texto = u'''    Bienvenido a este ejercicio de final de curso de Machine Learning con Deusto, realizado por Darío Zoreda.
El objetivo es crear y analizar un conjunto de datos ficticios relativos a la salud de un número de personas. 

De manera aleatoria, crearemos un número n de pacientes ficticios, con un ID, y datos de edad, peso, altura, presión arterial y glucosa.
Dado que la intención del ejercicio es ponernos las cosas un poquito complicadas, crearé esos datos como cadenas de caracteres, con el número y su unidad, y en distintas unidades de medida, cuando sea posible.
Una vez creados estos datos, crearé la columna "hospitalización", que será la columna objetivo a predecir por el modelo.
Finalmente, introduciré errores en la base de datos: números negativos, 0 y NaN.

Habiendo ya creado los datos, pasaremos al análisis: primero, un EDA básico.
Veremos cómo transformo las columnas de cadenas de caracteres a números, y cómo homogeneizo las unidades.
Entonces, pasaremos a ver las características de los datos, los errores y cómo los corregiré.

Ya tendremos los datos listos para entrenar un modelo.
Se ofrecen tres opciones a probar: árbol de decisión, bosque aleatorio y SVC.
Según el modelo elegido, se mostrará una gráfica que lo represente.
Ahora vamos a evaluar el rendimiento del modelo, con una matriz de confusión, la curva ROC-AUC y las puntuaciones de precisión y recuperación.

Finalmente, veamos unas gráficas demostrativas del rendimiento del modelo:
- Importancia de las características
- Densidad de probabilidades
- Dispersión por clase predicha frente a clase real
- Ganancias y pérdidas
'''
        return texto
    
    def creacion():
        """Devuelve el texto de explicación de la creación de los datos."""
        texto = u'''En este paso, crearemos la base de datos.
Primero, estableceré unos rangos de peligro basados en lo que la ciencia médica dice, para el IMC, la presión arterial y la glucosa, y todo ello relacionado con unos rangos de edad.
Para agregar complejidad a los datos, creé las columnas de altura, peso y glucosa con dos tipos de unidad de medida cada una, distribuida de manera aleatoria.
Para asegurar una distribución realista, utilizaré una distribución normal o de campana de Gauss, estableciendo una desviación estándar tal que produzca datos extremos más o menos realistas, que nos permitan crear esos datapoints en los que el paciente debe ser hospitalizado.
El siguiente paso es revisar si se cumple alguna condición para la hospitalización (con una basta), y agregar la columna correspondiente.
Una vez los datos están completos y coherentes, agregamos errores: de manera aleatoria, se cambian datos por 0, NaN o se cambian de signo a negativo.
Finalmente, guardamos los datos en un archivo de formato csv: datos_forjados.csv'''
        return texto
    
    def transf_num():

        texto = u'''Debido al formato en que hemos recibido los datos, hay varias columnas que son de tipo "object", y por tanto, incompatibles con un modelo de clasificación o regresión.
Además, hay columnas con más de un tipo de unidad, lo cual es un gran problema, ya que al tener diferentes escalas, desvirtuarían mucho la capacidad predictiva del modelo.
Por tanto, en el backend realizaremos dos operaciones fundamentales:
- Quitar el nombre de la unidad, dejando sólo el número.
- Convertir el número a una unidad estándar, y cambiar su tipo a float.

Con esto, tendremos un DataFrame compuesto de 7 características, 6 de ellas numéricas y una categórica (hospitalización)
'''
        return texto
    
    def trat_err():
        texto = '''Ahora pasamos a eliminar los errores que introdujimos en los datos previamente.
Como no sabemos cuál era el dato original, he decidido que los ceros y NaN serán sustituidos por la media aritmética, y todos 
los datos que estén en signo negativo serán multiplicados por -1, aunque también hubiera servido usar la función abs().

Con estas operaciones, los datos ya están listos para ser utilizados en el entrenamiento de nuestro modelo.

A continuación, se muestra un recuento de los errores en la columna seleccionada, y el DataFrame resultado de la limpieza:

'''
        return texto
    
    def modelo_reglog():
        ecuacion_logit = u"ln(P / (1 - P)) = β₀ + β₁X₁ + ... + βₙXₙ" 
        ecuacion_sigmoide = u"P = 1 / (1 + e^-(β₀ + β₁X₁ + ... + βₙXₙ))"
        texto = f'''Modelo de Regresión Logística.
Este es el modelo más sencillo que vamos a crear. No es el más recomendado, pero es un buen comienzo para empezar a analizar y entender nuestros datos.
Es un modelo basado en la función logística o sigmoide, que transforma una combinación lineal de variables en una probabilidad.
La ecuación del modelo se crea al igualar la ecuación Logit a una combinación lineal de los predictores (X):
{ecuacion_logit}

Finalmente, obtenemos la probabilidad directa (P) a partir de la ecuación anterior.
Para ello, se despeja la fórmula resultando en la función logística o inversa del logit:
{ecuacion_sigmoide}

Con esto, obtenemos un rango de probabilidad entre 0 y 1, y nuestro modelo intentará asignar una de las dos categorías objetivo a cada entrada (sí o no).
Como podemos ver en la gráfica de la derecha, el ajuste a los datos reales bastante bajo.

En la página siguiente veremos los datos de evaluación del modelo.

Parámetros:
- Penalty: es la regularización que se aplica al modelo, que castiga los coeficientes demasiado grandes para evitar el overfitting. Opciones:
    · "l2": la llamada técnica "Ridge", es la predeterminada, y penaliza la suma de los cuadrados de los coeficientes.
    · "l1": conocida como "Lasso", penaliza el valor absoluto de los coeficientes, pudiendo llevar algunos valores a 0, y actuando así como una herramienta de selección de variables.
    · "elasticnet": es una combinación de las dos anteriores.
    · "None": no aplica ninguna regularización
- C: controla cómo de fuerte es la penalización aplicada. Consiste en un número de tipo "float" positivo.
    · Valor bajo: presentará una regularización fuerte. Se evita el overfitting, pero el modelo podría perder capacidad de ajuste.
    · Valor alto: regularización débil, que permite mayor ajuste a los datos de entrenamiento, y perjudicando la capacidad predictiva del modelo.
- Solver: se trata del algoritmo que encuentra los mejores coeficientes para el modelo y minimiza la función de pérdida. Las opciones son:
    · "newton-cg": o Newton Conjugate Gradient, usa información de la curvatura de la función de pérdida para encontrar el mínimo. Soporta nativamente la clasificación de más de dos clases. Sólo es compatible con regularización l2 o ninguna. Es bastante robusto, y converge en menos iteraciones que otros métodos, aunque cada iteración es más costosa. Se recomienda usarlo  cuando el tamaño de los datos es de pequeño a mediano.
    · "liblinear": 
    · "saga"
- Max iter
'''
        return texto

    def modelo_bosque():
        texto = ''' Modelo de Bosque Aleatorio.
Es el modelo más típicamente usado para este tipo de problema, y el que se recomendó en la documentación del proyecto.
Se trata de un modelo de aprendizaje supervisado que combina varios árboles de decisión (los que se definan en el parámetro "n_estimators") para obtener un resultado más consistente y preciso.

'''
        return texto

    def modelo_xgb():
        texto = ''' Modelo Aumento Extremo del Gradiente
'''
        return texto
    
class Info:
    import pandas as pd
    def extraer_info(info: list) -> list:
        import re
        col_nom = []
        non_null = []
        dtype = []
        # Patrón correspondiente a, por ejemplo: " 8  abc4  123  non-null def5"
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
    
    def crear_info(df: pd.DataFrame) -> list:
        import io
        # Creamos un buffer para poder recoger la información del método .info()
        buffer = io.StringIO()
        df.info(buf=buffer, memory_usage=False)
        # Lo dividimos por líneas
        lista_texto = buffer.getvalue().split('\n')
        return lista_texto

    def extraer_descripcion_columna(df: pd.DataFrame) -> list:
        info = df.describe()
        col = info.columns
        iterador = info[col].items()

        descripcion = []
        for label, content in iterador:
            for linea in content:
                descripcion.append(linea)
        return descripcion

    def info_datos_originales(url: str = 'datos_forjados.csv'):
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
    
    def info_datos_num(col: str, url: str = 'datos_forjados.csv') -> tuple[pd.DataFrame, tuple[str,str,str]]:
        
        df = Leer_Datos.abrir_csv(url)
        df_num = Analisis.cadena_a_numero(df=df, cols=[col], modo='columna')

        lista_texto = Info.crear_info(df_num[0])

        col_nom, non_null, dtype = Info.extraer_info(lista_texto)
        descripcion = Info.extraer_descripcion_columna(df_num[0])
        texto = f'''
Al realizar el tratamiento de los datos, vamos viendo el progreso en la coherencia de estos:

Cantidad de datos y tipo de dato en {col_nom[0]}:
    - Datos no nulos: {non_null[0]}
    - Datos nulos: {len(df) - int(non_null[0])}
    - Tipo de dato: {dtype[0]}

Características de la columna:
    - Media aritmética: {round(descripcion[1], 2)}
    - Desviación estándar: {round(descripcion[2], 2)}
    - Valor mínimo: {descripcion[3]}
    - Mediana: {descripcion[5]}
    - Valor máximo: {descripcion[7]}

'''
        unidades = {'peso':['kg', 'lb'],
                    'altura':['m', 'cm, inch'],
                    'glucosa':['mg/dL', 'mmol/L']}
        if col in unidades.keys():
            texto += f'''Cantidad de datos originales en {col_nom[0]}:
- Unidades estándar ({unidades[col][0]}): {df_num[1][0]}
- Unidades no estándar ({unidades[col][1]}): {df_num[1][1]}
'''
        return texto
    
    def info_datos_noerr(col: str, url: str = 'datos_forjados.csv') -> str:

        columnas = {'peso_kg':'peso',
                    'altura_m':'altura',
                    'presion_sistolica':'presion_arterial',
                    'glucosa_mg_dL':'glucosa'}
        df = Leer_Datos.abrir_csv(url)
        if col in columnas.keys():
            df_num = Analisis.cadena_a_numero(df=df, cols=[columnas[col]], modo='columna')
            df_noerr = Analisis.limpiar_errores(df=df_num[0], cols=col, modo='columna')
        elif col == 'hospitalizacion':
            df_noerr = ('', (0,0,0))
        else:
            df_num = Analisis.cadena_a_numero(df=df, cols=[col], modo='columna')
            df_noerr = Analisis.limpiar_errores(df=df_num[0], cols=col, modo='columna')
        
        texto = f'''
Recuento de errores en la columna {col}:
    - NaN: {df_noerr[1][0]}
    - 0: {df_noerr[1][1]}
    - Negativos: {df_noerr[1][2]}'''
        return texto
