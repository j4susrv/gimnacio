from datetime import datetime

#se va a guardar un registro del peso del cliente en una fecha
class HistorialPeso:
    def __init__(self, rut_cliente, peso, fecha=None):
        self.rut_cliente = rut_cliente
        self.peso = peso
        # Si no se proporciona fecha, usar la actual
        if fecha is None:
            self.fecha = datetime.now().strftime("%d-%m-%Y")
        else:
            self.fecha = fecha
    
    def a_diccionario(self):
        return {
            "rut_cliente": self.rut_cliente,
            "peso": self.peso,
            "fecha": self.fecha
        }
    
    @staticmethod
    def parsear_fecha(fecha_str: str) -> datetime:
        """Convierte string de fecha a datetime"""
        try:
            return datetime.strptime(fecha_str, "%d-%m-%Y")
        except ValueError:
            try:
                return datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                return None