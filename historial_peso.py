#se va a guardar un registro del peso del cliente en una fecha
class HistorialPeso:
    def __init__(self,rut_cliente,peso,fecha):
        self.rut_cliente = rut_cliente
        self.peso = peso
        self.fecha = fecha
    def a_diccionario(self):
        return {
            "rut_cliente":self.rut_cliente,
            "peso":self.peso,
            "fecha":self.fecha
        }