from servicios.analisis import Analisis
from servicios.trabajador import Decorador
class Modelo():
    from pandas import DataFrame
    from numpy import ndarray
    @staticmethod
    def params(modelo: str) -> dict:
        """
        Contén y devuelve los hiperparámetros posibles para el entrenamiento de cada modelo.
        
        :param modelo: Nombre abreviado del modelo a entrenar.
        :type modelo: str
        :return: Diccionario con todos los hiperparámetros posibles del modelo solicitado.
        :rtype: dict
        """
        import numpy as np
        parametros_reglog = {'l1_ratio':['1.0','0.5','0'],
                             'C':['0.01', '0.1', '1.0', '10'],
                             'solver':['liblinear','newton-cg','saga'],
                             'max_iter':['100','1000','10000']}
        
        parametros_bosque = {'n_estimators':['100','200'],
                             'max_depth':['5','10'],
                             'min_samples_split':['10','25','50'],
                             'min_samples_leaf':['1','5','10','20'],
                             'max_features':['1', '3', '5'],
                             'bootstrap':['True','False']}
        
        parametros_xgb = {'n_estimators':['100','300'],
                          'learning_rate':['0.05','0.15', '0.3'],
                          'max_depth':['5','7'],
                          'min_child_weight':['1','3'],
                          'subsample':['0.6','0.9'],
                          'colsample_bytree':['0.6','0.9'],
                          'reg_alpha':['0','1'],
                          'reg_lambda':['0','1']}
        
        switch = {'reglog':'parametros_reglog',
                  'bosque':'parametros_bosque',
                  'xgb':'parametros_xgb'}
        
        return eval(switch[modelo])
    
    
    @Decorador.progreso
    @staticmethod
    def reglog(*args, **kwargs):
        """
        Entrena un modelo de regresión logística usando los hiperparámetros aportados en args y devuelve un diccionario que contiene el modelo, X_test e y_test.
        
        :param args: Hiperparámetros para entrenar el modelo.
        :param kwargs: Otros parámetros relativos a Trabajador.
        """
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression

        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        scaler_X= StandardScaler()
        X_sc = scaler_X.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_sc, y, random_state=17)
        modelo_dicc['X_test'] = X_test
        modelo_dicc['y_test'] = y_test

        l1_ratio = float(args[0]) if args[0] != 'None' else None
        C = float(args[1])
        solver = args[2]
        max_iter = int(args[3])

        modelo = LogisticRegression(l1_ratio=l1_ratio, C=C, solver=solver, max_iter=1, class_weight='balanced')
        for n in range(1, max_iter+1):
            modelo.fit(X_train, y_train)
            reporte(n)
            modelo_dicc['modelo'] = modelo
            return modelo_dicc

    @Decorador.progreso
    @staticmethod
    def bosque(*args, **kwargs):
        """
        Entrena un modelo de bosque aleatorio usando los hiperparámetros aportados en args y devuelve un diccionario que contiene el modelo, X_test e y_test.
        
        :param args: Hiperparámetros para entrenar el modelo.
        :param kwargs: Otros parámetros relativos a Trabajador.
        """
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier

        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        params = []
        for arg in args:
            try:
                params.append(int(arg))
            except ValueError:
                params.append(bool(arg))

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)
        modelo_dicc['X_test'] = X_test
        modelo_dicc['y_test'] = y_test

        lista_params = [int(item) for item in args[:-1]]
        lista_params.append(bool(args[-1]))
        modelo =  RandomForestClassifier(n_estimators=1, max_depth=lista_params[1], min_samples_split=lista_params[2],
                                    min_samples_leaf=lista_params[3], max_features=lista_params[4], bootstrap=lista_params[5], 
                                    random_state=17, warm_start=True, n_jobs=1)
        for n in range(1, control.total_pasos+1):
            modelo.n_estimators = n
            modelo.fit(X_train, y_train)
            reporte(n)
        modelo_dicc['modelo'] = modelo

        return modelo_dicc

    @Decorador.progreso
    @staticmethod
    def xgb(*args, **kwargs):
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

        parametros = []
        for n, arg in enumerate(args):
            if n in [0, 2, 3, 6, 7]:
                parametros.append(int(arg))
            else:
                parametros.append(float(arg))

        class BarraProgresoLlamada(xgboost.callback.TrainingCallback):
            def after_iteration(self, model, epoch, evals_log):
                reporte(epoch+1)
                return False

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)
        modelo_dicc['X_test'] = X_test
        modelo_dicc['y_test'] = y_test

        modelo = XGBClassifier(n_estimators=control.total_pasos, learning_rate=parametros[1],
                               max_depth=parametros[2], min_child_weight=parametros[3], 
                               subsample=parametros[4], colsample_bytree=parametros[5], 
                               reg_alpha=parametros[6], reg_lambda=parametros[7],
                                callbacks=[BarraProgresoLlamada()], eval_metric='auc', early_stopping_rounds=10)
        modelo.fit(X_train, y_train,
                    eval_set=[(X_train, y_train), (X_test, y_test)])
        modelo_dicc['modelo'] = modelo
        return modelo_dicc
    
    @staticmethod
    def gs_cv(nom: str, **kwargs):
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
        from joblib import parallel_backend

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)
        modelo_dicc['X_test'] = X_test
        modelo_dicc['y_test'] = y_test

        parametros = Modelo.params(nom)

        floats = ['l1_ratio','C', 'learning_rate','subsample','colsample_bytree']
        enteros = ['max_iter', 'n_estimators', 'max_depth','min_samples_split', 'min_samples_leaf','max_features',
                    'min_child_weight','reg_alpha','reg_lambda']
        booleanos = ['bootstrap']

        parametros_convertidos = {}
        for k, v in parametros.items():
            if k in floats:
                lista = []
                for item in v:
                    lista.append(float(item))
                parametros_convertidos[k] = lista
            elif k in enteros:
                lista = []
                for item in v:
                    lista.append(int(item))
                parametros_convertidos[k] = lista
            elif k in booleanos:
                lista = []
                for item in v:
                    lista.append(bool(item))
                parametros_convertidos[k] = lista
            else:
                if v == 'None':
                    parametros_convertidos[k] = None
                else:
                    parametros_convertidos[k] = v
        if nom == 'reglog':
            modelo = LogisticRegression(random_state=17, n_jobs=1)
            mod = LogisticRegression
        elif nom == 'bosque':
            modelo = RandomForestClassifier(max_samples=0.5, random_state=17, n_jobs=1)
            mod = RandomForestClassifier
        elif nom == 'xgb':
            modelo = XGBClassifier(tree_method='hist', device='cpu', random_state=17, n_jobs=1)
            mod = XGBClassifier

        
        hgscv = HalvingGridSearchCV(
                modelo, 
                parametros_convertidos, 
                factor=4, 
                resource='n_samples', 
                max_resources=len(X_train),
                random_state=17,
                cv=3,
                n_jobs=-1, 
                refit=False,
                aggressive_elimination=True,
                verbose=3)
        with parallel_backend('threading'):
            hgscv.fit(X_train, y_train)

        mejores = hgscv.best_params_
        modelo_final = mod(**mejores, random_state=17, n_jobs=-1)
        if nom == 'xgb':
            modelo_final = XGBClassifier(**mejores, random_state=17, n_jobs=-1, eval_metric='auc', early_stopping_rounds=10, gamma=0.2)
            modelo_final.fit(X_train, y_train,
                            eval_set=[(X_train, y_train), (X_test, y_test)])
        elif nom == 'reglog':
            modelo_final = LogisticRegression(**mejores, random_state=17, n_jobs=-1, class_weight='balanced')
            modelo_final.fit(X_train, y_train)
        else:
            modelo_final.fit(X_train, y_train)
        print("Mejor modelo: ", modelo_final)

        modelo_dicc['modelo'] = modelo_final
        return modelo_dicc

    @staticmethod
    def guardar_modelo(modelo: object, kpis: dict) -> str:
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

        hora_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_modelo = type(modelo).__name__

        
        nom_archivo_specs = f'specs_{nom_modelo}_{hora_actual}.txt'
        url_archivo_specs = os.path.join(os.path.dirname(__file__), nom_archivo_specs)

        if nom_modelo == 'XGBClassifier':
            nom_archivo_modelo = f'{nom_modelo}_{hora_actual}.ubj'
            url_archivo_modelo = os.path.join(os.path.dirname(__file__), nom_archivo_modelo)
            parametros = modelo.get_xgb_params()
            modelo.save_model(url_archivo_modelo)
            if os.path.exists(url_archivo_modelo) and os.path.getsize(url_archivo_modelo) > 0:
                try:
                    nuevo_modelo = xgboost.XGBClassifier()
                    nuevo_modelo.load_model(url_archivo_modelo)
                    mensaje = "El modelo se guardó correctamente y es válido."
                except Exception as e:
                    mensaje = f"El archivo se guardó correctamente pero el modelo es inválido: {e}"
            else:
                mensaje = f"Error: El archivo '{url_archivo_modelo}' no se encontró o está vacío."

        elif nom_modelo == 'LogisticRegression' or nom_modelo == 'RandomForestClassifier':
            nom_archivo_modelo = f'{nom_modelo}_{hora_actual}.pkl'
            url_archivo_modelo = os.path.join(os.path.dirname(__file__), nom_archivo_modelo)
            parametros = modelo.get_params()
            joblib.dump(modelo, url_archivo_modelo)
            if os.path.exists(url_archivo_modelo) and os.path.getsize(url_archivo_modelo) > 0:
                try:
                    joblib.load(url_archivo_modelo)
                    mensaje = "El modelo se guardó correctamente y es válido."
                except Exception as e:
                    mensaje = f"El archivo se guardó correctamente pero el modelo es inválido: {e}"
            else:
                mensaje = f"Error: El archivo '{url_archivo_modelo}' no se encontró o está vacío."

        specs = ''
        specs += f'Parámetros del modelo {nom_modelo}:\n'
        for k in parametros:
            if parametros[k] is not None:
                specs += f'{k}: {parametros[k]}\n'
        specs += f'\nIndicadores clave de rendimiento (KPIs):\n'
        for k in kpis:
            specs += f'{k}: {round(kpis[k], 4)}\n'

        if nom_modelo == 'LogisticRegression' or nom_modelo == 'RandomForestClassifier':
            specs += f'\nVersión de Scikit-Learn: {sklearn.__version__}'
        elif nom_modelo == 'XGBClassifier':
            specs += f'\nVersión de XGBoost: {xgboost.__version__}'
            
        with open(url_archivo_specs, 'w', encoding='UTF-8') as f:
            f.write(specs)

        print(mensaje)
        return mensaje

class Evaluacion:
    from numpy import ndarray
    from pandas import Series
    from matplotlib.axes import Axes
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