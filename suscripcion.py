from datetime import datetime, timedelta

class Suscripcion:
    def __init__(self, rut_cliente: str, tipo_suscripcion: str, fecha_inicio: str):
        self.rut_cliente = rut_cliente
        self.tipo_suscripcion = tipo_suscripcion.lower()
        
        # Convierte la fecha de texto a datetime (acepta DD-MM-YYYY o YYYY-MM-DD)
        self.fecha_inicio = self._parsear_fecha(fecha_inicio)
        # Calcula la fecha de fin automáticamente
        self.fecha_fin = self.calcular_fecha_fin()

    def _parsear_fecha(self, fecha_str: str) -> datetime:
        # Intenta primero formato chileno DD-MM-YYYY
        try:
            return datetime.strptime(fecha_str, "%d-%m-%Y")
        except ValueError:
            # Si falla, intenta formato ISO YYYY-MM-DD
            return datetime.strptime(fecha_str, "%Y-%m-%d")

    def calcular_fecha_fin(self) -> datetime:
        # Define cuántos días dura cada tipo de suscripción
        if self.tipo_suscripcion == "mensual":
            dias = 30
        elif self.tipo_suscripcion == "trimestral":
            dias = 90
        elif self.tipo_suscripcion == "semestral":
            dias = 180
        elif self.tipo_suscripcion == "anual":
            dias = 365
        else:
            dias = 30
        
        # Suma los días a la fecha de inicio
        return self.fecha_inicio + timedelta(days=dias)

    def esta_activa(self) -> bool:
        # True si la suscripción aún no ha vencido
        return datetime.now() <= self.fecha_fin

    def dias_restantes(self) -> int:
        # Calcula cuántos días faltan
        diferencia = self.fecha_fin - datetime.now()
        dias = diferencia.days + 1
        # Nunca devuelve negativos
        return max(0, dias)

    def a_diccionario(self) -> dict:
        # Convierte a diccionario para guardar en JSON (formato chileno)
        return {
            "rut_cliente": self.rut_cliente,
            "tipo_suscripcion": self.tipo_suscripcion,
            "fecha_inicio": self.fecha_inicio.strftime("%d-%m-%Y"),
            "fecha_fin": self.fecha_fin.strftime("%d-%m-%Y"),
            "activa": self.esta_activa(),
            "dias_restantes": self.dias_restantes()
        }