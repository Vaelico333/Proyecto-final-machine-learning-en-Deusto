from servicios.analisis import Analisis
class Eda:
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    @staticmethod
    def col_hosp(figura: Figure) -> Axes:
        """
        Crea una gráfica de barras que muestra la distribución de las clases de la columna "hospitalizacion"
        
        :param figura: Figura en la que se dibujará la gráfica.
        :type figura: Figure
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
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
    
    @staticmethod
    def cols_num(figura: Figure, col: str) -> Axes:
        """
        Crea una gráfica de línea que muestra la distribución de los datos de la columna a lo largo de sus entradas.
        
        :param figura: Figura en la que se dibujará la gráfica.
        :type figura: Figure
        :param col: Columna a graficar.
        :type col: str
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
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
    from matplotlib.axes import Axes
    from pandas import Series
    from numpy import ndarray
    @staticmethod
    def graf_muestra(y_test: Series, y_pred: ndarray, ax: Axes) -> Axes:
        """
        Crea una gráfica que muestra la exactitud del modelo.
        
        :param y_test: Variable objetivo de prueba.
        :type y_test: Series
        :param y_pred: Variable objetivo predicha por el modelo.
        :type y_pred: ndarray
        :param ax: Objeto tipo Axes que contendrá la gráfica.
        :type ax: Axes
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
        import seaborn as sns
        
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        sns.lineplot(x=y_test, y=y_pred, color='red', ax=ax)
        ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='green')
        ax.set_xlabel('Datos reales')
        ax.set_ylabel('Datos predichos')
        
        return ax

class EvaluacionGraf:
    from pandas import DataFrame
    from numpy import ndarray
    from matplotlib.axes import Axes
    @staticmethod
    def matriz_conf(cm: ndarray, ax: Axes) -> Axes:
        """
        Crea un mapa de calor que muestra la matriz de confusión del modelo.
        
        :param cm: Matriz de confusión del modelo.
        :type cm: ndarray
        :param ax: Objeto tipo Axes que contendrá la gráfica.
        :type ax: Axes
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
        import seaborn as sns

        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels='auto',
                    yticklabels='auto', ax=ax)
        ax.set_xlabel('Predicción')
        ax.set_ylabel('Valor real')
        ax.set_title('Matriz de confusión')
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)

        return ax
    
    @staticmethod
    def curva_roc(fpr: ndarray, tpr: ndarray, curva: float, ax: Axes) -> Axes:
        """
        Crea una gráfica de línea que muestra la curva ROC.
        
        :param fpr: Ratio de falsos positivos.
        :type fpr: ndarray
        :param tpr: Ratio de verdaderos positivos.
        :type tpr: ndarray
        :param curva: Puntuación AUC-ROC.
        :type curva: float
        :param ax: Objeto tipo Axes que contendrá la gráfica.
        :type ax: Axes
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
        ax.plot(fpr, tpr, color='darkorange', lw=2, 
         label=f'ROC curve (AUC = {curva:.2f})')
        ax.plot([0, 1], [0, 1], color='steelblue', lw=2, linestyle='--', 
                label='Referencia de azar')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('Ratio de falsos positivos')
        ax.set_ylabel('Ratio de positivos verdaderos')
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)
        ax.set_title('Curva de Receiver Operating Characteristic (ROC)')
        ax.legend(loc="lower right")

        return ax

    @staticmethod
    def logloss_clase(log_losses: list[float], ax: Axes) -> Axes:
        """
        Crea una gráfica de barras que muestra la pérdida logarítmica por clase.
        
        :param log_losses: Lista de puntuaciones de pérdida por clase.
        :type log_losses: list[float]
        :param ax: Objeto tipo Axes que contendrá la gráfica.
        :type ax: Axes
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
        bars = ax.bar(['No', 'Sí'], log_losses, color='steelblue', alpha=0.7, 
                      edgecolor='black')
        
        for bar, loss in zip(bars, log_losses):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{loss:.4f}',
                    ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Hospitalización')
        ax.set_ylabel('Log Loss')
        ax.set_title('Pérdida logarítmica por clase', fontsize=14)
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)
        ax.set_ylim(0, max(log_losses) * 1.15) 

        return ax

    @staticmethod
    def importancia_carac(df: DataFrame, ax: Axes) -> Axes:
        """
        Crea una gráfica de barras que muestra la importancia relativa de cada característica con que se entrenó el modelo.
        
        :param df: Dataframe que contiene la lista de características y su importancia.
        :type df: DataFrame
        :param ax: Objeto tipo Axes que contendrá la gráfica.
        :type ax: Axes
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
        ax.bar(df['características'], 
                df['importancia'], 
                color='green', alpha=0.8, edgecolor='black')
        
        ax.set_ylabel('Importancia')
        ax.set_xlabel('Características')
        ax.set_title('Importancia de Características', fontsize=14)
        ax.tick_params(axis='x', labelrotation=15)
        ax.figure.subplots_adjust(left=0.15, bottom=0.35, right=0.95, top=0.85)
        
        return ax
    
class Informes:
    from matplotlib.axes import Axes
    @staticmethod
    def grafico_final(modelo_dict: dict, ax: Axes, nom: str) -> Axes:
        """
        Crea una gráfica acorde al modelo actual: impacto de características en LogReg, y uno de los árboles en el resto.
        
        :param modelo_dict: Diccionario que contiene el modelo y X_test, como mínimo.
        :type modelo_dict: dict
        :param ax: Objeto tipo Axes que contendrá la gráfica.
        :type ax: Axes
        :param nom: Nombre del tipo de modelo.
        :type nom: str
        :return: Objeto tipo Axes que contiene la gráfica.
        :rtype: Axes
        """
        import matplotlib.pyplot as plt
        modelo = modelo_dict['modelo']
        X = modelo_dict['X_test']
        if nom == 'LogisticRegression':
            coefs = modelo.coef_[0]
            columnas = Analisis.limpiar_errores().drop(columns='hospitalizacion').columns
            ax.barh(columnas, coefs, color=['red' if c < 0 else 'blue' for c in coefs])
            ax.axvline(0, color='black', linestyle='--')
            ax.set_title("Impacto de las Variables (Coeficientes)")

        elif nom == 'RandomForestClassifier':
            from sklearn.tree import plot_tree
            arbol = modelo.estimators_[-1]
            plot_tree(arbol, feature_names=X.columns, label='root', impurity=False, filled=True, rounded=True, ax=ax, fontsize=5)

        elif nom == 'XGBClassifier':
            import xgboost as xgb
            plt.rcParams.update({'font.size': 12}) 
            xgb.plot_tree(modelo, tree_idx=-1, rankdir='LR', ax=ax, condition_node_params={'fontsize':'20'}, leaf_node_params={'fontsize':'20'})

        return ax