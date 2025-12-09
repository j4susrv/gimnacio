import re, os, json
from datetime import datetime
class Validaciones:

    ESPECIALIDADES_VALIDAS = [
        "zumba", "cardio", "fuerza", "funcional", "yoga",
        "pilates", "spinning", "crossfit", "boxeo", "elongacion",
        "reduccion de calorias"
    ]

    @staticmethod
    def validar_nombre(nombre):
        nombre_sin_espacios = nombre.replace(" ","")
        if not nombre or nombre.strip() == "":
            return False, "El nombre no puede estar vacio"
        if len(nombre_sin_espacios) < 3:
            return False, "El nombre debe tener mas de 3 caracteres"
        if len(nombre_sin_espacios)>50:
            return False, "El nombe no puede tener mas de 50 caracteres"
        if not re.match(r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ\s]+$', nombre):
            return False, "El nombre solo puede contener letras y espacios"
        
        if nombre.count(" ")>5:
            return False, "Contiene demasiados espacios"
        
        return True,"Nombre valido"
    
    @staticmethod
    def validar_rut(rut):
        if not rut or rut.strip() == "": #Verifica si el rut esta completo
            return False,"El Rut no puede estar vacio"
        rut_limpio = rut.replace(".","").replace("-","").strip()

        if len(rut_limpio) <8 or len(rut_limpio) >9: #Recorre el rut hasta los 9 dijitos
            return False, "El rut tiene que tener un minimo de 8 o 9 caracteres"
        if not re.match(r'^\d{7,8}[0-9Kk]$', rut_limpio):
            return False, "El formato del rut invalido"
        rut_invalido = [
            "111111111","222222222","333333333","444444444","555555555","666666666","777777777","888888888","999999999"
        ]
        if rut_limpio in rut_invalido:
            return False, "El rut es invalido, ingrese nuevamente"
        #Aqui se limpia el rut
        rut_numeros = rut_limpio[:-1] #elimina el ultimo digito de el rut en este caso el verificador
        digito_verificador = rut_limpio[-1].upper() #La funcion upper sirve para colocar todo en mayusculas

        suma = 0
        multiplicador = 2

        for digitos in reversed(rut_numeros):
            suma += int(digitos) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2
        #Se calcula el codigo verificador
        resto = suma % 11
        dv_calculado = 11 - resto

        if dv_calculado == 11:
            dv_esperado = "0"
        elif dv_calculado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(dv_calculado)

        # se verifica si el codigo verificador es el correcto
        if digito_verificador != dv_esperado:
            return False,"El digito verificador del RUT es erroneo"
        return True, "RUT verificado" #Si el codigo verificador es correcto, devuelve Rut verificado
    @staticmethod
    def validar_rut_unico(rut):
        """
        Valida que el RUT no esté duplicado en NINGUNO de los tres JSONs
        Retorna (es_unico, mensaje)
        """
        archivos_a_revisar = ["clientes.json", "entrenadores.json", "administradores.json"]
        
        for archivo in archivos_a_revisar:
            if os.path.exists(archivo):
                try:
                    with open(archivo, "r", encoding="utf-8") as f:
                        datos = json.load(f)
                        
                        # Validar si es una lista o un diccionario
                        if isinstance(datos, list):
                            for registro in datos:
                                if registro.get("rut") == rut:
                                    return False, f"El RUT {rut} ya existe en {archivo}"
                        elif isinstance(datos, dict):
                            if datos.get("rut") == rut:
                                return False, f"El RUT {rut} ya existe en {archivo}"
                except Exception as e:
                    print(f"Error al revisar {archivo}: {e}")
                    continue
        
        return True, "RUT disponible"
    @staticmethod
    def validar_fecha_nacimiento(fecha_str):
        if not fecha_str or fecha_str.strip()==" ": #Verifica si la fecha vacia o no
            return False, "Fecha de nacimiento no puede estar vacia"
        try: #Es una funcion que captura errores  pero  que no rompe el programa
            formatos = ["%Y-%m-%d","%d/%m/%Y","%d-%m-%Y"]
            fecha = None
            for formato in formatos:
                try:
                    fecha = datetime.strptime(fecha_str,formato)
                    break
                except ValueError:
                    continue

            if fecha is None: #Fecha si es nulo, va a retornar formato fecha es invalido
                return False, "El formato fecha es invalido"
            #Verifica si la fecha de nacimiento no sea futura.
            if fecha > datetime.now():
                return False, "La fecha de nacimiento no puede ser futura"
        
            hoy = datetime.now()
            edad = hoy.year - fecha.year - ((hoy.month,hoy.day) < (fecha.month,fecha.day))

            if edad < 15:
                return False, "El cliente debe tener al menos 15 años"
            if edad > 100:
                return False, "La edad no puede ser mayor a 100 años"
        
            return True, "La fecha es valida"
        except Exception as e:
            return False,f"Error en la fecha {str(e)}"
    @staticmethod
    def validar_fecha(dia,mes,anio):
        if mes < 1 or mes >12:
            return False
        dia_mes = [31,28,31,30,31,30,31,31,30,31,30,31]
        #se valida si es un año bisiesto
        if (anio % 4 == 0 and anio % 100!=0) or (anio % 400 == 0):
            dia_mes[1] = 29
        #se valida el dia maximo
        if dia > dia_mes[mes -1]:
            return False
    @staticmethod
    def validar_estatura(estatura):
        try:
            estatura_num = float(estatura)
            if estatura_num < 50:
                return False, "La estatura debe ser mayor a 50 cm"
            if estatura_num > 250:
                return False, "La estatura debe ser menor a 250 cm"
            if estatura_num < 120 or estatura_num > 220:
                return False, f"Estatura inusual: {estatura_num} cm"
            return True, "Estatura válida"

        except ValueError:
            return False, "Error: la estatura no es un número"
        
    @staticmethod
    def validar_peso(peso):
        #Se valida el peso ek kg siendo realista entre 30 y 300
        try:
            peso_num = float(peso)
            if peso_num <30:
                return False, "El peso debe ser menor a 30kg"
            if peso_num > 300:
                return False, "El peso no puede ser mayor a 300kg"
            if peso_num < 40 or peso_num > 200:
                return True, f"Es correcto el peso dado? {peso_num}kg"
            return True, "El peso es valido"
        except ValueError:
            return False, "El peso debe ser un numero valido"
        
    @staticmethod
    def validar_estado_civil(estado_civil):
        estados_validos = ["soltero", "casado", "divorciado", "viudo", "conviviente"]
        if not estado_civil or estado_civil.strip() == "":
            return False, "El estado civil no puede estar vacío"
        if estado_civil.lower() not in estados_validos:
            return False, f"Estado civil inválido. Debe ser: {', '.join(estados_validos)}"
        
        return True, "Estado civil válido"
    @staticmethod
    def validar_direccion(direccion):
        direccion_sin_espacios = direccion.replace(" ", "")
        #Verificar si esta el campo con informacion y retorna falso si esta vacio
        if not direccion or direccion.strip() == "":
            return False, "La direccion no puede estar vacia" 
        if len(direccion_sin_espacios) < 5:
            return False, "La direccion debe tener mas de 5 caracteres"
        if len(direccion_sin_espacios) > 100:
            return False, "La direcicion no puede tener mas de 100 caracteres"
        if not re.search(r'\d', direccion): #Se verifica si direccion cuenta con algun digito numerico con el \d
            return True, f"La direccion no contiene numeros {direccion}. ¿Es correcto?"
        
        return True, "Direccion valida"
    @staticmethod
    def validar_duracion(duracion):
        #Verifica que la duracion de un ejercicio sea de tipo entero
        try:
            duracion_num = int(duracion)
        except ValueError:
            return False, "La duracion tiene que ser un numero entero"
        if duracion_num <= 0:
            return False, "La duracion de un ejercicio no puede ser 0 o un valor negativo"
        if duracion_num < 15:
            return True, "Duracion muy corta, ¿Es correcto?"
        
    @staticmethod
    def validar_tipo_ejercicio(tipo_ejercicio):
        if not tipo_ejercicio or tipo_ejercicio.strip() == "":
            return False, "No puede estar este campo vacio"
        tipos_validos = [
            "resistencia",           # Ejercicios de aguante
            "elongacion",            # Estiramientos
            "reduccion de calorias", # Cardio para quemar calorías
            "cardio",                # Cardiovascular
            "fuerza",                # Pesas, musculación
            "flexibilidad",          # Yoga, pilates
            "funcional"              # Ejercicios funcionales
        ]
        if tipo_ejercicio.lower() not in tipos_validos:
            return False,f"Tipo de ejercicio invalido: {', '.join(tipos_validos)}"
    @staticmethod
    def validar_contraseña(contraseña):
        if not contraseña or contraseña.strip()=="":
            return False,"El campo de contraseaña no puede estar vacio"
        if len(contraseña) <6:
            return False, "Debe contar con almenos 6 caracteres"
        if len(contraseña) > 30:
            return False, "Debe contar con menos de 30 caracteres"
        #El isdigit ayuda para verificar si existen numeros dentro y si no retornara falso "Contraseña debil"
        if contraseña.isdigit():
            return False, "La contraseña debe contener al menos una letra"
        return True, "Contraseña valida"

    @staticmethod
    def validar_tipo_suscripcion(tipo_suscripcion):
        suscripciones_validas = ["mensual","semestral","trimestral","anual"]
        if not tipo_suscripcion or tipo_suscripcion.strip() == "":
            return False, "El tipo de suscripcion no puede estar vacio"
        if tipo_suscripcion.lower() not in suscripciones_validas:
            return False,f"Tipo de suscripcion invalido. Debe ser {', '.join(suscripciones_validas)}"
        return True, "Tipo de suscripcion valido"
    @staticmethod
    def validar_especialidad(especialidad):
        if not especialidad or especialidad.strip() == "":
            return False, "El campo especialidad no puede estar vacío"
        
        # Validamos contra la lista de la clase
        if especialidad.lower() not in Validaciones.ESPECIALIDADES_VALIDAS:
            return False, "Especialidad no válida. Seleccione una de la lista."
            
        return True, "Especialidad válida"
    @staticmethod
    def validar_hora(hora):
        if not hora or hora.strip() == "":
            return False, "La hora no puede estar vacia"
        #Los 3 primeros corchetes representan a horas de 00 hasta las 23
        #Las ultimas 2 corresponden a 00 a 59 osea son minutos
        patron_hora = r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$'
        if re.match(patron_hora, hora.strip()):
        # Si coincide con el patrón después de limpiar espacios
            return True, "Formato de hora válido"
        else:
            # Si no coincide con el patrón
            return False, f"La hora '{hora.strip()}' no tiene el formato HH:MM por lo tanto no es valido."