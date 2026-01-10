from servicios.analisis import *
class Eda:

    def col_hosp(figura):
        col = 'hospitalizacion'
        # Recuperamos los datos
        df_col = Analisis.cadena_a_numero()
        df_col = df_col['hospitalizacion']

        # Creamos un subplot
        ax = figura.add_subplot(111)

        # Contamos las ocurrencias de cada valor
        conteo = df_col.value_counts()

        # Creamos la gráfica de barras
        ax.bar(conteo.index, conteo.values)

        # Nombramos los ejes
        ax.set_xlabel(col)
        ax.set_ylabel('Entradas')
        ax.set_title('Distribución de los datos')
        return ax
    
    def cols_num(figura, col):

        import pandas as pd
        # Recuperamos los datos
        df_col = Analisis.cadena_a_numero()
        df_col, datos = Analisis.limpiar_errores(df_col, col, 'columna')

        # Convertimos df_col a dataframe y lo ordenamos por valores   
        df_col = pd.DataFrame(df_col)
        df_col = df_col.sort_values(col)
        df_col = df_col.reset_index(drop=True)

        # Recibimos los datos de la columna indicada
        y = df_col

        # Creamos un subplot
        ax = figura.add_subplot(111)
                        
        # Creamos la gráfica de línea
        ax.plot(y)

        #Nombramos los ejes
        ax.set_xlabel('Entradas')
        ax.set_ylabel(col)
        ax.set_title('Distribución de los datos')
        return ax
    
class GrafModelo:
    def graf_reglog(y_test, y_pred, ax):
        import seaborn as sns
        
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        sns.lineplot(x=y_test, y=y_pred, color='red', ax=ax)
        ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='green')
        ax.set_xlabel('Datos reales')
        ax.set_ylabel('Datos predichos')
        ax.set_title('Regresión logística de hospitalización de pacientes')
        
        return ax
    
    def graf_bosque():

        pass

    def graf_xgb():
        pass

class Evaluación:
    pass

class Informes:
    pass