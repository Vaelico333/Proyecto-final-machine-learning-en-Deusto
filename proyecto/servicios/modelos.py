from servicios.analisis import *
from servicios.trabajador import Trabajador
class Modelo():
    def params(modelo) -> dict:

        parametros_reglog = {'penalty':['l1','l2','elasticnet','None'],
                             'C':['0.001', '0.01', '0.1', '1.0'],
                             'solver':['liblinear','newton-cg','saga'],
                             'max_iter':['10','50','100']}
        
        parametros_bosque = {'n_estimators':['100','200','300','400'],
                             'max_depth':['5','10','15','20'],
                             'min_samples_split':['10','25','50','100'],
                             'min_samples_leaf':['1','5','10','20'],
                             'max_features':['3','5','9','12'],
                             'bootstrap':['True','False']}
        
        parametros_xgb = {'n_estimators':['100','200','350','500'],
                          'learning_rate':['0.01', '0.1', '0.2', '0.3'],
                          'max_depth':['3','5','7','10'],
                          'min_child_weight':['1','3','5','7'],
                          'subsample':['0.6', '0.7', '0.8', '0.9'],
                          'colsample_bytree':['0.6', '0.7', '0.8', '0.9'],
                          'reg_alpha':['0','1'],
                          'reg_lambda':['0','1']}
        
        switch = {'reglog':'parametros_reglog',
                  'bosque':'parametros_bosque',
                  'xgb':'parametros_xgb'}
        
        return eval(switch[modelo])
    
    def reglog(penalty, C, solver, max_iter, **kwargs):

        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)
        modelo_dicc['mapa'] = mapa

        scaler_X= StandardScaler()
        X_sc = scaler_X.fit_transform(X)
        modelo_dicc['scaler_X'] = scaler_X
        X_train, X_test, y_train, y_test = train_test_split(X_sc, y, random_state=17)

        if not kwargs:
            modelo = LogisticRegression(penalty=penalty, C=float(C), solver=solver, max_iter=int(max_iter), random_state=17)
        else:
            if kwargs['penalty'] == 'None':
                kwargs['penalty'] = None
            modelo = LogisticRegression(kwargs)
        modelo.fit(X_train, y_train)
        modelo_dicc['modelo'] = modelo

        return modelo_dicc

    def bosque(*args, **kwargs):

        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier

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
        modelo_dicc['mapa'] = mapa

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)

        if not kwargs:
            modelo = RandomForestClassifier(n_estimators=params[0], max_depth=params[1], min_samples_split=params[2],
                                        min_samples_leaf=params[3], max_features=params[4], bootstrap=params[5], random_state=17)
        else:
            modelo =  RandomForestClassifier(kwargs)
        modelo.fit(X_train, y_train)
        modelo_dicc['modelo'] = modelo

        return modelo_dicc

    def xgb(*args, **kwargs):

        from sklearn.model_selection import train_test_split
        from xgboost import XGBClassifier

        params = []
        for n, arg in enumerate(args):
            if n in [0, 2, 3, 6, 7]:
                params.append(int(arg))
            else:
                params.append(float(arg))

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)
        modelo_dicc['mapa'] = mapa

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)
        if not kwargs:
            modelo = XGBClassifier(n_estimators=params[0], learning_rate=params[1], max_depth=params[2], min_child_weight=params[3],
                                subsample=params[4], colsample_bytree=params[5], reg_alpha=params[6], reg_lambda=params[7])
        else:
            modelo = XGBClassifier(kwargs=kwargs)
        modelo.fit(X_train, y_train)
        modelo_dicc['modelo'] = modelo
        return modelo_dicc
    
    def gs_cv(nom):

        from sklearn.model_selection import RandomizedSearchCV
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from xgboost import XGBClassifier
        from sklearn.model_selection import train_test_split

        modelo_dicc = {}
        df = Analisis.limpiar_errores()
        X = df.drop(columns='hospitalizacion')
        mapa = {'Sí':1, 'No':0}
        y = df['hospitalizacion'].map(mapa)
        modelo_dicc['mapa'] = mapa

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17)

        parametros = Modelo.params(nom)
        if nom == 'reglog':
            #modelo = LogisticRegression(random_state=17)
            floats = ['C']
            enteros = ['max_iter']
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
                else:
                    parametros_convertidos[k] = v
            modelo = LogisticRegression(random_state=17)

        elif nom == 'bosque':
            enteros = ['n_estimators', 'max_depth','min_samples_split', 'min_samples_leaf','max_features']
            booleanos = ['bootstrap']
            parametros_convertidos = {}
            for k, v in parametros.items():
                if k in enteros:
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
                    parametros_convertidos[k] = v
            modelo = RandomForestClassifier(random_state=17)

        elif nom == 'xgb':
            enteros = ['n_estimators','max_depth','min_child_weight','reg_alpha','reg_lambda']
            floats = ['learning_rate','subsample','colsample_bytree']
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
                else:
                    parametros_convertidos[k] = v
            modelo = XGBClassifier(random_state=17)

        gscv = RandomizedSearchCV(modelo, parametros_convertidos)
        gscv.fit(X_train, y_train)
        mejores = gscv.best_params_
        print("Mejores parámetros:", gscv.best_params_)

        modelo_dicc['modelo'] = modelo
        pass

class Evaluacion:
    pass
