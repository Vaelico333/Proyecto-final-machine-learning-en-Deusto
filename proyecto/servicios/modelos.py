from servicios.analisis import *
from servicios.trabajador import Trabajador, Decorador
class Modelo():
    def params(modelo) -> dict:

        parametros_reglog = {'penalty':['l1','l2','elasticnet','None'],
                             'C':['0.001', '0.01', '0.1', '1.0'],
                             'solver':['liblinear','newton-cg','saga'],
                             'max_iter':['10','50','100']}
        
        parametros_bosque = {'n_estimators':['100','200'],
                             'max_depth':['5','10'],
                             'min_samples_split':['10','25','50'],
                             'min_samples_leaf':['1','5','10','20'],
                             'max_features':['3','5','9','12'],
                             'bootstrap':['True','False']}
        
        parametros_xgb = {'n_estimators':['100','200'],
                          'learning_rate':['0.01', '0.1', '0.2', '0.3'],
                          'max_depth':['5','7'],
                          'min_child_weight':['1','3','5','7'],
                          'subsample':['0.6', '0.7', '0.8', '0.9'],
                          'colsample_bytree':['0.6', '0.7', '0.8', '0.9'],
                          'reg_alpha':['0','1'],
                          'reg_lambda':['0','1']}
        
        switch = {'reglog':'parametros_reglog',
                  'bosque':'parametros_bosque',
                  'xgb':'parametros_xgb'}
        
        return eval(switch[modelo])
    

    @Decorador.progreso
    def reglog(*args, **kwargs):

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
        modelo_dicc['scaler_X'] = scaler_X
        X_train, X_test, y_train, y_test = train_test_split(X_sc, y, random_state=17)
        modelo_dicc['X_test'] = X_test
        modelo_dicc['y_test'] = y_test

        penalty = args[0][0]
        C = float(args[0][1])
        solver = args[0][2]
        max_iter = int(args[0][3])

        modelo = LogisticRegression(penalty=penalty, C=C, solver=solver, max_iter=1)
        for n in range(1, max_iter+1):
            modelo.fit(X_train, y_train)
            reporte(n)
            modelo_dicc['modelo'] = modelo
            return modelo_dicc

    @Decorador.progreso
    def bosque(*args, **kwargs):

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
                                    random_state=17)
        for n in range(1, control.total_pasos+1):
            modelo.n_estimators = n
            modelo.fit(X_train, y_train)
            reporte(n)
        modelo_dicc['modelo'] = modelo

        return modelo_dicc

    @Decorador.progreso
    def xgb(*args, **kwargs):

        from sklearn.model_selection import train_test_split
        import xgboost
        from xgboost import XGBClassifier

        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        params = []
        for n, arg in enumerate(args):
            if n in [0, 2, 3, 6, 7]:
                params.append(int(arg))
            else:
                params.append(float(arg))

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

        modelo = XGBClassifier(kwargs=kwargs, n_estimators=control.total_pasos, callbacks=[BarraProgresoLlamada()])
        modelo.fit(X_train, y_train)
        modelo_dicc['modelo'] = modelo
        return modelo_dicc
    
    @Decorador.progreso
    def gs_cv(nom, **kwargs):

        from sklearn.experimental import enable_halving_search_cv
        from sklearn.model_selection import HalvingGridSearchCV, ParameterGrid
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from xgboost import XGBClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import make_scorer, accuracy_score
        from joblib import parallel_backend

        reporte = kwargs['reporte_progreso']
        control = kwargs['objeto_control']

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)
        modelo_dicc['mapa'] = mapa

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)
        modelo_dicc['X_test'] = X_test
        modelo_dicc['y_test'] = y_test

        parametros = Modelo.params(nom)

        floats = ['C', 'learning_rate','subsample','colsample_bytree']
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
            modelo = LogisticRegression(random_state=17, n_jobs=-1)
            mod = LogisticRegression
        elif nom == 'bosque':
            modelo = RandomForestClassifier(max_samples=0.5, random_state=17, n_jobs=6)
            mod = RandomForestClassifier
        elif nom == 'xgb':
            modelo = XGBClassifier(tree_method='hist', device='cpu', random_state=17, n_jobs=-1)
            mod = XGBClassifier

        n_candidatos = len(ParameterGrid(parametros_convertidos))
        control.total_pasos = n_candidatos * 1.5

        contador = {'actual':0}
        def puntuador_progreso(y_true, y_pred):
            contador['actual'] += 1
            reporte(contador['actual'])
            return accuracy_score(y_true, y_pred)
        
        hgscv = HalvingGridSearchCV(
                modelo, 
                parametros_convertidos, 
                factor=3, 
                resource='n_samples', 
                max_resources=len(X_train),
                random_state=17,
                cv=3,
                n_jobs=1, 
                refit=False)
        
        hgscv.scoring = make_scorer(puntuador_progreso)
        with parallel_backend('threading'):
            hgscv.fit(X_train, y_train)

        mejores = hgscv.best_params_
        modelo_final = mod(**mejores, random_state=17, n_jobs=-1)
        modelo_final.fit(X_train, y_train)
        print("Mejor: ", modelo_final)

        modelo_dicc['modelo'] = modelo_final
        return modelo_dicc

class Evaluacion:
    pass
