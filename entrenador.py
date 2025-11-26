from validaciones import Validaciones
from datetime import datetime
#Agrega 1 atributo de especialidad y guardarlo como lista, def agregar_especialidad y agregar tambien a_diccionario especialidad 
class Entrenador:
    def __init__(self,nombre,fecha_nacimiento,rut,estatura,peso,especialidades):
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
    def agregar_especialidad(self,especialidad):
        valido, mensaje = Validaciones.validar_especialidad(especialidad)
        if valido and especialidad.lower() not in self.especialidades:
            self.especialidades.append(especialidad.lower())
            return True,f"Epecialidad agregada: {especialidad}"
        return False,mensaje if not valido else "Especialidad ya existe"
    def a_diccionario(self):
        return {
            "nombre": self.nombre,
            "fecha_nacimiento": self.fecha_nacimiento,
            "rut": self.rut,
            "estatura": self.estatura,
            "peso": self.peso,
            "especialidades": self.especialidades
        }

class TurnoEntrenador:
    def __init__(self, rut_entrenador, dia_semana, hora_inicio, hora_final):
        self.rut_entrenador = rut_entrenador
        self.dia_semana = dia_semana.lower()
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final  # CORREGIDO: nombre correcto
    
    def calcular_horas_trabajadas(self):
        try:
            hora_inicio = datetime.strptime(self.hora_inicio, "%H:%M")
            hora_final = datetime.strptime(self.hora_final, "%H:%M")
            diferencia = hora_final - hora_inicio
            return diferencia.seconds / 3600
        except:
            return 0
    
    def a_diccionario(self):
        return {
            "rut_entrenador": self.rut_entrenador,
            "dia_semana": self.dia_semana,
            "hora_inicio": self.hora_inicio,
            "hora_fin": self.hora_final,  # CORREGIDO: usar hora_final
            "horas_trabajo": self.calcular_horas_trabajadas()
        }