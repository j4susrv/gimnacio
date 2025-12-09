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
    def validar_datos(nombre, fecha_nacimiento, estatura, peso, contraseña):
        errores = []
        advertencias = []

        valido, mensaje = Validaciones.validar_nombre(nombre)
        if not valido:
            errores.append(mensaje)
        
        valido, mensaje = Validaciones.validar_fecha_nacimiento(fecha_nacimiento)
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

from datetime import datetime

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
            "dia": self.dia_semana,  # Cambiado a "dia" para consistencia
            "hora_inicio": str(self.hora_inicio),
            "hora_fin": str(self.hora_final),
            "horas_trabajo": self.calcular_horas_trabajadas()
        }
    
    @staticmethod
    def esta_disponible(rut_entrenador, entrenadores_lista):
        """
        Verifica si el entrenador está disponible AHORA
        Args:
            rut_entrenador: RUT del entrenador
            entrenadores_lista: Lista de entrenadores desde gimnasio.entrenadores o JSON
        Returns:
            bool: True si está disponible ahora
        """
        if not entrenadores_lista:
            return False
        
        # Buscar el entrenador
        entrenador = None
        for e in entrenadores_lista:
            if e.get("rut") == rut_entrenador:
                entrenador = e
                break
        
        if not entrenador or "turnos" not in entrenador:
            return False
        
        ahora = datetime.now()
        
        # Traducir día actual
        dias_ingles_espanol = {
            "Monday": "lunes", 
            "Tuesday": "martes", 
            "Wednesday": "miércoles",
            "Thursday": "jueves", 
            "Friday": "viernes", 
            "Saturday": "sábado", 
            "Sunday": "domingo"
        }
        
        dia_actual = dias_ingles_espanol.get(ahora.strftime("%A"), "").lower()
        hora_actual = ahora.time()
        
        # Buscar si tiene turno HOY
        for turno in entrenador["turnos"]:
            # CORRECCIÓN: Buscar tanto "dia" como "dia_semana" para compatibilidad
            dia_turno = turno.get("dia") or turno.get("dia_semana")
            
            if dia_turno and dia_turno.lower() == dia_actual:
                try:
                    hora_inicio_str = turno.get("hora_inicio", "")
                    hora_fin_str = turno.get("hora_fin", "")
                    
                    # Manejar diferentes formatos de hora
                    if ":" in hora_inicio_str and ":" in hora_fin_str:
                        inicio = datetime.strptime(hora_inicio_str.split(".")[0], "%H:%M:%S").time()
                        fin = datetime.strptime(hora_fin_str.split(".")[0], "%H:%M:%S").time()
                        
                        if inicio <= hora_actual <= fin:
                            return True
                except Exception as e:
                    print(f"DEBUG: Error al verificar turno: {e}")
                    continue
        
        return False