# Predicción de hospitalización de pacientes - Aplicación de escritorio basada en Python

[Resumen](#resumen-del-proyecto) · [Características](#características-clave) · [Arquitectura](#arquitectura) · [Desafíos](#desafíos-técnicos) · [Propósito](#propósito-del-proyecto)  
[Fases](#fases-del-desarrollo) · [Módulos](#modularización) · [Aprendizaje](#qué-he-aprendido)

## Resumen del proyecto

Este proyecto es una aplicación de escritorio construida utilizando Python y PyQt5 como base para la interfaz, que guía al usuario a través de un flujo completo de Machine Learning, desde la generación de datos sintéticos, pasando por su limpieza, entrenamiento del modelo, su evaluación, y terminando con la exportación del modelo elegido.  

Esta aplicación se diseñó como un entorno educacional y experimental para comprender cómo la recolección y limpieza de los datos, así como la selección del modelo y sus hiperparámetros, afectan al resultado de la tarea de clasificación.
Los datos se han diseñado de manera que imiten la imperfecta recolección de datos en el mundo real, pero para poder crear modelos fiables, se les aplica una limpieza:  
  
Datos artificiales
       ↓
Unidades incoherentes
       ↓
Errores introducidos
       ↓
Limpieza de datos
       ↓
	  EDA
       ↓
Entrenamiento del modelo

## Características clave

- Generación de dataset de pacientes sintético
- Control del desequilibrio de clases
- Inyección de errores automática
- Limpieza de datos y normalización de unidades
- EDA: Análisis Exploratorio de los Datos
- Varios algoritmos de clasificación
- Uso de HalvingGridSearchCV para selección de hiperparámetros
- Validación cruzada
- Evaluación y comparación de modelos
- Visualización de la matriz de confusión y la curva ROC
- Análisis de importancia de características
- Persistencia de los modelos a través del proceso
- Entrenamiento de modelos multihilo
- Interfaz gráfica con PyQt5

## Arquitectura

                 ┌──────────────────────┐
                 │      PyQt5 GUI       │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       Generación de datos           Análisis de datos
              │                           │
              └─────────────┬─────────────┘
                            │
                     Entrenamiento
					   del modelo
                            │
                     Evaluación del
					      modelo
                            │
                    Resultados / Export
					
La aplicación presenta un diseño modular, con la interfaz gráfica separada de la lógica backend.

## Desafíos técnicos

**Mantener la responsividad de la GUI**  
→ Resuelto usando procesamiento multihilo  
  
**Manejo de datos artificiales inconsistentes**  
→ Diseño de un mecanismo controlado de corrupción de datos y una pipeline de limpieza  

**Compartir modelos entrenados entre páginas de la aplicación**  
→ Creación de una capa de gestión de modelos y envío y recepción de datos entre páginas  

**Gestión de múltiples configuraciones de los modelos**  
→ Entrenamiento centralizado y manejo de los hiperparámetros  

## Propósito del proyecto

Para el proyecto final del curso de Machine Learning en Deusto, se me propusieron tres opciones:

1. Analizar los datos de una **financiera** usando Tensorflow.
2. Crear datos ficticios de una empresa de **comercio electrónico** y analizarlos mediante gráficas.
3. Crear datos ficticios de **pacientes** y desarrollar un modelo que aprenda a clasificarlos como necesitados de hospitalización o no, según sus estadísticas de peso, altura, edad, glucosa en sangre y presión arterial.

Elegí la ***número 3***, ya que me parecía la más interesante y alineada con mis propósitos: crear tecnología que ayude a la gente o nos ayude a entender el mundo.

## Fases del desarrollo

### 1. Planificación

Llevaba tiempo queriendo aprender a hacer aplicaciones con GUI en python, y Qt parecía la opción ideal. Decidí hacerlo usando PyQt5, ya que hay muchos recursos y documentación al respecto.
En las instrucciones del proyecto, se me pedían los siguientes cinco bloques:
● Generación de datos e introducción de errores
● Limpieza y depuración de datos
● Entrenamiento del modelo
● Evaluación del modelo
● Representación gráfica de resultados

Decidí que crearía un widget apilado que contuviera cada una de esas partes como una página, a través de las cuales podría navegar usando botones. Crearía un script de python con la interfaz, y luego varios módulos con las funcionalidades *backend*: creación de los datos, EDA y análisis avanzado, creación y gestión de modelos, textos, gráficas y un trabajador que gestiona el *multithreading*. Todo esto se lanzaría desde un archivo main.

Las páginas serían:

1. **Bienvenida**: explicación de la estructura e intención del trabajo.
2. **Creación de datos**: se explicaría el proceso, se daría la opción de crear una base de datos de diferentes tamaños y con diferente proporción en la clase objetivo, y se podría ver una muestra de los datos creados.
3. **EDA**: se mostrarían las características de los datos, los errores, se subsanarían y quizá se mostraría la distribución de los datos de cada columna mediante gráficas.
4. **Modelos**: se daría a elegir entre tres modelos, cada uno con la opción de cambiar varios hiperparámetros y con su explicación, y al crear el modelo debería verse una representación del mismo y debería poderse propagar ese modelo a las siguientes páginas.
5. **Evaluación**: con el modelo recibido de la página anterior, se evaluarían varias métricas básicas, se mostraría alguna gráfica pertinente y se daría una valoración en base a las métricas obtenidas.
6. **Informe final**: con el mismo modelo recibido de las páginas anteriores, se daría un veredicto final y una explicación, así como alguna representación del modelo y una despedida. Más tarde decidí añadir la opción de guardar el modelo.

Con esto en mente, me puse a trabajar: lo primero, la creación de los datos y algunos análisis.

### 2. Generación de datos

Primero, creé todas las variables asociadas a cada paciente usando la función normal dentro de random de numpy, la cual extrae números aleatorios de una distribución normal marcada por un punto central y una desviación estándar. Eso hace que los datos creados, en principio, tengan una distribución muy natural y parecida a lo que probablemente veríamos en la realidad.
Para agregarle dificultad, creé las variables peso, altura y glucosa usando dos tipos de magnitud distinta (kg y libras, para el peso, por ejemplo). Luego, introduje en cada dato el nombre de la magnitud y lo guardé como cadena de caracteres. Entonces, en función de la edad del paciente, creé unos rangos y evalué cada paciente según su gravedad para etiquetarlo como "Sí" o "No" necesita hospitalización.
Y llegó el momento de añadir otro hándicap: errores. Decidí introducir los errores de manera aleatoria con la opción en varios pasos de "salvarse", de tal forma que no fueran tan frecuentes: de media, se crea un 7-7,5% de errores. Pueden ser de tres tipos: sustituir por 0, por NaN o cambiar a negativo.
Y como colofón de este módulo, todos los datos generados se guardan en forma de archivo CSV.

Antes de comenzar con la interfaz, definí otra función que abriría el archivo CSV y lo leería, devolviendo un DataFrame que contenga todos los datos. Si no existe el CSV al abrir el programa, se le llamará desde la interfaz para que cree una mini base de datos de 100 entradas, para asegurar que no haya fallos en la ejecución.

### 3. Interfaz

Entonces comencé a crear la interfaz, y el resto de módulos y funciones las crearía cuando las necesitase. Con la ayuda de la herramienta *designer* de Qt y la amplia experiencia con este módulo que hay recogida en internet, me dediqué a crear mi app primero, y después a ir escribiendo página por página, en orden.

Primero pensé en un menú de navegación, pero me di cuenta de que poder saltar entre secciones podría traer complicaciones si lo que quería era crear un modelo y evaluarlo, ya que podría llegar a una página de evaluación sin modelo a evaluar. Me decidí por una estructura más simple: un *widget* apilado, con páginas por las que navegaría de manera secuencial usando botones. Y al final de la aplicación, un botón para volver al principio. Más tarde, agregué un segundo botón para volver a la página de entrenamiento del modelo.

### 4. Páginas iniciales

La **página de bienvenida** la hice muy simple:

- Título arriba.
- Cuadro de texto con la explicación del proyecto en el medio.
- Botón para pasar a la siguiente página debajo.

Pero aproveché para fijar el estilo que quería darle al resto de la aplicación.

En la página de **generación de datos** comencé a crear una estructura más compleja:

- Título arriba.
- Un *layout* horizontal que contiene las dos partes de la página:
  - A la izquierda, un selector de la cantidad de datos a generar, y debajo un *slider* para seleccionar la proporción de la clase objetivo. Justo debajo, un cuadro de texto con la explicación pertinente, y finalmente, el botón que genera los datos.
  - A la derecha, una vista de tabla que permite visualizar una muestra de los datos recién creados.
- Botón para pasar a la siguiente página debajo.

Estas dos páginas marcarían el estilo y organización del resto.

### 5. Página del EDA

Ahora pasamos a la página de EDA, o Análisis Exploratorio de los Datos. Aquí vamos a explorar la estructura de los datos, los errores o vacíos y veremos cómo están distribuidos los datos.
Como la idea es explorar varios conceptos, decidí crear un *widget* de pestañas, cada una de las cuales se dedicara a un paso del análisis:

1. **Transformación**: convertimos las columnas tipo *string* en numéricas, y estandarizamos a una unidad de medida por columna. Estructura:
	- Izquierda: un selector para la columna a explorar, el botón de transformar y debajo un cuadro de texto explicativo que se actualiza con los datos de la columna, una vez pulsado el botón.
	- Derecha: una vista de tabla que nos muestra la columna seleccionada, ya transformada a numérico y estandarizada.

2. **Errores**: analizamos en busca de errores, y los solucionamos. La estructura es muy similar a la pestaña anterior:
	- Izquierda: un selector para la columna a explorar, el botón de eliminar errores y debajo un cuadro de texto explicativo que se actualiza con los datos de la columna, una vez pulsado el botón.
	- Derecha: una vista de tabla que nos muestra los datos ya limpios, una vez pulsamos el botón.

3. **Representación gráfica**: mostramos la distribución de los datos a lo largo las entradas, por columna. En el caso de *hospitalizacion*, se muestra un gráfico de barras con la proporción de cada una de las clases. La estructura cambia:
	- Arriba: selector de columna y botón para generar la gráfica.
	- Central: *widget* tipo lienzo para representación de las gráficas.
	- Debajo: botón para pasar a la siguiente página.

### 6. Página de entrenamiento del modelo

En la página de creación del modelo seleccionaremos el modelo a entrenar y los hiperparámetros correspondientes, o bien entrenar el modelo usando *HalvingGridSearchCV*, o validación cruzada en cuadrícula eliminatoria, que evalúa una serie de combinaciones predefinidas de hiperparámetros usando validación cruzada, y selecciona la configuración que mejor funciona según la métrica escogida. Es más eficiente que GridSearchCV, ya no necesita evaluar todas las opciones disponibles, sino que evalúa todos los modelos con pocos datos y escoge la mitad más eficiente, y así sucesivamente hasta encontrar el mejor. Al otorgarle el hiperparámetro *cv=3*, se consigue que se entrenen dos versiones del modelo, y se valide en la tercera.
Aquí, para cada uno de los tres posibles modelos, creamos una pestaña, con la siguiente estructura:

1. Izquierda: arriba, un selector para cada uno de los hiperparámetros, con su botón de entrenar el modelo con ellos o con validación cruzada. Más abajo, un cuadro de texto donde explicamos el modelo y sus parámetros, y finalmente, un texto con los datos del modelo ya entrenado que sólo aparece al crearlo.
2. Derecha: al crear un modelo aparecerá una barra de progreso que nos hará saber cuánto tiempo queda aproximadamente para terminar el entrenamiento. Debajo, mostramos una representación gráfica de la correlación entre los datos predichos por el modelo y los datos reales de prueba, como primera medida de la capacidad predictiva del modelo. Debajo, al entrenar el modelo aparecerá también el botón que nos permitirá continuar a la evaluación del modelo que tengamos en ese momento entrenado en la pestaña actual.

### 7. Evaluación del modelo

Aquí, según el modelo que se envíe desde la página anterior, se realizará la evaluación correspondiente:

- LogisticRegression:
	- Matriz de confusión: permite ver los aciertos y errores, y su tipo.
	- Pérdida logarítmica por clase: castiga la incertidumbre y el exceso de confianza en los errores.
 	- Curva ROC y AUC: compara falsos positivos con verdaderos positivos a lo largo de diferentes umbrales de clasificación, indicando su capacidad de predicción.
- RandomForestClassifier:
	- Matriz de confusión: permite ver los aciertos y errores, y su tipo.
	-  Importancia de características: muestra qué características de los datos han ofrecido más información. Muy útil en caso de querer podar los árboles.
  	- Curva ROC y AUC: compara falsos positivos con verdaderos positivos a lo largo de diferentes umbrales de clasificación, indicando su capacidad de predicción.
 -  XGBClassifier:
	- Matriz de confusión: permite ver los aciertos y errores, y su tipo.
	-  Importancia de características: muestra qué características de los datos han ofrecido más información. Muy útil en caso de querer podar los árboles.
  	- Curva ROC y AUC: compara falsos positivos con verdaderos positivos a lo largo de diferentes umbrales de clasificación, indicando su capacidad de predicción.

El hecho de que los modelos compartan métricas, facilita su comparación. Todos los modelos evalúan la exactitud, precisión, sensibilidad y F1:

- La **exactitud** nos indica cuál es el porcentaje de aciertos sobre el total de predicciones correctas. Es una *medida general* de la capacidad de predicción del modelo.
- La **precisión** nos muestra los aciertos a la hora de marcar un dato como positivo, sobre el total de datos marcados como positivo. Mide el *entusiasmo* del modelo para marcar como positivos datos que realmente son negativos.
- La **sensibilidad** nos indica cuántos casos positivos reales fueron identificados correctamente por el modelo. Podría decirse que mide la *precaución* del modelo a la hora de afirmar que un dato es positivo. Es especialmente importante en este ejercicio, ya que podría marcar como sanos a pacientes que sí necesitan hospitalización. Debe ser lo más alta posible.
- La **puntuación F1** resulta de la media armónica entre la precisión y la sensibilidad. Nos indica el *desempeño general* del modelo.
  
La estructura es la siguiente:

1. Izquierda: creamos cuatro contenedores con un título y la métrica asociada para exactitud, precisión, sensibilidad y puntuación F1 del modelo. Debajo, en un cuadro de texto, se muestra una explicación de cada una de las métricas y lo que implican a nivel de rendimiento del modelo. La explicación es condicional a la puntuación obtenida.
2. Derecha: mostramos tres gráficas que nos ayudan a visualizar mejor el rendimiento del modelo: matriz de confusión, gráfica personalizada según el tipo de modelo (pérdida logarítmica o importancia de características) y curva ROC.

### 8. Informe final

Esta es la página del informe final, donde doy una breve explicación final y una valoración general del modelo, y muestro una gráfica representativa o informativa del modelo.
La estructura es:

1. Izquierda: mostramos un cuadro de texto con la valoración final y una nota de despedida. Debajo, un botón nos permite guardar el modelo creado junto con sus especificaciones y otro nos permite volver a la página de entrenamiento de los modelos.
2. Derecha: se muestra una gráfica personalizada (impacto de las variables en LogisticRegression, un árbol de decisión para los otros dos modelos). Debajo, un cuadro de texto con un resumen de las métricas del modelo actual, y finalmente, un botón que permite volver a la primera página de la aplicación.

## Modularización

### Módulo de interfaz

El módulo **interfaz** contiene la aplicación PyQt5 y todas sus partes.  

### Módulo visual accesorio

Todos los textos a mostrar en los cuadros de texto quedaron contenidos en el módulo **textuales**, y las gráficas se generan siempre desde el módulo **graficos**.  

### Módulos backend

El módulo **generador_datos** se encarga exclusivamente de crear los datos sintéticos de pacientes, introducir errores en ellos y guardar el archivo en forma de archivo CSV.  
Desde el módulo **analisis** se gestiona la evaluación de los modelos, además del EDA, la limpieza de datos y la lectura del CSV.  
Desde el módulo **modelos** se gestiona el entrenamiento de los modelos, sea directo o mediante validación cruzada, los hiperparámetros, el guardado del modelo y sirve de intermediario para la evaluación de los modelos.  

### Módulo de control

Desde el módulo **trabajador** se gestiona tanto el control de progreso del entrenamiento de los modelos como la ejecución multihilo para evitar que la aplicación se congele al intentar gestionar a la vez la interfaz y los modelos.

## Resultados

Mediante esta aplicación, me ha sido posible crear y comparar los tres tipos de modelo de clasificación utilizados: regresión logística, bosque aleatorio e incremento extremo del gradiente (XGBoost).  
Para encontrar los mejores modelos, utilicé la técnica de validación cruzada en cuadrícula (HalvingGridSearchCV). Los resultados son:

### Modelo con mejores características generales

El modelo que mejor F1 presenta, siendo esta métrica una media armónica de la precisión y la sensibilidad, es el modelo **XGBoost**:  

- Exactitud: 0.9775  
- Precisión: 0.9942  
- Sensibilidad: 0.9606  
- F1: 0.9771  

Sus hiperparámetros, escogidos mediante HalvingGridSearchCV, son:  

- objective: binary:logistic
- colsample_bytree: 0.6
- gamma: 0.2
- learning_rate: 0.05
- max_depth: 5
- min_child_weight: 1
- reg_alpha: 0
- reg_lambda: 0
- subsample: 0.6


### Modelo con mejor característica para el caso (sensibilidad)



## Qué he aprendido 

### Lo que este proyecto demuestra

- Desarrollo de aplicaciones en Python
- Desarrollo de interfaces gráficas con PyQt5
- Preprocesamiento de datos y EDA
- Uso de modelos de clasificación
- Optimización de hiperparámetros
- Evaluación de modelos
- Modularización de programas
- Procesamiento multihilo
- Visualización de datos

### Lo que me gustaría mejorar

- Añadir tests automatizados
- Mejorar la gestión de errores
- Mejorar el empaquetado en .EXE de la aplicación
- Añadir gestión de la configuración
- Mejorar el control sobre la inyección de errores
- Mejorar la comparación de modelos
- Introducir más modelos
- Introducir la carga de modelos pre-guardados
