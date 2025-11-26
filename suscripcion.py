from datetime import datetime, timedelta

class Suscripcion:
    def __init__(self,rut_cliente,tipo_suscripcion,fecha_inicio,monto):
        self.rut_cliente = rut_cliente
        self.tipo_suscripcion = tipo_suscripcion.lower()
        self.fecha_inicio = fecha_inicio
        self.monto = monto
        self.fecha_fin = self.calcular_fecha_fin()
    
    def calcular_fecha_fin(self):
        # CORREGIDO: Usar strptime (parsing) en lugar de strftime
        try:
            fecha_inicio_dt = datetime.strptime(self.fecha_inicio, "%Y-%m-%d")
        except:
            fecha_inicio_dt = datetime.now()
        
        if self.tipo_suscripcion == "mensual":
            fecha_fin = fecha_inicio_dt + timedelta(days=30)
        elif self.tipo_suscripcion == "trimestral":
            fecha_fin = fecha_inicio_dt + timedelta(days=90)
        elif self.tipo_suscripcion == "semestral":
            fecha_fin = fecha_inicio_dt + timedelta(days=180)
        elif self.tipo_suscripcion == "anual":
            fecha_fin = fecha_inicio_dt + timedelta(days=365)
        else:
            fecha_fin = fecha_inicio_dt + timedelta(days=30)
        
        return fecha_fin.strftime("%Y-%m-%d")
    
    def esta_activa(self):
        hoy = datetime.now()
        try:
            fecha_fin_dt = datetime.strptime(self.fecha_fin, "%Y-%m-%d")
            return hoy <= fecha_fin_dt
        except:
            return False
    
    def dias_restantes(self):
        hoy = datetime.now()
        try:
            fecha_fin_dt = datetime.strptime(self.fecha_fin, "%Y-%m-%d")
            diferencia = fecha_fin_dt - hoy
            return diferencia.days if diferencia.days > 0 else 0
        except:
            return 0
    
    def a_diccionario(self):
        return {
            "rut_cliente": self.rut_cliente,
            "tipo_suscripcion": self.tipo_suscripcion,
            "fecha_inicio": self.fecha_inicio,  # CORREGIDO: era fecha_fin
            "fecha_fin": self.fecha_fin,
            "activa": self.esta_activa(),
            "dias_restantes": self.dias_restantes(),
            "monto": self.monto
        }
