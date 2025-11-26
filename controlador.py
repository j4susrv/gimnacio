import json
import os
from datetime import datetime
from cliente import Cliente
from entrenador import Entrenador
from suscripcion import Suscripcion
from historial_peso import HistorialPeso
from gimnasio import Gimnacio

class ControladorGUI:
    """
    Controlador centralizado para todas las operaciones de la GUI.
    Evita duplicación de lógica y garantiza consistencia de datos.
    """
    
    def __init__(self):
        self.gym = Gimnacio()
    
    # ==================== CLIENTES ====================
    def registrar_cliente(self, nombre, rut, fecha_nacimiento, estatura, peso, 
                         estado_civil="No especificado", direccion="No especificada"):
        """
        Registra un cliente con validación centralizada.
        Retorna: (éxito: bool, mensaje: str)
        """
        try:
            # Validar que no exista duplicado
            exito, _ = self.gym.buscar_cliente_por_rut(rut)
            if exito:
                return False, f"Ya existe cliente con RUT {rut}"
            
            # Crear cliente
            nuevo_cliente = Cliente(
                nombre=nombre,
                rut=rut,
                fecha_nacimiento=fecha_nacimiento,
                estatura=float(estatura),
                peso=float(peso),
                estado_civil=estado_civil,
                direccion=direccion
            )
            
            # Agregar a través del gimnasio
            return self.gym.agregar_cliente(nuevo_cliente)
            
        except ValueError as e:
            return False, f"Error de tipo: {str(e)} (estatura y peso deben ser números)"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def obtener_clientes(self):
        """Obtiene lista actualizada de clientes."""
        self.gym.cargar_datos()  # Recargar antes de retornar
        return self.gym.clientes
    
    def eliminar_cliente(self, rut):
        """Elimina cliente y retorna estado."""
        try:
            return self.gym.eliminar_cliente(rut)
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    # ==================== ENTRENADORES ====================
    def registrar_entrenador(self, nombre, rut, fecha_nacimiento, estatura, 
                            peso, especialidades):
        """
        Registra entrenador con validación centralizada.
        Retorna: (éxito: bool, mensaje: str)
        """
        try:
            # Validar que no exista duplicado
            exito, _ = self.gym.buscar_entrenador_por_rut(rut)
            if exito:
                return False, f"Ya existe entrenador con RUT {rut}"
            
            # Crear entrenador
            nuevo_entrenador = Entrenador(
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                rut=rut,
                estatura=float(estatura),
                peso=float(peso),
                especialidades=especialidades if especialidades else []
            )
            
            # Agregar a través del gimnasio
            return self.gym.agregar_entrenador(nuevo_entrenador)
            
        except ValueError as e:
            return False, f"Error de tipo: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def obtener_entrenadores(self):
        """Obtiene lista actualizada de entrenadores."""
        self.gym.cargar_datos()
        return self.gym.entrenadores
    
    def eliminar_entrenador(self, rut):
        """Elimina entrenador y retorna estado."""
        try:
            return self.gym.eliminar_entrenador(rut)
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    # ==================== SUSCRIPCIONES ====================
    def crear_suscripcion(self, rut_cliente, tipo_suscripcion, monto):
        """Crea suscripción con validación."""
        try:
            fecha_inicio = datetime.now().strftime("%Y-%m-%d")
            suscripcion = Suscripcion(rut_cliente, tipo_suscripcion, fecha_inicio)
            return self.gym.crear_suscripcion(suscripcion)
        except Exception as e:
            return False, f"Error al crear suscripción: {str(e)}"
    
    # ==================== SEGURIDAD DE DATOS ====================
    def hacer_backup(self):
        """Crea backup de todos los datos."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"backup_{timestamp}"
            os.makedirs(backup_dir, exist_ok=True)
            
            archivos_json = [
                "clientes.json", "entrenadores.json", "ejercicios.json",
                "suscripciones.json", "historial_peso.json"
            ]
            
            for archivo in archivos_json:
                if os.path.exists(archivo):
                    with open(archivo, 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                    with open(f"{backup_dir}/{archivo}", 'w', encoding='utf-8') as f:
                        json.dump(datos, f, indent=4, ensure_ascii=False)
            
            return True, f"Backup creado: {backup_dir}"
        except Exception as e:
            return False, f"Error en backup: {str(e)}"