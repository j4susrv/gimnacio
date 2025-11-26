from datetime import datetime, timedelta

class Suscripcion:
    TIPOS_VALIDOS = {"mensual", "trimestral", "semestral", "anual"}
    MAPEO_DIAS = {
        "mensual": 30,
        "trimestral": 90,
        "semestral": 180,
        "anual": 365
    }
    
    def __init__(self, rut_cliente: str, tipo_suscripcion: str, fecha_inicio: str, monto: float = 0):
        try:
            # Validar tipo de suscripción
            if tipo_suscripcion.lower() not in self.TIPOS_VALIDOS:
                raise ValueError(f"Tipo inválido. Debe ser: {', '.join(self.TIPOS_VALIDOS)}")
            
            self.rut_cliente = rut_cliente
            self.tipo_suscripcion = tipo_suscripcion.lower()
            self.monto = float(monto)
            
            # Parsear fecha con manejo de errores
            try:
                self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Formato de fecha inválido: {fecha_inicio}. Debe ser YYYY-MM-DD")
            
            self.fecha_fin = self.calcular_fecha_fin()
            
        except Exception as e:
            raise ValueError(f"Error al crear suscripción: {str(e)}")
    
    def calcular_fecha_fin(self) -> datetime:
        """Calcula fecha de fin con validación."""
        try:
            dias = self.MAPEO_DIAS.get(self.tipo_suscripcion, 30)
            return self.fecha_inicio + timedelta(days=dias)
        except Exception as e:
            raise ValueError(f"Error al calcular fecha fin: {str(e)}")
    
    def esta_activa(self) -> bool:
        """Verifica si la suscripción está activa."""
        try:
            return datetime.now() < self.fecha_fin
        except Exception:
            return False
    
    def dias_restantes(self) -> int:
        """Calcula días restantes con validación."""
        try:
            hoy = datetime.now()
            diferencia = self.fecha_fin - hoy
            dias = diferencia.days + 1
            return max(0, dias)
        except Exception:
            return 0
    
    def a_diccionario(self) -> dict:
        """Convierte a diccionario con manejo de errores."""
        try:
            return {
                "rut_cliente": self.rut_cliente,
                "tipo_suscripcion": self.tipo_suscripcion,
                "fecha_inicio": self.fecha_inicio.strftime("%Y-%m-%d"),
                "fecha_fin": self.fecha_fin.strftime("%Y-%m-%d"),
                "monto": self.monto,
                "activa": self.esta_activa(),
                "dias_restantes": self.dias_restantes()
            }
        except Exception as e:
            raise ValueError(f"Error al convertir suscripción: {str(e)}")
