class textos:
    def bienvenida():
        texto = '''Bienvenido a este ejercicio de final de curso de Machine Learning con Deusto, realizado por Darío Zoreda.
El objetivo es crear y analizar un conjunto de datos ficticios relativos a la salud de un número de personas. 

De manera aleatoria, crearemos un número n de pacientes ficticios, con un ID, y datos de edad, peso, altura, presión arterial y glucosa.
Dado que la intención del ejercicio es ponernos las cosas un poquito complicadas, crearé esos datos como cadenas de caracteres, con el número y su unidad, y en distintas unidades de medida, cuando sea posible.
Una vez creados estos datos, crearé la columna "hospitalización", que será la columna objetivo a predecir por el modelo.
Finalmente, introduciré errores en la base de datos: números negativos, 0 y NaN.

Una vez creados los datos, pasaremos al análisis: primero, un EDA básico.
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
