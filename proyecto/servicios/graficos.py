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
    def graf_muestra(y_test, y_pred, ax):
        import seaborn as sns
        
        sns.scatterplot(x=y_test, y=y_pred, ax=ax)
        sns.lineplot(x=y_test, y=y_pred, color='red', ax=ax)
        ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='green')
        ax.set_xlabel('Datos reales')
        ax.set_ylabel('Datos predichos')
        ax.set_title('Regresión logística de hospitalización de pacientes')
        
        return ax

class EvaluacionGraf:
    def matriz_conf(cm, ax):
        """
        Docstring for matriz_conf
        
        :param cm: Description
        :param ax: Description
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
    
    def curva_roc(fpr, tpr, curva, ax):
        """
        Docstring for curva_roc
        
        :param fpr: Description
        :param tpr: Description
        :param curva: Description
        :param ax: Description
        """
        ax.plot(fpr, tpr, color='darkorange', lw=2, 
         label=f'ROC curve (AUC = {curva:.2f})')
        ax.plot([0, 1], [0, 1], color='steelblue', lw=2, linestyle='--', 
                label='Modelo')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('Ratio de falsos positivos')
        ax.set_ylabel('Ratio de positivos verdaderos')
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)
        ax.set_title('Curva de Receiver Operating Characteristic (ROC)')
        ax.legend(loc="lower right")

        return ax

    def logloss_clase(log_losses: list, ax):
        bars = ax.bar(['No', 'Sí'], log_losses, color='steelblue', alpha=0.7, 
                      edgecolor='black')
        
        for bar, loss in zip(bars, log_losses):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{loss:.4f}',
                    ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Clases')
        ax.set_ylabel('Log Loss')
        ax.set_title('Log Loss por Clase', fontsize=14)
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)
        ax.set_ylim(0, max(log_losses) * 1.15) 

        return ax

    def importancia_carac_rf(df, ax):
        ax.bar(df['características'], 
                df['importancia'], 
                color='green', alpha=0.8, edgecolor='black')
        
        ax.set_xlabel('Importancia de Característica')
        ax.set_ylabel('Características')
        ax.set_title('Importancia de Características', fontsize=14)
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)
        
        return ax
    
    def metricas_evals(metrica_entrenamiento, metrica_validacion, ax):
        import numpy as np
        # Graficar métricas de entrenamiento
        ax.plot(metrica_entrenamiento, label='Entrenamiento', linewidth=2, color='blue', marker='o')
        
        # Graficar métricas de validación
        ax.plot(metrica_validacion, label='Validación', linewidth=2, color='red', marker='s')
        
        # Añadir líneas de referencia
        ax.axhline(y=min(metrica_entrenamiento), color='green', linestyle='--', alpha=0.7, 
                    label='Mejor Entrenamiento')
        ax.axhline(y=min(metrica_validacion), color='orange', linestyle='--', alpha=0.7, 
                    label='Mejor Validación')
        
        # Añadir texto con mejor valor
        best_train_idx = np.argmin(metrica_entrenamiento)
        best_val_idx = np.argmin(metrica_validacion)
        
        ax.text(best_train_idx, min(metrica_entrenamiento), f'{min(metrica_entrenamiento):.4f}', 
                color='green', fontsize=10, fontweight='bold')
        ax.text(best_val_idx, min(metrica_validacion), f'{min(metrica_validacion):.4f}', 
                color='orange', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Número de Iteraciones')
        ax.set_ylabel('AUC')
        ax.set_title('Métricas de Evaluación durante Entrenamiento - AUC', fontsize=14)
        ax.figure.subplots_adjust(left=0.15, bottom=0.25, right=0.95, top=0.85)
        ax.legend(loc='best', fontsize=11)
        ax.grid(alpha=0.3)
class Informes:
    pass