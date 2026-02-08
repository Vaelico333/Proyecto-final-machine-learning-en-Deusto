from servicios.generador_datos import Generador_Datos 
class Leer_Datos:
    import pandas as pd
    def abrir_csv(url: str = 'datos_forjados.csv') -> pd.DataFrame:
        """
        Abre el archivo CSV especificado en el mismo directorio o un subdirectorio del actual,
        y devuélvelo en forma de DataFrame.

        :param url: Nombre del archivo CSV a abrir, incluyendo si procede, el nombre de la carpeta.
        :type url: str
        :return: DataFrame generado a partir de los datos del CSV
        :rtype: DataFrame
        """
        import pandas as pd
        import os
        url = os.path.join(os.path.dirname(__file__), url)
        try:
            with open(url,'r',encoding='UTF-8') as file:
                df = pd.read_csv(file)
        except FileNotFoundError:
            Generador_Datos.generar_datos(1)
            df = Leer_Datos.abrir_csv()
        return df
    
    def muestra_df(url: str = 'datos_forjados.csv', df = pd.DataFrame()) -> pd.DataFrame | pd.Series:
        """
        Docstring for muestra_df
        
        :param url: Nombre del archivo CSV a leer, incluyendo la extensión
        :type url: str
        :param df: Dataframe a mostrar. En caso de no proporcionarse, se creará uno desde el CSV.
        :type df: None | DataFrame | Series
        :return: Devuelve las 15 primeras y últimas entradas del DataFrame o Serie proporcionada, o los datos del CSV
        :rtype: DataFrame | Series
        """
        import pandas as pd
        if df.empty:  
            df = Leer_Datos.abrir_csv(url)
        df_muestra = pd.concat([df.head(15), df.tail(15)])
        return df_muestra
    
class Analisis():
    from pandas import DataFrame
    from numpy import ndarray
    def operacion_str(num: float, *args) -> float:
        """
        Ejecuta la operación u operaciones contenidas en args sobre num.
        
        :param num: Número sobre el que realizar la conversión.
        :type num: float
        :param args: Conjunto de operaciones a aplicar, en forma de strings con operador+número, separando cada operación de la siguiente con un espacio.
        :return: Devuelve num convertido a la nueva unidad de medida.
        :rtype: float
        """
        import operator
        import re
        # Creamos un diccionario con cada operador y la operación a la que se refiere
        operadores = {
            '/' : operator.truediv,
            '*' : operator.mul,
            '+' : operator.add,
            '-' : operator.sub
        }
        # Este patrón reconoce cadenas que contengan un operador (+-*/) y después un número con o sim decimales
        patron = r'^([+\-*/]{1})(\d+\.?\d*)$'
        for factor in args:
            # Por cada posible factor de conversión, aplicamos el patrón y extraemos el operador y la cantidad por separado
            match = re.match(patron, factor)
            operacion, numero = match.groups()
            # Aplicamos la operación correspondiente al número original
            num = operadores[operacion](num, float(numero))
        return num

    def cadena_a_numero(df: DataFrame = DataFrame(), cols: list = None, modo: str = 'num') -> DataFrame:
        """
        Docstring for cadena_a_numero
        
        :param df: Description
        :type df: DataFrame
        :param cols: Description
        :type cols: list
        :param modo: Description
        :type modo: str
        :return: Description
        :rtype: DataFrame
        """
        import pandas as pd
        import numpy as np

        if df.empty:
            df = Leer_Datos.abrir_csv()

        # Mapeo de nuevas columnas
        mapeo_cols = {
            'peso': 'peso_kg',
            'altura': 'altura_m',
            'glucosa': 'glucosa_mg_dL',
            'presion_arterial': 'presion_sistolica'
        }
        # Diccionario de conversión: (factor_multiplicador, termino_a_eliminar)
        conversiones = {
            'lb': (0.453592, 'lb'),
            'cm': (0.01, 'cm'),
            'inch': (0.0254, 'inch'),
            'mmol/l': (18.01, 'mmol/l'),
            'kg': (1.0, 'kg'),
            'mg/dl': (1.0, 'mg/dl')
                }
        def procesar_valor(val):
            try:
                for unidad, (factor, sufijo) in conversiones.items():
                    if unidad in val:
                        num = float(val.replace(sufijo, '').strip())
                        return round(num * factor, 2)
                return float(val) # Si no tiene unidad, intenta convertir a float
            except:
                return np.nan
            
        # Si no se pasan columnas, usamos las que están en nuestro mapeo y existan en el df
        if not cols:
            cols = [c for c in df.columns if c in mapeo_cols or c == 'IMC']

        df_res = df.copy()

        for col in cols:
            # Calculamos IMC basándonos en las columnas ya transformadas o existentes
            # Nota: Asegurarse de que altura esté en metros
            
            p = df_res['peso'].apply(procesar_valor)
            a = df_res['altura'].apply(procesar_valor)
            a, p = a.replace(0, np.nan), p.replace(0, np.nan)
            media_a, media_p = a.mean(), p.mean()
            a, p = a.fillna(media_a), p.fillna(media_p)
            df_res['IMC'] = pd.to_numeric(p) / (pd.to_numeric(a)**2)
            

            if col not in mapeo_cols:
                continue

            nueva_col = mapeo_cols[col]
            
            # Limpieza inicial: convertir a string y manejar nulos
            serie = df_res[col].astype(str).str.lower().str.strip()

            if col == 'presion_arterial':
                # Extraer solo la sistólica (antes del /)
                df_res[nueva_col] = serie.str.split('/').str[0].astype(float)
            
            else:
                df_res[nueva_col] = serie.apply(procesar_valor)

        # Lógica de retorno según modo
        if modo == 'total':
            return df_res
        
        elif modo == 'num':
            # Retorna columnas originales no mapeadas + las nuevas transformadas
            cols_a_mantener = [c for c in df_res.columns if c not in mapeo_cols.keys()]
            cols_a_mantener.remove('id') # Quitamos la columna id para no confundir a los modelos
            cols_a_mantener.remove('peso_kg')
            cols_a_mantener.remove('altura_m')
            return df_res[cols_a_mantener]
        
        elif modo == 'columna':
            # Retorna solo las nuevas columnas creadas en este proceso
            nuevas = [v for k, v in mapeo_cols.items() if k in cols]
            if 'IMC' in cols: nuevas.append('IMC')
            return df_res[nuevas]

        return df_res

                            
                  
    
    def limpiar_errores(df: DataFrame = DataFrame(), cols: str = None, modo: str = 'total') -> DataFrame | tuple[DataFrame, tuple[int, int, int]]:
        """
        Docstring for limpiar_errores
        
        :param df: Description
        :type df: pd.DataFrame
        :param cols: Description
        :type cols: str
        :param modo: Description
        :type modo: str
        :return: Description
        :rtype: DataFrame
        """
        import numpy as np
        if df.empty:
            df = Analisis.cadena_a_numero()

        # Identificar columnas numéricas para evitar errores de tipo
        columnas_numericas = df.select_dtypes(include=[np.number]).columns

        if not cols:
            for col in columnas_numericas:
                # Convertimos negativos a positivos primero
                df[col] = df[col].abs()
                
                # Calculamos la media de valores > 0 para que sea un promedio real
                valores_validos = df.loc[df[col] > 0, col]
                media = valores_validos.mean() if not valores_validos.empty else 0
                
                # Reemplazamos NaN y 0 por la media calculada
                df[col] = df[col].replace(0, np.nan).fillna(media)
                
                # Redondeo eficiente
                df[col] = df[col].round(2)
            return df
        
        # Modo columna (cuando se especifica una columna concreta)
        if modo == 'columna' and cols in df.columns:
            # Estadísticas previas
            num_nan = df[cols].isna().sum()
            num_cero = (df[cols] == 0).sum()
            num_neg = (df[cols] < 0).sum()

            # Limpieza
            df[cols] = df[cols].abs()
            valores_validos = df.loc[df[cols] > 0, cols]
            media = valores_validos.mean() if not valores_validos.empty else 0
            
            df[cols] = df[cols].replace(0, np.nan).fillna(media).round(2)
            
            return df[cols], (int(num_nan), int(num_cero), int(num_neg))

        return df
    
    def log_loss_modelo(modelo_dict: dict) -> list[float]:
        """
        Docstring for log_loss_modelo
        
        :param modelo_dict: Description
        :type modelo_dict: dict
        :return: Description
        :rtype: list[float]
        """
        from sklearn.metrics import log_loss
        from sklearn.preprocessing import label_binarize
        import numpy as np

        X_test = modelo_dict['X_test']
        y_test = modelo_dict['y_test']
        modelo = modelo_dict['modelo']
        y_pred_proba = modelo.predict_proba(X_test)
        n_clases = y_pred_proba.shape[1]

        y_test_bin = label_binarize(y_test, classes=range(n_clases))
        if n_clases == 2 and y_test_bin.shape[1] == 1:
            y_test_bin = np.hstack((1 - y_test_bin, y_test_bin))

        log_losses = []
        for i in range(n_clases):
            ll = log_loss(y_test_bin[:, i], y_pred_proba[:, i], labels=[0, 1])
            log_losses.append(ll)

        return log_losses
    
    def confusion_matrix_modelo(modelo_dict: dict) -> ndarray:
        """
        Docstring for confusion_matrix_modelo
        
        :param modelo_dict: Description
        :type modelo_dict: dict
        :return: Description
        :rtype: ndarray
        """
        from sklearn.metrics import confusion_matrix

        y_test = modelo_dict['y_test']
        y_pred = modelo_dict['y_pred']
        cm =  confusion_matrix(y_test, y_pred)

        return cm
    
    def roc_auc_modelo(modelo_dict: dict) -> list[ndarray, ndarray, float]:
        """
        Docstring for roc_auc_modelo
        
        :param modelo_dict: Description
        :type modelo_dict: dict
        :return: Description
        :rtype: list[ndarray]
        """
        from sklearn.metrics import roc_curve, auc
        X_test = modelo_dict['X_test']
        y_test = modelo_dict['y_test']
        modelo = modelo_dict['modelo']
        y_pred_proba = modelo.predict_proba(X_test)
        fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba[:, 1])
        roc_auc_curva = auc(fpr, tpr)

        return [fpr, tpr, roc_auc_curva]

    def importancia_caracteristicas_modelo(modelo_dict: dict) -> DataFrame:
        """
        Docstring for importancia_caracteristicas_modelo
        
        :param modelo_dict: Description
        :type modelo_dict: dict
        :return: Description
        :rtype: DataFrame
        """
        import pandas as pd
        X_test = modelo_dict['X_test']
        modelo = modelo_dict['modelo']
        características = X_test.columns.tolist()
        importancias = modelo.feature_importances_

        import_carac_df = pd.DataFrame({
            'características': características,
            'importancia': importancias}).sort_values('importancia', ascending=False)

        return import_carac_df
