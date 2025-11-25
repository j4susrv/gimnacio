from datetime import datetime, timedelta

class Suscripcion:
    def __init__(self, rut_cliente: str, tipo_suscripcion: str, fecha_inicio: str):
        self.rut_cliente = rut_cliente
        self.tipo_suscripcion = tipo_suscripcion.lower() # mensual, semestral, etc.
        # Almacena fecha_inicio como objeto datetime
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") 
        # Almacena fecha_fin como objeto datetime
        self.fecha_fin = self.calcular_fecha_fin()

    def calcular_fecha_fin(self) -> datetime:
        # Ya tenemos self.fecha_inicio como objeto datetime
        fecha_inicio_dt = self.fecha_inicio
        
        if self.tipo_suscripcion == "mensual":
            # Usar 30 días es una aproximación, pero se mantiene la lógica original
            dias = 30
        elif self.tipo_suscripcion == "trimestral":
            dias = 90
        elif self.tipo_suscripcion == "semestral":
            dias = 180
        elif self.tipo_suscripcion == "anual":
            dias = 365
        else:
            # Opción por defecto o para un tipo no reconocido
            dias = 30
            
        return fecha_inicio_dt + timedelta(days=dias)

    def esta_activa(self) -> bool:
        hoy = datetime.now()
        # Se compara directamente el objeto datetime con self.fecha_fin (objeto datetime)
        return hoy < self.fecha_fin # Usar < o <= según el criterio

    def dias_restantes(self) -> int:
        # Se calculan los días restantes desde hoy hasta la fecha de fin
        hoy = datetime.now()
        diferencia = self.fecha_fin - hoy # Esto da un timedelta
        
        # .days devuelve el número entero de días. 
        # Si la suscripción ha terminado, será negativo.
        dias = diferencia.days + 1 # Se añade 1 día para contar el día actual completo
        
        return max(0, dias) # Asegura que nunca sea un número negativo

    def a_diccionario(self) -> dict:
        # Se convierten los objetos datetime a cadena para la salida
        return {
            "rut_cliente": self.rut_cliente,
            "tipo_suscripcion": self.tipo_suscripcion,
            "fecha_inicio": self.fecha_inicio.strftime("%Y-%m-%d"), # Corregido a fecha_inicio
            "fecha_fin": self.fecha_fin.strftime("%Y-%m-%d"), # Se añade la fecha de fin
            "activa": self.esta_activa(),
            "dias_restantes": self.dias_restantes()
        }