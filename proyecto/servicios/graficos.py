from servicios.analisis import Analisis
class Eda:
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    def col_hosp(figura: Figure) -> Axes:
        """
        Docstring for col_hosp
        
        :param figura: Description
        :type figura: Figure
        :return: Description
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
    
    def cols_num(figura: Figure, col: str) -> Axes:
        """
        Docstring for cols_num
        
        :param figura: Description
        :type figura: Figure
        :param col: Description
        :type col: str
        :return: Description
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
    def graf_muestra(y_test: Series, y_pred: ndarray, ax: Axes):
        """
        Docstring for graf_muestra
        
        :param y_test: Description
        :type y_test: Series
        :param y_pred: Description
        :type y_pred: ndarray
        :param ax: Description
        :type ax: Axes
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
    def matriz_conf(cm: ndarray, ax: Axes) -> Axes:
        """
        Docstring for matriz_conf
        
        :param cm: Description
        :type cm: ndarray
        :param ax: Description
        :type ax: Axes
        :return: Description
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
    
    def curva_roc(fpr: ndarray, tpr: ndarray, curva: float, ax: Axes) -> Axes:
        """
        Docstring for curva_roc
        
        :param fpr: Description
        :type fpr: ndarray
        :param tpr: Description
        :type tpr: ndarray
        :param curva: Description
        :type curva: float
        :param ax: Description
        :type ax: Axes
        :return: Description
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

    def logloss_clase(log_losses: list[float], ax: Axes) -> Axes:
        """
        Docstring for logloss_clase
        
        :param log_losses: Description
        :type log_losses: list[float]
        :param ax: Description
        :type ax: Axes
        :return: Description
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

    def importancia_carac(df: DataFrame, ax: Axes) -> Axes:
        """
        Docstring for importancia_carac
        
        :param df: Description
        :type df: DataFrame
        :param ax: Description
        :type ax: Axes
        :return: Description
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
    
    def grafico_final(modelo_dict: dict, ax: Axes, nom: str):

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