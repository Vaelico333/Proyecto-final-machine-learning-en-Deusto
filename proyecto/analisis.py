class analisis():
    import pandas as pd
    def operacion_str(num: float, *args) -> float:

        import operator
        import re
        operadores = {
            '/' : operator.truediv,
            '*' : operator.mul,
            '+' : operator.add,
            '-' : operator.sub
        }
        patron = r'^([+\-*/]{1})(\d+\.?\d*)$'
        for factor in args:
            match = re.match(patron, factor)
            operacion, numero = match.groups()
            num = operadores[operacion](num, float(numero))
        return num

    def cadena_a_numero(df: pd.DataFrame, col: str) -> pd.DataFrame:
        
        columnas = {
            'peso':'peso_kg',
            'altura':'altura_m',
            'glucosa':'glucosa_mg_dL',
            'presion_arterial':'presion_sistolica'}
        
        unidades_estandar = ['kg', 'mg/dL']
        unidades_no_estandar = ['lb', 'cm', 'inch', 'mmol/L']

        factores_conversion = {
        'lb' :  '/0.45359237',
        'cm' : '/100',
        'inch' : '*0.0254',
        'mmol/L' : '*17.5 +3.75'}
        if col not in columnas.keys():
            return df
        
        df[columnas[col]] = df[col].astype(str)
        
        valores_finales = []
        if col == 'presion_arterial':
            for valor in df[columnas[col]]:
                valor_limpio = valor.split('/')[0]
                valores_finales.append(valor_limpio)
        else:
            for valor in df[columnas[col]]:
                    agregado = False
                    if not agregado:
                        for unidad in unidades_estandar:
                                if unidad in valor:
                                    valor_limpio = valor.replace(f' {unidad}', '')
                                    valores_finales.append(valor_limpio)
                                    agregado = True
                                    break
                    if not agregado:
                        for unidad in unidades_no_estandar:
                                if unidad in valor:
                                    valor_num = valor.replace(f' {unidad}', '')
                                    valor_limpio = round(analisis.operacion_str(float(valor_num), *factores_conversion[unidad].split()), 2)
                                    valores_finales.append(valor_limpio)
                                    agregado = True
                                    break
                    if not agregado:
                        valores_finales.append(valor)
        df[columnas[col]] = valores_finales
        df[columnas[col]] = df[columnas[col]].astype(float)
        return df
