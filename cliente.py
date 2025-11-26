from datetime import datetime
from validaciones import Validaciones

class Cliente:
    def __init__(self, nombre, rut, fecha_nacimiento, estatura, peso, 
                 estado_civil, direccion):
        # ✅ ELIMINADO: apellido
        self.nombre = nombre
        self.rut = rut
        self.fecha_nacimiento = fecha_nacimiento
        self.estatura = float(estatura)
        self.peso = float(peso)
        self.estado_civil = estado_civil
        self.direccion = direccion
        self.fecha_registro = datetime.now().strftime("%Y-%m-%d")
    
    def calcular_imc(self):
        """Calcula IMC con validación de seguridad."""
        try:
            if self.estatura <= 0 or self.peso <= 0:
                raise ValueError("Estatura y peso deben ser positivos")
            
            estatura_m = self.estatura / 100
            imc = self.peso / (estatura_m ** 2)
            return round(imc, 2)
        except ZeroDivisionError:
            raise ValueError("La estatura no puede ser 0")
        except Exception as e:
            raise ValueError(f"Error al calcular IMC: {str(e)}")
    
    def determinar_rutina(self):
        """Determina rutina según IMC con manejo de errores."""
        try:
            imc = self.calcular_imc()
            
            if imc < 18.5:
                return 5, "Peso bajo"
            elif imc < 25:
                return 7, "Peso normal"
            elif imc < 30:
                return 10, "Sobrepeso"
            else:
                return 15, "Obesidad"
        except Exception as e:
            return 7, "Error en cálculo"
    
    def a_diccionario(self):
        """Convierte a diccionario con validación."""
        try:
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
                "fecha_registro": self.fecha_registro
            }
        except Exception as e:
            raise ValueError(f"Error al convertir cliente a diccionario: {str(e)}")
    
    @staticmethod
    def validar_datos(nombre, rut, fecha_nacimiento, estatura, peso, estado_civil, direccion):
        """Valida todos los datos del cliente."""
        errores = []
        advertencias = []
        
        valido, mensaje = Validaciones.validar_nombre(nombre)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        valido, mensaje = Validaciones.validar_rut(rut)
        if not valido:
            errores.append(mensaje)
        
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
        
        valido, mensaje = Validaciones.validar_direccion(direccion)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        
        return errores, advertencias