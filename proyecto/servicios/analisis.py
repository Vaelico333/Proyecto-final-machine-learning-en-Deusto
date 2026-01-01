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
    import pandas as pd
    def operacion_str(num: float, *args) -> float:
        """
        Ejecuta la operación u operaciones contenidas en args sobre num.
        
        :param num: Número sobre el que realizar la conversión
        :type num: float
        :param args: Conjunto de operaciones a aplicar, en forma de strings con operador+número sin espacios
        :return: Devuelve num convertido a la nueva unidad de medida
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

    def cadena_a_numero(df: pd.DataFrame, cols: list = None, modo: str = 'num') -> pd.DataFrame:
        """
        Convierte las columnas con medidas de cadena de caracteres a número de coma flotante, 
        elimina el nombre de la unidad y 
        homogeneiza los datos convirtiendo a las unidades estándar.
        
        :param df: DataFrame de pandas a modificar
        :type df: DataFrame
        :param col: Nombre de las columnas a transformar
        :type col: tuple
        :param modo: Indica qué se retornará: todos los datos (total), sólo la columna (columna) o sólo los nuevos datos (num)
        :type modo: str
        :return: DataFrame modificado
        :rtype: DataFrame
        """
        import pandas as pd
        # Creamos un diccionario para otorgar una nueva columna numérica 
        # por cada vieja columna categórica
        columnas = {
            'peso':'peso_kg',
            'altura':'altura_m',
            'glucosa':'glucosa_mg_dL',
            'presion_arterial':'presion_sistolica'}
        
        # Dos listas: una contiene las unidades objetivo, y la otra las no deseadas
        unidades_estandar = ['kg', 'mg/dL']
        unidades_no_estandar = ['lb', 'cm', 'inch', 'mmol/L']

        # Factores para convertir de libras a kg, cm a m, pulgadas a m y mmol/L a mg/dL
        factores_conversion = {
            'lb' :  '/0.45359237',
            'cm' : '/100',
            'inch' : '*0.0254',
            'mmol/L' : '*17.5 +3.75'}

        if not cols:
            cols = list(df.columns)
        # Contamos cuántas veces aparece una unidad estándar y cuántas una no estándar 
        # la idea es usarlo solo cuando sea una columna y no un DF completo
        estandar = 0
        no_estandar = 0
        # Comprobamos que las columnas solicitadas sean de las convertibles, 
        # y si no lo son, terminamos la función y devolvemos False
        for col in cols:
            if col not in columnas.keys():
                continue
            
            # Nos aseguramos de convertir todo a cadena de caracteres para 
            # evitar problemas con NaN y 0 introducidos como errores
            df[columnas[col]] = df[col].astype(str)
            
            # Esta lista contendrá la columna ya convertida en numérica
            valores_finales = []
            # Presión arterial tiene un formato especial, y requiere otro tratamiento
            if col == 'presion_arterial':
                for valor in df[columnas[col]]:
                    valor_limpio = valor.split('/')[0] # Cogemos el número que va antes de la barra, ya que es la presión sistólica y es más representativo
                    valores_finales.append(valor_limpio)
            else:
                for valor in df[columnas[col]]: # Iteramos por la columna
                        agregado = False # Creamos una "flag" que nos indique si ya se ha agregado un dato
                        if not agregado:
                            for unidad in unidades_estandar: # Si la unidad es estándar, le quitamos la unidad, lo convertimos en float y lo agregamos directamente
                                    if unidad in valor:
                                        valor_limpio = valor.replace(f' {unidad}', '')
                                        valores_finales.append(valor_limpio)
                                        agregado = True
                                        estandar += 1
                                        break
                        if not agregado:
                            for unidad in unidades_no_estandar: # Si no es estándar:
                                    if unidad in valor: # Si el dato contiene la unidad, así evitamos 0 y NaN
                                        valor_num = valor.replace(f' {unidad}', '') # Le quitamos la unidad
                                        # Usando otra función, convertimos a la unidad correspondiente
                                        valor_limpio = round(Analisis.operacion_str(float(valor_num), *factores_conversion[unidad].split()), 2)
                                        valores_finales.append(valor_limpio)
                                        agregado = True
                                        no_estandar += 1
                                        break
                        if not agregado:
                            valores_finales.append(valor)
            df[columnas[col]] = valores_finales
            df[columnas[col]] = df[columnas[col]].astype(float)

        # Defino 3 modos: 
        if modo == 'total': # Para retornar tanto datos sin transformar como transformados, en el mismo DF
            return df
        elif modo == 'num': # Para retornar solamente los datos transformados
            df_num = pd.DataFrame()
            for df_col in df.columns:
                if df_col not in columnas.keys():
                    df_num[df_col] = df[df_col]
                elif df_col in columnas.keys():
                    df.drop(columns=df_col)
            df_num.drop(columns='id', inplace=True)
            return df_num
        elif modo == 'columna': # Para retornar una columna concreta
            for col in cols:
                if col in columnas.keys():
                    return pd.DataFrame(df[columnas[col]]), [estandar, no_estandar]
                elif col not in columnas.keys():
                    df = Leer_Datos.abrir_csv()
                    return pd.DataFrame(df[col]), [estandar, no_estandar]
                            
                  
    
    def limpiar_errores(df: pd.DataFrame, cols: str = None, modo: str = 'total') -> pd.DataFrame:
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

        if not cols:
            for col in df.columns:
                if df[col].dtype == float or df[col].dtype == int: # Si el dtype es numérico, evitamos modificar hospitalización
                    df[col] = df[col].fillna(value=df[col].mean()) # Reemplazamos NaN por la media de valores
                    df[col] = df[col].replace(to_replace=0, value=df[col].mean()) # Reemplazamos 0 por la media de valores
                    df[col] = [round(num, 2) for num in df[col]] # Redondeamos al 2º decimal
                    df.loc[df[col]<0, col] *= -1 # Si el dato es negativo, lo volvemos positivo
            return df
        
        if modo == 'columna' and cols:
            num_no_nan = df.count()
            num_nan = len(df) - num_no_nan
            num_cero = len(df[df[cols] == 0])
            num_neg = len(df[df[cols] < 0])

            df[cols] = df[cols].fillna(value=df[cols].mean()) # Reemplazamos NaN por la media de valores
            df[cols] = df[cols].replace(to_replace=0, value=df[cols].mean()) # Reemplazamos 0 por la media de valores
            df[cols] = [round(num, 2) for num in df[cols]] # Redondeamos al 2º decimal
            df.loc[df[cols] < 0, cols] *= -1 # Si el dato es negativo, lo volvemos positivo
            return df[cols], (num_nan[cols], num_cero, num_neg)

'''import pandas as pd
df = Leer_Datos.abrir_csv()
df = Analisis.cadena_a_numero(df, modo='num')
print(df)
'''#df = pd.DataFrame(df)
#limpieza = Analisis.limpiar_errores(df=df[0], cols='peso_kg', modo='columna')
#print(type(limpieza[0]))
