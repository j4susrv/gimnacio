from datetime import datetime
from validaciones import Validaciones

class Cliente:
    def __init__(self, nombre, rut, fecha_nacimiento, estatura, peso, estado_civil, direccion, contraseña, entrenador_asignado=None):
        self.nombre = nombre
        self.rut = rut
        self.fecha_nacimiento = fecha_nacimiento
        self.estatura = estatura
        self.peso = peso
        self.estado_civil = estado_civil
        self.direccion = direccion
        self.contraseña = contraseña
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d")
        self.entrenador_asignado = entrenador_asignado
    
    def calcular_imc(self):
        estatura_m = self.estatura/100
        return round(self.peso/(estatura_m **2), 2)
    
    def determinar_rutina(self):
        imc = self.calcular_imc()
        if imc < 18.5:
            return 5, "Peso bajo"
        if imc < 25:
            return 7, "Peso normal"
        if imc < 30:
            return 10, "Sobrepeso"
        else:
            return 15, "Obesidad"
    
    def a_diccionario(self):
        rutina, categoria = self.determinar_rutina()
        return {
            "nombre": self.nombre,
            "rut": self.rut,
            "fecha_nacimiento": self.fecha_nacimiento,
            "estatura": self.estatura,
            "peso": self.peso,
            "estado_civil": self.estado_civil,
            "direccion": self.direccion,
            "imc": self.calcular_imc(),
            "rutina_mensual": rutina,
            "categoria_imc": categoria,
            "contraseña": self.contraseña,
            "entrenador_asignado": self.entrenador_asignado,
            "fecha_registro": self.fecha_registro
        }
    
    @staticmethod
    def validar_datos(nombre, fecha_nacimiento, estatura, peso, estado_civil, direccion, contraseña):
        errores = []
        advertencias = []
        
        valido, mensaje = Validaciones.validar_nombre(nombre)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        valido, mensaje = Validaciones.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_estatura(estatura)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        valido, mensaje = Validaciones.validar_peso(peso)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        valido, mensaje = Validaciones.validar_estado_civil(estado_civil)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_contraseña(contraseña)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_direccion(direccion)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        return errores, advertencias