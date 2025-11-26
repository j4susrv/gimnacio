from validaciones import Validaciones
from datetime import datetime

class Entrenador:
    def __init__(self, nombre, fecha_nacimiento, rut, estatura, peso, especialidades, contraseña):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.rut = rut
        self.estatura = estatura
        self.peso = peso
        # Formato lista para los entrenadores segun sus especialidades
        if especialidades is None:
            self.especialidades = []
        else:
            self.especialidades = especialidades
        self.contraseña = contraseña
        
    def obtener_detalles(self):
        print(f"Nombre {self.nombre}\n Rut: {self.rut}\n Especialidad: {self.especialidades}")
    
    def agregar_especialidad(self, especialidad):
        #se agregara una especialidad segun lo que haga el entrenador
        especialidad_lower = especialidad.lower()
        
        if especialidad_lower in self.especialidades:
            return False, "Especialidad ya existe"
        
        valido, mensaje = Validaciones.validar_especialidad(especialidad)
        if valido:
            self.especialidades.append(especialidad_lower)
            return True, f"Especialidad agregada: {especialidad}"
        
        return False, mensaje
    
    def a_diccionario(self):
        #guardara en un diccionario para guardarlos en un json
        return {
            "nombre": self.nombre,
            "fecha_nacimiento": self.fecha_nacimiento,
            "rut": self.rut,
            "estatura": self.estatura,
            "peso": self.peso,
            "especialidades": self.especialidades,
            "contraseña": self.contraseña
        }
    
    @staticmethod
    def validar_datos(nombre, fecha_nacimiento, rut, estatura, peso, contraseña):
        errores = []
        advertencias = []

        valido, mensaje = Validaciones.validar_nombre(nombre)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_rut(rut)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_estatura(estatura)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_contraseña(contraseña)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_peso(peso)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        return errores, advertencias


class TurnoEntrenador:
    def __init__(self, rut_entrenador, dia_semana, hora_inicio, hora_final):
        self.rut_entrenador = rut_entrenador
        self.dia_semana = dia_semana.lower()
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
    
    def calcular_horas_trabajadas(self):
        diferencia = self.hora_final - self.hora_inicio
        return diferencia.total_seconds() / 3600
    
    def a_diccionario(self):
        return {
            "rut_entrenador": self.rut_entrenador,
            "dia_semana": self.dia_semana,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_final,
            "horas_trabajo": self.calcular_horas_trabajadas()
        }