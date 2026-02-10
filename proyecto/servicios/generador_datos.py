class Generador_Datos():
    @staticmethod
    def guardar_generador_datos(datos: list[dict], url: str = 'datos_forjados.csv') -> bool:
        """
        Guarda los datos generados en forma de archivo CSV en la misma carpeta que el archivo actual.
        
        :param datos: Lista de diccionarios, cada uno de los cuales es una fila.
        :type datos: list[dict]
        :param url: Nombre del archivo a crear.
        :type url: str
        :return: Confirmación de guardado.
        :rtype: bool
        """
        import os
        import csv
        url = os.path.join(os.path.dirname(__file__), url)
        try:
            with open(url, 'w', encoding='UTF-8') as file:
                encabezados = datos[0].keys()
                escritor = csv.DictWriter(file, encabezados, lineterminator="\n")
                escritor.writeheader()
                escritor.writerows(datos)
            # Devolvemos True si tuvo éxito, o False si no pudimos crear el archivo
            return True
        except FileNotFoundError:
            return False
    
    @staticmethod
    def condicion_hosp(paciente: dict, imc_rango: list[float], gluc_rango: list[float], ten_sis: int) -> int:
        """
        Evalúa si los datos caen dentro o fuera del rango de salud, y devuelve un número que indica la gravedad del paciente.
        
        :param paciente: Diccionario que contiene los datos del paciente.
        :type paciente: dict
        :param imc_rango: Rango de salud del IMC.
        :type imc_rango: list[float]
        :param gluc_rango: Rango de salud de la glucosa.
        :type gluc_rango: list[float]
        :param ten_sis: Rango de salud de la presión arterial.
        :type ten_sis: int
        :return: Nivel de gravedad del paciente.
        :rtype: int
        """
        hospitalizacion = 0
        # En base al índice de masa corporal: un peso muy bajo o muy alto puede ser de riesgo
        if 'kg' in paciente['peso']: 
            peso_kg = float(paciente['peso'].strip(' kg'))
        elif 'lb' in paciente['peso']:
            peso_kg = float(paciente['peso'].strip(' lb')) * 0.45359237

        if 'cm' in paciente['altura']:
            altura_m = float(paciente['altura'].strip(' cm')) /100
        elif 'inch' in paciente['altura']:
            altura_m = float(paciente['altura'].strip(' inch')) * 2.54 /100
    
        imc = peso_kg / altura_m**2

        if imc < imc_rango[0] or imc > imc_rango[1]:
            hospitalizacion += 1
        
        # En base a la presión arterial: muy alta o muy baja indica una crisis
        presion_sis = int(paciente['presion_arterial'].split('/')[0])
        if presion_sis < 90 or presion_sis > ten_sis:
            hospitalizacion += 1

        # En base a la glucosa en sangre: muy baja o muy alta requiere atención inmediata
        if 'mg/dL' in paciente['glucosa']:
            glucosa = float(paciente['glucosa'].strip(' mg/dL'))
            if glucosa < gluc_rango[0] or glucosa > gluc_rango[1]:
                hospitalizacion += 1

        if 'mmol/L' in paciente['glucosa']:
            glucosa = (float(paciente['glucosa'].strip(' mmol/L')) *17.5) +3.75
            if glucosa < gluc_rango[0] or glucosa > gluc_rango[1]:
                hospitalizacion += 1

        return hospitalizacion

    @staticmethod
    def crear_errores(paciente: dict, prob: int=1) -> dict:
        """
        Recibe los datos de un paciente e introduce entre 0 y 1 errores por dato.
        
        :param paciente: Diccionario con los datos del paciente.
        :type paciente: dict
        :param prob: Modifica la probabilidad de introducir un error: a más alta, menor probabilidad.
        :type prob: int
        :return: Diccionario con datos de paciente modificado.
        :rtype: dict
        """
        import random
        import numpy as np
        # Definimos la probabilidad como 1/prob+1:
        alea = random.randint(0, prob)
        # k es el número de columnas a aplicar cambios
        k = random.randint(0,6)
        # Elegimos k columnas de entre las 6 disponibles
        cambio = random.choices(list(paciente.keys()), k=k)
        for elemento in cambio:
            # Dentro de cada elemento, elegimos de manera aleatoria si recibirá cambios
            suerte = random.randint(0, prob)
            if suerte == alea:
                # Si va a recibir cambios, elegimos el tipo de cambio
                eleccion = random.randint(0,3)
                if eleccion == 0:
                    # Ningún cambio
                    pass
                elif eleccion == 1:
                    # Cambiar por NaN
                    paciente[elemento] = np.nan
                elif eleccion == 2:
                    # Cambiar el signo a negativo
                    try:
                        if '-' not in paciente[elemento]:
                            paciente[elemento] = '-' + paciente[elemento]
                    except TypeError:
                        paciente[elemento] = paciente[elemento] * -1
                else:
                    # Cambiar por 0
                    paciente[elemento] = 0
            else:
                pass
        return paciente

    @staticmethod
    def generar_datos(num: int = 100, prop_enf: float = 0.5) -> bool:
        """
        Genera de manera aleatoria los datos de los paciente solicitados 
        según la proporción de hospitalizados requerida, introduce errores y 
        guarda los datos en un archivo CSV.
        
        :param num: Número de pacientes a generar.
        :type num: int
        :param prop_enf: Proporción de pacientes que requerirán hospitalización.
        :type prop_enf: float
        :return: Confirmación de generación y guardado exitosos.
        :rtype: bool
        """
        import numpy as np
        import random
        sanos = []
        enfermos = []
        id = 1
        pacientes = sanos +  enfermos

        while len(pacientes) < num:
            paciente = dict()

            # ID: simplemente el número de paciente
            paciente['id'] = id

            # Edad: rango entre 18 y 90
            # El centro de la distribución será 49 años
            edad = round(np.random.normal(49,12))
            paciente['edad'] = edad

            # Peso: habrá valores en kg y otros en lb
            # El centro de la distribución será 80 kg
            # 1 lb = 0.45359237 kg
            # 1 lb = 1/2.20462 kg
            peso_kg = str(round(np.random.normal(80, 6), 2)) + ' kg'
            peso_lb = str(round(np.random.normal(36.28, 3), 2)) + ' lb'
            paciente['peso'] = random.choice([peso_kg, peso_lb])

            # Altura: habrá valores en cm y pulgadas
            # El centro de la distribución será 170 cm
            # 1 inch = cm * 2.54
            # 1 cm = 0.3937 * inch
            altura_cm = str(round(np.random.normal(160, 8))) + ' cm'
            altura_inch = str(round(np.random.normal(62, 3.89))) + ' inch'
            paciente['altura'] = random.choice([altura_cm, altura_inch])

            # IMC: peso en kg / (altura en m)^2
            # No la introduciré en los datos, pero sí la usaré como criterio 
            # de hospitalización

            # Presión arterial
            # Tiene 2 componentes: presión sistólica y presión diastólica
            # El centro de la distribución será 110/75
            presion_sis = round(np.random.normal(110, 25))
            presion_dias = round(presion_sis * 0.66)
            presion = str(presion_sis) + '/' + str(presion_dias)
            paciente['presion_arterial'] = presion

            # Glucosa: habrá algunos valores en mmol/l y otros en mg/dl
            # El centro de la distribución será 180 mg/dL
            # el estándar en España es mg/dl, así que es el que usaré
            # Fórmula: Y(mg/dl) = 17,5 * X(mmol/l) + 3,75
            glucosa_mg = str(round(np.random.normal(190, 55), 2)) + ' mg/dL'
            glucosa_mmol = str(round(np.random.normal(10, 3.36), 2)) + ' mmol/L'
            paciente['glucosa'] = random.choice([glucosa_mg, glucosa_mmol])

            # Hospitalización: en base a criterios médicos, cuando un paciente se sale
            # de ciertos rangos (por exceso o defecto), se considera en crisis
            # y debe ser hospitalizado.
            
            # Si la edad es baja o alta, cambian las condiciones de hospitalización:
            # <20 años: IMC<15 | IMC>40, GLUC<70 | GLUC>400, TEN>=180/110
            if paciente['edad'] < 20:
                hospitalizacion = Generador_Datos.condicion_hosp(paciente, imc_rango=[13,43], gluc_rango=[70,400], ten_sis=180)

            # 20< años <60: IMC<15 | IMC>40, GLUC<54 | GLUC>450, TEN>=180/110
            elif 20 < paciente['edad'] < 60:
                hospitalizacion = Generador_Datos.condicion_hosp(paciente, imc_rango=[13,43], gluc_rango=[54,450], ten_sis=180)

            # >60 años: IMC<15 | IMC>40, GLUC<70 | GLUC>300, TEN>=180/110
            else:
                hospitalizacion = Generador_Datos.condicion_hosp(paciente, imc_rango=[13,43], gluc_rango=[70,300], ten_sis=180)

            # Introducción de errores: de manera aleatoria, introducción 
            # de valores negativos, 0, NaN o sin cambios.
            errores = random.randint(1, 10)
            paciente = Generador_Datos.crear_errores(paciente, errores)

            # Generamos el dato "hospitalizacion" en base a si se cumplen las condiciones
            if hospitalizacion > 0:
                paciente['hospitalizacion'] = 'Sí'
                if len(enfermos) < num * prop_enf:
                    enfermos.append(paciente)
            else:
                paciente['hospitalizacion'] = 'No'
                if len(sanos) < num * (1 - prop_enf):
                    sanos.append(paciente)
            pacientes = sanos + enfermos
            id += 1

        pacientes.sort(key=lambda x: x['id'])
        return Generador_Datos.guardar_generador_datos(pacientes)
