from servicios.analisis import *

class textos:
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
        texto = ''' '''
        return texto
    
class info:
    def extraer_info(info: list) -> list:
        import re
        col_nom = []
        non_null = []
        dtype = []
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
    
    def extraer_descripcion(df):
        df.describe()

    def info_datos_originales(url: str = 'datos_forjados.csv'):
        """
        Abre los datos originales y 
        devuelve un resumen de las características en texto
        """
        import io
        import os
        # Leemos el archivo csv para crear un Dataframe
        url = os.path.join(os.path.dirname(__file__), url)
        df = leer_datos.abrir_csv(url)

        # Creamos un buffer para poder recoger la información del método .info()
        buffer = io.StringIO()
        df.info(buf=buffer, memory_usage=False)

        # Lo dividimos por líneas
        lista_texto = buffer.getvalue().split('\n')
        
        # Extraemos las listas de datos que necesitamos y se los aplicamos a un texto
        col_nom, non_null, dtype = info.extraer_info(lista_texto)
        texto = '''Cantidad de datos no nulos y tipo de dato por columna:\n'''
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
    
    def info_datos_num():
        
        pass