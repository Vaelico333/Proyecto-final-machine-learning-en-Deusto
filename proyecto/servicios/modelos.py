from servicios.analisis import Analisis, Limpieza, Leer_Datos
from servicios.trabajador import Decorador
from numpy import ndarray
from pandas import Series
from matplotlib.axes import Axes

class Modelo():
    @staticmethod
    def params(modelo: str) -> dict:
        """
        Contén y devuelve los hiperparámetros posibles para el entrenamiento de cada modelo.
        
        :param modelo: Nombre abreviado del modelo a entrenar.
        :type modelo: str
        :return: Diccionario con todos los hiperparámetros posibles del modelo solicitado.
        :rtype: dict
        """
        parametros_reglog = {'l1_ratio':[1.0,0.5,0],
                             'C':[0.01, 0.1, 1.0, 10.0],
                             'solver':['liblinear','newton-cg','saga'],
                                 'max_iter':[100, 1000, 10000]}
        
        parametros_bosque = {'n_estimators':[100, 200],
                             'max_depth':[5, 10],
                             'min_samples_split':[10, 25, 50],
                             'min_samples_leaf':[1, 5, 10, 20],
                             'max_features':[1, 3, 5],
                             'bootstrap':[True,False]}
        
        parametros_xgb = {'n_estimators':[100, 300],
                          'learning_rate':[0.05, 0.15, 0.3],
                          'max_depth':[5, 7],
                          'min_child_weight':[1, 3],
                          'subsample':[0.6, 0.9],
                          'colsample_bytree':[0.6, 0.9],
                          'reg_alpha':[0, 1],
                          'reg_lambda':[0, 1]}
        
        switch = {'reglog': parametros_reglog,
              'bosque': parametros_bosque,
              'xgb': parametros_xgb}
        
        return switch[modelo]
    
    
    @Decorador.progreso
    @staticmethod
    def regresion_logistica(*args, **kwargs):
        """
        Entrena un modelo de regresión logística usando los hiperparámetros aportados en args y devuelve un diccionario que contiene el modelo, X_test e y_test.
        
        :param args: Hiperparámetros para entrenar el modelo.
        :param kwargs: Otros parámetros relativos a Trabajador.
        """
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        df = Limpieza.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        columnas = X.columns.tolist()
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17, stratify=y)

        l1_ratio = args[0]
        C = args[1]
        solver = args[2]
        max_iter = args[3]

        if solver != 'saga':
            l1_ratio = None
            penalty = 'l2'
        else:
            penalty = 'elasticnet'

        modelo = Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(
                l1_ratio=l1_ratio,
                C=C,
                solver=solver,
                penalty=penalty,
                max_iter=max_iter,
                class_weight='balanced',
                random_state=17
            ))
        ])
        for n in range(1, max_iter + 1):
            modelo.fit(X_train, y_train)
            reporte(n)
        modelo_dicc = {'X_test': X_test, 'y_test': y_test,
                       'tipo_modelo': 'LogisticRegression',
                       'random_state': 17,
                       'test_size': 0.25,
                       'feature_names': columnas,
                       'target_column': 'hospitalizacion',
                       'preprocessing': {'scaler': 'StandardScaler'}}
        modelo_dicc['modelo'] = modelo
        modelo_dicc['y_pred'] = modelo.predict(X_test)
        return modelo_dicc

    @Decorador.progreso
    @staticmethod
    def bosque_aleatorio(*args, **kwargs):
        """
        Entrena un modelo de bosque aleatorio usando los hiperparámetros aportados en args y devuelve un diccionario que contiene el modelo, X_test e y_test.
        
        :param args: Hiperparámetros para entrenar el modelo.
        :param kwargs: Otros parámetros relativos a Trabajador.
        """
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier

        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        df = Limpieza.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        columnas = X.columns.tolist()
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17, stratify=y)
        modelo_dicc = {'X_test': X_test, 'y_test': y_test}

        n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features, bootstrap = args
        modelo =  RandomForestClassifier(n_estimators=1, max_depth=max_depth, min_samples_split=min_samples_split,
                        min_samples_leaf=min_samples_leaf, max_features=max_features, bootstrap=bootstrap, 
                                    random_state=17, warm_start=True, n_jobs=1)
        for n in range(1, control.total_pasos+1):
            modelo.n_estimators = n
            modelo.fit(X_train, y_train)
            reporte(n)
        modelo_dicc['modelo'] = modelo
        modelo_dicc['y_pred'] = modelo.predict(X_test)
        modelo_dicc.update({'tipo_modelo': 'RandomForestClassifier', 'random_state': 17,
                    'test_size': 0.25, 'feature_names': columnas,
                    'target_column': 'hospitalizacion', 'preprocessing': None})

        return modelo_dicc

    @Decorador.progreso
    @staticmethod
    def potenciacion_gradiente_extremo(*args, **kwargs):
        """
        Entrena un modelo de potenciación extrema del gradiente usando los hiperparámetros aportados en args y devuelve un diccionario que contiene el modelo, X_test e y_test.
        
        :param args: Hiperparámetros para entrenar el modelo.
        :param kwargs: Otros parámetros relativos a Trabajador.
        """
        from sklearn.model_selection import train_test_split
        import xgboost
        from xgboost import XGBClassifier

        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        n_estimators, learning_rate, max_depth, min_child_weight, subsample, colsample_bytree, reg_alpha, reg_lambda = args

        class BarraProgresoLlamada(xgboost.callback.TrainingCallback):
            def after_iteration(self, model, epoch, evals_log):
                reporte(epoch+1)
                return False

        df = Limpieza.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        columnas = X.columns.tolist()
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17, stratify=y)
        X_fit, X_val, y_fit, y_val = train_test_split(
            X_train, y_train, test_size=0.2, random_state=17, stratify=y_train)
        modelo_dicc = {'X_test': X_test, 'y_test': y_test}

        modelo = XGBClassifier(n_estimators=n_estimators, learning_rate=learning_rate,
                       max_depth=max_depth, min_child_weight=min_child_weight, 
                       subsample=subsample, colsample_bytree=colsample_bytree, 
                       reg_alpha=reg_alpha, reg_lambda=reg_lambda,
                                callbacks=[BarraProgresoLlamada()], eval_metric='auc', early_stopping_rounds=10)
        modelo.fit(X_fit, y_fit,
                eval_set=[(X_fit, y_fit), (X_val, y_val)])
        modelo_dicc['modelo'] = modelo
        modelo_dicc['y_pred'] = modelo.predict(X_test)
        modelo_dicc.update({'tipo_modelo': 'XGBClassifier', 'random_state': 17,
                    'test_size': 0.25, 'validation_size': 0.2,
                    'feature_names': columnas, 'target_column': 'hospitalizacion',
                    'preprocessing': None})
        return modelo_dicc
    
    @staticmethod
    def validacion_cruzada_cuadricula_mitad(nom: str, **kwargs):
        """
        Entrena el modelo solicitado mediante HalvingGridSearchCV usando los hiperparámetros contenidos en Modelo.params() y devuelve un diccionario que contiene el modelo, X_test e y_test.
        
        :param nom: Nombre abreviado del tipo de modelo a entrenar.
        :type nom: str
        :param kwargs: Otros parámetros relativos a Trabajador.
        """
        from sklearn.experimental import enable_halving_search_cv
        from sklearn.model_selection import HalvingGridSearchCV
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from xgboost import XGBClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.pipeline import Pipeline
        from joblib import parallel_backend

        modelo_dicc = {}
        df = Limpieza.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        columnas = X.columns.tolist()
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17, stratify=y)
        modelo_dicc['y_test'] = y_test

        parametros = Modelo.params(nom)

        if nom == 'reglog':
            modelo = Pipeline([
                ('scaler', StandardScaler()),
                ('model', LogisticRegression(random_state=17, n_jobs=1, class_weight='balanced'))
            ])
            parametros = {'model__l1_ratio': parametros['l1_ratio'],
                          'model__C': parametros['C'],
                          'model__max_iter': parametros['max_iter'],
                          'model__solver': ['saga'],
                          'model__penalty': ['elasticnet']}
            mod = Pipeline
        elif nom == 'bosque':
            modelo = RandomForestClassifier(max_samples=0.5, random_state=17, n_jobs=1)
            mod = RandomForestClassifier
        elif nom == 'xgb':
            modelo = XGBClassifier(tree_method='hist', device='cpu', random_state=17, n_jobs=1)
            mod = XGBClassifier


        # Solamente busco hiperparámetros
        hgscv = HalvingGridSearchCV(
                modelo, 
                parametros, 
                factor=4, 
                resource='n_samples', 
                max_resources=len(X_train),
                random_state=17,
                cv=3,
                n_jobs=-1, 
                refit=False,
                aggressive_elimination=True,
                verbose=3)
        # Se mantienen los estimadores individuales con un único hilo (n_jobs) durante la búsqueda
        # para que HalvingGridSearchCV controle el paralelismo. 
        with parallel_backend('threading'):
            hgscv.fit(X_train, y_train)

        #Escojo la mejor configuración y entreno con ella el mejor modelo
        mejores = hgscv.best_params_
        if nom == 'reglog':
            modelo_final = Pipeline([
                ('scaler', StandardScaler()),
                ('model', LogisticRegression(random_state=17, n_jobs=-1, class_weight='balanced'))
            ])
            modelo_final.set_params(**mejores)
            modelo_final.fit(X_train, y_train)
            modelo_dicc['X_test'] = X_test
        else:
            modelo_final = mod(**mejores, random_state=17, n_jobs=-1)
            if nom == 'xgb':
                X_fit, X_val, y_fit, y_val = train_test_split(
                    X_train, y_train, test_size=0.2, random_state=17, stratify=y_train)
                modelo_final = XGBClassifier(**mejores, random_state=17, n_jobs=-1, eval_metric='auc', early_stopping_rounds=10)
                modelo_final.fit(X_fit, y_fit,
                                eval_set=[(X_fit, y_fit), (X_val, y_val)])
            else:
                modelo_final.fit(X_train, y_train)
            modelo_dicc['X_test'] = X_test
        print("Mejor modelo: ", modelo_final)

        modelo_dicc['modelo'] = modelo_final
        modelo_dicc['y_pred'] = modelo_final.predict(modelo_dicc['X_test'])
        modelo_dicc.update({'tipo_modelo': 'LogisticRegression' if nom == 'reglog' else type(modelo_final).__name__,
                    'random_state': 17, 'test_size': 0.25,
                    'feature_names': columnas, 'target_column': 'hospitalizacion',
                    'preprocessing': {'scaler': 'StandardScaler'} if nom == 'reglog' else None})
        return modelo_dicc

    @staticmethod
    def guardar_modelo(modelo: object, kpis: dict, metadatos: dict = None) -> str:
        """
        Guarda el modelo actual en formato .ubj si es XGBoost, o .pkl en los otros casos.
        
        :param modelo: Modelo a guardar.
        :type modelo: object
        :param kpis: Diccionario que contiene la exactitud, precisión, sensibilidad y F1 del modelo.
        :type kpis: dict
        :return: Mensaje de éxito o fallo en el guardado.
        :rtype: str
        """
        import datetime
        import os
        import joblib
        import xgboost
        import sklearn
        import json
        import numpy as np
        import pandas as pd
        from sklearn.pipeline import Pipeline

        hora_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        es_pipeline_reglog = isinstance(modelo, Pipeline)
        nom_modelo = 'LogisticRegression' if es_pipeline_reglog else type(modelo).__name__

        raiz_proyecto = os.path.dirname(os.path.dirname(__file__))
        url_resultados = os.path.join(raiz_proyecto, "resultados")
        if not os.path.exists(url_resultados):
            os.makedirs(url_resultados, exist_ok=True)
        url_modelo = os.path.join(url_resultados, f"{nom_modelo}_{hora_actual}")
        os.makedirs(url_modelo, exist_ok=True)
        nom_archivo_specs = f'specs_{nom_modelo}_{hora_actual}.json'
        url_archivo_specs = os.path.join(url_modelo, nom_archivo_specs)
        print(url_archivo_specs)

        if nom_modelo == 'XGBClassifier':
            nom_archivo_modelo = f'{nom_modelo}_{hora_actual}.ubj'
            url_archivo_modelo = os.path.join(url_modelo, nom_archivo_modelo)
            parametros = modelo.get_xgb_params()
            modelo.save_model(url_archivo_modelo)
            try:
                xgboost.XGBClassifier().load_model(url_archivo_modelo)
                mensaje = "El modelo se guardó correctamente y es válido."
            except Exception as e:
                mensaje = f"El archivo se guardó correctamente pero el modelo es inválido: {e}"
        elif nom_modelo in {'LogisticRegression', 'RandomForestClassifier'}:
            nom_archivo_modelo = f'{nom_modelo}_{hora_actual}.pkl'
            url_archivo_modelo = os.path.join(url_modelo, nom_archivo_modelo)
            estimador = modelo.named_steps['model'] if es_pipeline_reglog else modelo
            parametros = estimador.get_params()
            joblib.dump(modelo, url_archivo_modelo)
            try:
                joblib.load(url_archivo_modelo)
                mensaje = "El modelo se guardó correctamente y es válido."
            except Exception as e:
                mensaje = f"El archivo se guardó correctamente pero el modelo es inválido: {e}"
        else:
            raise ValueError(f'Tipo de modelo no soportado: {nom_modelo}')

        df = Leer_Datos.abrir_csv()
        proporcion = df['hospitalizacion'].value_counts(normalize=True)
        versiones = {'scikit_learn': sklearn.__version__}
        if nom_modelo == 'XGBClassifier':
            versiones['xgboost'] = xgboost.__version__

        campos_excluidos = {'modelo', 'y_pred', 'X_test', 'y_test', 'kpis', 'metricas'}
        entrenamiento = ({clave: valor for clave, valor in metadatos.items()
                  if clave not in campos_excluidos}
                 if metadatos else {})

        documento = {
            'model': {
                'name': nom_modelo,
                'artifact': nom_archivo_modelo,
                'pipeline': es_pipeline_reglog,
                'parameters': parametros
            },
            'kpis': kpis,
            'training': entrenamiento,
            'software_versions': versiones,
            'dataset': {
                'entries': len(df),
                'target_distribution': proporcion.to_dict()
            }
        }

        def convertir_json(valor):
            if isinstance(valor, (pd.Series, pd.Index)):
                return valor.tolist()
            if isinstance(valor, pd.DataFrame):
                return valor.to_dict()
            if isinstance(valor, np.ndarray):
                return valor.tolist()
            if isinstance(valor, np.generic):
                return valor.item()
            return str(valor)

        with open(url_archivo_specs, 'w', encoding='UTF-8') as f:
            json.dump(documento, f, ensure_ascii=False, indent=4, default=convertir_json)

        print(mensaje)
        return mensaje

class Evaluacion:
    @staticmethod
    def kpis(y_test: Series, y_pred: ndarray) -> dict:
        """
        Evalúa el modelo en exactitud, precisión, sensibilidad y F1 y devuélvelos en forma de diccionario.
        
        :param y_test: Variable objetivo de prueba.
        :type y_test: Series
        :param y_pred: Variable objetivo predicha por el modelo.
        :type y_pred: ndarray
        :return: Diccionario que contiene la exactitud, precisión, sensibilidad y F1 del modelo.
        :rtype: dict
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        import numpy as np
        
        kpis = {}
        punteria = accuracy_score(y_test, y_pred)
        kpis['Exactitud'] = punteria
        precision = precision_score(y_test, y_pred, zero_division=np.nan)
        kpis['Precisión'] = precision
        llamada = recall_score(y_test, y_pred, zero_division=np.nan)
        kpis['Sensibilidad'] = llamada
        f1 = f1_score(y_test, y_pred, zero_division=np.nan)
        kpis['F1'] = f1

        return kpis
    
    @staticmethod
    def eval_modelo(modelo_dict: dict, axes: list[Axes], nom: str) -> tuple [tuple[Axes], dict[str, float]]:
        """
        Evalúa el modelo y extrae la matriz de confusión, puntuación AUC y si el modelo es LogReg, evalúa la pérdida logarítmica, y en el resto de casos, la importancia de características.
        
        :param modelo_dict: Diccionario que contiene el modelo, X_test, y_test e y_pred.
        :type modelo_dict: dict
        :param axes: Lista de objetos tipo Ax donde dibujaremos las gráficas.
        :type axes: list[Axes]
        :param nom: Nombre del tipo de modelo.
        :type nom: str
        :return: Tupla que contiene los Axes dibujados y las métricas del modelo.
        :rtype: tuple [tuple [Axes], dict]
        """
        from servicios.graficos import EvaluacionGraf as eg

        ax_sup, ax_med, ax_inf = axes

        if nom == 'LogisticRegression':
            metricas = {}
            cm =  Analisis.confusion_matrix_modelo(modelo_dict)
            metricas['matriz_confusion'] =  cm
            ax_sup = eg.matriz_conf(cm, ax_sup)

            log_losses = Analisis.log_loss_modelo(modelo_dict)
            metricas['log_losses'] = log_losses
            ax_med = eg.logloss_clase(log_losses, ax_med)

            roc_auc = Analisis.roc_auc_modelo(modelo_dict)
            metricas['auc'] = roc_auc[2]
            ax_inf = eg.curva_roc(*roc_auc, ax_inf)

            return (ax_sup, ax_med, ax_inf), metricas

        elif nom == 'RandomForestClassifier' or nom == 'XGBClassifier':
            metricas = {}
            cm =  Analisis.confusion_matrix_modelo(modelo_dict)
            metricas['matriz_confusion'] =  cm
            ax_sup = eg.matriz_conf(cm, ax_sup)

            import_carac_df = Analisis.importancia_caracteristicas_modelo(modelo_dict)
            metricas['importancia_carac'] = import_carac_df
            ax_med = eg.importancia_carac(import_carac_df, ax_med)

            roc_auc = Analisis.roc_auc_modelo(modelo_dict)
            metricas['auc'] = roc_auc[2]
            ax_inf = eg.curva_roc(*roc_auc, ax_inf)

            return (ax_sup, ax_med, ax_inf), metricas