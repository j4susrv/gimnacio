import json
import os
import re
from datetime import datetime, timedelta
from validaciones import Validaciones
from suscripcion import Suscripcion
from historial_peso import HistorialPeso
from cliente import Cliente
from entrenador import TurnoEntrenador
def crear_archivo():
    #se crean los archivos json
    archivos = {
        "clientes.json": [],
        "ejercicios.json": [],
        "entrenadores.json": [],
        "historial_peso.json":[],
        "administradores.json":[
            {
                "rut": "22297344-9",
                "contraseña": "jesusrivera",
                "nombre": "Jesus Rivera" 
            }
        ],
        "suscripciones.json": [],
        "turnos_disponibles.json": [
            {
                "nombre": "Turno Manana (Lun-Vie)",
                "hora_inicio": "07:00:00",
                "hora_fin": "14:00:00"
            },
            {
                "nombre": "Turno Tarde (Lun-Vie)",
                "hora_inicio": "14:00:00",
                "hora_fin": "22:00:00"
            },
            {
                "nombre": "Turno Completo (Lun-Vie)",
                "hora_inicio": "07:00:00",
                "hora_fin": "22:00:00"
            },
            {
                "nombre": "Turno Sabado",
                "hora_inicio": "09:00:00",
                "hora_fin": "17:00:00"
            },
            {
                "nombre": "Turno Domingo",
                "hora_inicio": "12:00:00",
                "hora_fin": "17:00:00"
            }
        ],
        "horas_gimnasio.json": {
            "dias_semanas": {
                "lunes": {"abre": "07:00", "cierra": "22:00", "activo": True},
                "martes": {"abre": "07:00", "cierra": "22:00", "activo": True},
                "miercoles": {"abre": "07:00", "cierra": "22:00", "activo": True},
                "jueves": {"abre": "07:00", "cierra": "22:00", "activo": True},
                "viernes": {"abre": "07:00", "cierra": "22:00", "activo": True},
                "sabado": {"abre": "09:00", "cierra": "17:00", "activo": True},
                "domingo": {"abre": "12:00", "cierra": "17:00", "activo": True}
            }
        }
    }
    for archivo, contenido_inicial in archivos.items():
        if not os.path.exists(archivo):
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(contenido_inicial, f, indent=4, ensure_ascii=False)

# se crea la clase gimnacio
class Gimnasio:
    def __init__(self):
        self.clientes = []
        self.entrenadores = []
        self.administradores = []
        self.ejercicios = []
        self.suscripciones = []
        self.historial_peso = []
        self.turnos_disponibles = []
        self.horario_gimnasio= {}
        crear_archivo()
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            with open("clientes.json", "r", encoding="utf-8") as f:
                self.clientes = json.load(f)
            with open("entrenadores.json", "r", encoding="utf-8") as f:
                self.entrenadores = json.load(f)
            with open("ejercicios.json", "r", encoding="utf-8") as f:
                self.ejercicios = json.load(f)
            with open("administradores.json", "r", encoding="utf-8") as f:
                self.administradores = json.load(f)    
            with open("suscripciones.json", "r", encoding="utf-8") as f:
                self.suscripciones = json.load(f)
            with open("historial_peso.json", "r", encoding="utf-8") as f:
                self.historial_peso = json.load(f)
            with open("turnos_disponibles.json", "r", encoding="utf-8") as f:
                self.turnos_disponibles = json.load(f)
            with open("horas_gimnasio.json", "r", encoding="utf-8") as f:
                self.horario_gimnasio = json.load(f)
        except Exception as e:
            print(f"Error al cargar los datos {e}")
    
    def guardar_datos(self):
        try:
            with open("clientes.json", "w", encoding="utf-8") as f:
                json.dump(self.clientes, f, indent=4, ensure_ascii=False)
            with open("entrenadores.json", "w", encoding="utf-8") as f:
                json.dump(self.entrenadores, f, indent=4, ensure_ascii=False)
            with open("ejercicios.json", "w", encoding="utf-8") as f:
                json.dump(self.ejercicios, f, indent=4, ensure_ascii=False)
            with open("administradores.json", "w", encoding="utf-8") as f:
                json.dump(self.administradores, f, indent=4, ensure_ascii=False)
            with open("suscripciones.json", "w", encoding="utf-8") as f:
                json.dump(self.suscripciones, f, indent=4, ensure_ascii=False)
            with open("historial_peso.json", "w", encoding="utf-8") as f:
                json.dump(self.historial_peso, f, indent=4, ensure_ascii=False)
            with open("turnos_disponibles.json", "w", encoding="utf-8") as f:
                json.dump(self.turnos_disponibles, f, indent=4, ensure_ascii=False)
            with open("horas_gimnasio.json", "w", encoding="utf-8") as f:
                json.dump(self.horario_gimnasio, f, indent=4, ensure_ascii=False)
            return True, "Datos guardados correctamente"
        except Exception as e:
            return False, f"Error al guardar los datos {e}"
    
    #gestion de clientes
    def agregar_cliente(self, cliente):
        # se agregan los clientes si es que no existen
        for c in self.clientes:
            if c["rut"] == cliente.rut:
                return False, "Ya existe un cliente con ese rut"
        
        self.clientes.append(cliente.a_diccionario())
        exito, mensaje = self.guardar_datos()
        if exito:
            return True, f"Cliente {cliente.nombre} agregado exitosamente"
        return False, mensaje
    
    def modificar_cliente(self, rut, nuevo_cliente):
        #se modificaran recoriendo los clientes sy luego los actualiza en el diccionario
        for i, c in enumerate(self.clientes):
            if c["rut"] == rut:
                self.clientes[i] = nuevo_cliente.a_diccionario()
                exito, mensaje = self.guardar_datos()
                if exito:
                    return True, "Cliente modificado exitosamente"
                return False, mensaje
        
        return False, "Cliente no encontrado"
    
    def eliminar_cliente(self, rut):
        # se eliminan de nuevo con un recorrido, buscando el rut y lo eliminan guardando la eliminacion
        for i, c in enumerate(self.clientes):
            if c["rut"] == rut:
                nombre = c["nombre"]
                self.clientes.pop(i)
                exito, mensaje = self.guardar_datos()
                if exito:
                    return True, f"Cliente {nombre} eliminado exitosamente"
                return False, mensaje
        
        return False, "Cliente no encontrado"
    
    def buscar_cliente_por_rut(self, rut):
        for c in self.clientes:
            if c["rut"] == rut:
                return True, c
        return False, "Cliente no encontrado"
    
    #gestion de reportes y consultas
    def listar_clientes_fecha(self, fecha):
        clientes_encontrados = []
        for ejercicio in self.ejercicios:
            if ejercicio["fecha"] == fecha:
                exito, cliente = self.buscar_cliente_por_rut(ejercicio["rut_cliente"])
                if exito and cliente not in clientes_encontrados:
                    clientes_encontrados.append(cliente)
        return clientes_encontrados
    
    def listar_clientes_imc_mayor30(self, fecha):
        clientes_fecha = self.listar_clientes_fecha(fecha)
        clientes_filtrados = [c for c in clientes_fecha if c["imc"] >= 30]
        return clientes_filtrados
    
    def obtener_clientes_por_entrenador(self, nombre_entrenador):
        resultado = {}
        for ejercicio in self.ejercicios:
            if ejercicio["nombre_entrenador"].lower() == nombre_entrenador.lower():
                rut_cliente = ejercicio["rut_cliente"]
                fecha = ejercicio["fecha"]
                exito, cliente = self.buscar_cliente_por_rut(rut_cliente)
                if exito:
                    nombre_cliente = cliente["nombre"]
                    if nombre_cliente not in resultado:
                        resultado[nombre_cliente] = {
                            "rut": rut_cliente,
                            "fechas": [],
                            "total_sesiones": 0
                        }
                    if fecha not in resultado[nombre_cliente]["fechas"]:
                        resultado[nombre_cliente]["fechas"].append(fecha)
                        resultado[nombre_cliente]["total_sesiones"] += 1
        return resultado
    
    def obtener_ejercicios_por_entrenador(self, nombre_entrenador):
        ejercicios_entrenador = [
            ej for ej in self.ejercicios
            if ej["nombre_entrenador"].lower() == nombre_entrenador.lower()
        ]
        return ejercicios_entrenador
    
    def contar_clientes_activos_entrenador(self, nombre_entrenador):
        clientes = self.obtener_clientes_por_entrenador(nombre_entrenador)
        return len(clientes)
    
    #gestion de suscripciones
    def crear_suscripcion(self, suscripcion):
        exito, cliente = self.buscar_cliente_por_rut(suscripcion.rut_cliente)
        if not exito:
            return False, "El cliente no existe en el sistema"
        
        for sus in self.suscripciones:
            if sus["rut_cliente"] == suscripcion.rut_cliente and sus.get("activa", True):
                sus["activa"] = False
        
        self.suscripciones.append(suscripcion.a_diccionario())
        exito, mensaje = self.guardar_datos()
        if exito:
            return True, f"Suscripcion {suscripcion.tipo_suscripcion} creada hasta {suscripcion.fecha_fin}"
        return False, mensaje
    
    def buscar_suscripcion_activa(self, rut_cliente):
            for sus in self.suscripciones:
                if sus["rut_cliente"] == rut_cliente:
                    if isinstance(sus["fecha_fin"], str):
                        # Intentar formato chileno primero, luego ISO
                        try:
                            fecha_fin = datetime.strptime(sus["fecha_fin"], "%d-%m-%Y")
                        except ValueError:
                            try:
                                fecha_fin = datetime.strptime(sus["fecha_fin"], "%Y-%m-%d")
                            except ValueError:
                                continue
                    else:
                        fecha_fin = sus["fecha_fin"]
                    
                    if datetime.now() <= fecha_fin:
                        return True, sus
            
            return False, "No hay suscripcion activa para este cliente"
        
    def renovar_suscripcion(self, rut_cliente, tipo_suscripcion, monto):
        # Usar formato chileno
        fecha_inicio = datetime.now().strftime("%d-%m-%Y")
        nueva_suscripcion = Suscripcion(rut_cliente, tipo_suscripcion, fecha_inicio, monto)
        return self.crear_suscripcion(nueva_suscripcion)
    
    def listar_suscripciones_por_vencer(self, dias=7):
        suscripciones_por_vencer = []
        fecha_limite = datetime.now() + timedelta(days=dias)
        
        for sus in self.suscripciones:
            if sus.get("activa", True):
                if isinstance(sus["fecha_fin"], str):
                    # Intentar formato chileno primero, luego ISO
                    try:
                        fecha_fin = datetime.strptime(sus["fecha_fin"], "%d-%m-%Y")
                    except ValueError:
                        try:
                            fecha_fin = datetime.strptime(sus["fecha_fin"], "%Y-%m-%d")
                        except ValueError:
                            continue
                else:
                    fecha_fin = sus["fecha_fin"]
                
                if datetime.now() < fecha_fin <= fecha_limite:
                    exito, cliente = self.buscar_cliente_por_rut(sus["rut_cliente"])
                    if exito:
                        sus_completa = sus.copy()
                        sus_completa["nombre_cliente"] = cliente["nombre"]
                        suscripciones_por_vencer.append(sus_completa)
        
        return suscripciones_por_vencer
    
    #gestion de peso
    def registrar_peso(self, historial):
        exito, cliente = self.buscar_cliente_por_rut(historial.rut_cliente)
        if not exito:
            return False, "El cliente no existe en el sistema"
        
        for i, c in enumerate(self.clientes):
            if c["rut"] == historial.rut_cliente:
                self.clientes[i]["peso"] = historial.peso
                estatura_m = c["estatura"] / 100
                nuevo_imc = round(historial.peso / (estatura_m ** 2), 2)
                self.clientes[i]["imc"] = nuevo_imc
                break
        
        self.historial_peso.append(historial.a_diccionario())
        exito, mensaje = self.guardar_datos()
        if exito:
            return True, f"Peso {historial.peso} kg registrado para el cliente"
        return False, mensaje
    
    def obtener_historial_peso_cliente(self, rut_cliente):
        historial = [h for h in self.historial_peso if h["rut_cliente"] == rut_cliente]
        historial.sort(key=lambda x: x["fecha"])
        return historial
    
    def calcular_progreso_peso(self, rut_cliente):
        historial = self.obtener_historial_peso_cliente(rut_cliente)
        if len(historial) < 2:
            return None, "No hay suficientes registros para calcular progreso"
        
        peso_inicial = historial[0]["peso"]
        peso_actual = historial[-1]["peso"]
        diferencia = peso_actual - peso_inicial
        
        return {
            "peso_inicial": peso_inicial,
            "peso_actual": peso_actual,
            "diferencia": round(diferencia, 2),
            "progreso": "Bajó" if diferencia < 0 else "Subió" if diferencia > 0 else "Mantuvo"
        }, "Progreso calculado"
    
    #gestion de entranador
    def asignar_turno_entrenador(self, turno):
        exito, _ = self.buscar_entrenador_por_rut(turno.rut_entrenador)
        if not exito:
            return False, "El entrenador no existe en el sistema"
        for t in self.turno_entrenadores:
            if t["rut_entrenador"] == turno.rut_entrenador and t["dia_semana"] == turno.dia_semana:
                return False, f"El entrenador ya tiene un turno asignado el {turno.dia_semana}"
        self.turno_entrenadores.append(turno.a_diccionario())
        exito, mensaje = self.guardar_datos()
        
        if exito:
            return True, f"Turno asignado: {turno.dia_semana} de {turno.hora_inicio} a {turno.hora_fin}"
        return False, mensaje
    
    def obtener_turnos_entrenador(self, rut_entrenador):
        turnos = [t for t in self.turno_entrenadores if t["rut_entrenador"] == rut_entrenador]
        return turnos
    
    def calcular_horas_semanales_entrenador(self, rut_entrenador):
        turnos = self.obtener_turnos_entrenador(rut_entrenador)
        total_horas = sum(t["horas_trabajo"] for t in turnos)
        return round(total_horas, 2)
    def entrenador_disponible_ahora(self, rut_entrenador):
        """
        Verifica si un entrenador está disponible AHORA
        Retorna: (bool, dict o None)
        """
        
        return TurnoEntrenador.esta_disponible(rut_entrenador, self.turno_entrenadores)
    def cargar_turnos_disponibles(self):
        """Carga los turnos desde el archivo JSON"""
        try:
            if os.path.exists("turnos_disponibles.json"):
                with open("turnos_disponibles.json", "r", encoding="utf-8") as f:
                    self.turnos_disponibles = json.load(f)
            else:
                self.turnos_disponibles = []
        except Exception as e:
            print(f"Error al cargar turnos: {e}")
            self.turnos_disponibles = []
    def listar_entrenadores_disponibles(self, dia_semana, hora):
        #se listan los entrenadores disponibles y se guardan temporalmente en entrenadores_disponibles
        #se obtienen los turnos y los dias de la semana con sus horas y luego se verifican los entrenadores disponibles
        #por especialidad
        entrenadores_disponibles = []
        for entrenador in self.entrenadores:
            turnos = self.obtener_turnos_entrenador(entrenador["rut"])
            for turno in turnos:
                if turno["dia_semana"] == dia_semana.lower():
                    hora_dt = datetime.strptime(hora, "%H:%M")
                    hora_inicio = datetime.strptime(turno["hora_inicio"], "%H:%M")
                    hora_fin = datetime.strptime(turno["hora_fin"], "%H:%M")
                    if hora_inicio <= hora_dt <= hora_fin:
                        entrenadores_disponibles.append({
                            "nombre": entrenador["nombre"],
                            "rut": entrenador["rut"],
                            "especialidades": entrenador.get("especialidades", []),
                            "turno": f"{turno['hora_inicio']} - {turno['hora_fin']}"
                        })
                        break
        return entrenadores_disponibles
    
    def eliminar_turno_entrenador(self, rut_entrenador, dia_semana):
        for i, turno in enumerate(self.turno_entrenadores):
            if turno["rut_entrenador"] == rut_entrenador and turno["dia_semana"] == dia_semana.lower():
                self.turno_entrenadores.pop(i)
                exito, mensaje = self.guardar_datos()
                
                if exito:
                    return True, f"Turno del {dia_semana} eliminado"
                return False, mensaje
        
        return False, "Turno no encontrado"
    
    #gestion de horario del gimnacio
    def modificar_horario_gimnasio(self, dia_semana, hora_abre, hora_cierra, activo=True):
        if dia_semana.lower() in self.horario_gimnasio["dias_semanas"]:
            self.horario_gimnasio["dias_semanas"][dia_semana.lower()] = {
                "abre": hora_abre,
                "cierra": hora_cierra,
                "activo": activo
            }
            exito, mensaje = self.guardar_datos()
            if exito:
                return True, f"Horario del {dia_semana} actualizado"
            return False, mensaje
        return False, "Día de la semana inválido"
    
    def obtener_horario_gimnasio(self):
        return self.horario_gimnasio
    
    def gimnasio_esta_abierto(self, dia_semana, hora):
        #ve si el gimnacio esta abierto o cerrado con el horario del gimnacio
        if dia_semana.lower() not in self.horario_gimnasio["dias_semanas"]:
            return False, "Día inválido"
        
        horario_dia = self.horario_gimnasio["dias_semanas"][dia_semana.lower()]
        if not horario_dia["activo"]:
            return False, f"El gimnasio está cerrado los {dia_semana}"
        hora_dt = datetime.strptime(hora, "%H:%M")
        hora_abre = datetime.strptime(horario_dia["abre"], "%H:%M")
        hora_cierra = datetime.strptime(horario_dia["cierra"], "%H:%M")
        if hora_abre <= hora_dt <= hora_cierra:
            return True, "El gimnasio está abierto"
        else:
            return False, f"El gimnasio está cerrado. Horario: {horario_dia['abre']} - {horario_dia['cierra']}"
    def obtener_estado_actual(self):
            """
            Verifica si el gimnasio está abierto AHORA (en tiempo real).
            Retorna: (bool, str) - (está_abierto, mensaje)
            """
            # Obtener día y hora actual
            ahora = datetime.now()
            dias_nombres = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
            dia_actual = dias_nombres[ahora.weekday()]  # 0=lunes, 6=domingo
            hora_actual = ahora.strftime("%H:%M")
            
            # Usar el método existente
            esta_abierto, mensaje_base = self.gimnasio_esta_abierto(dia_actual, hora_actual)
            
            # Personalizar el mensaje para la interfaz
            if esta_abierto:
                horario_dia = self.horario_gimnasio["dias_semanas"][dia_actual]
                mensaje = f"¡Abierto! - Hoy cerramos a las {horario_dia['cierra']}"
            else:
                # Si está cerrado, mostrar cuándo abre
                if dia_actual in self.horario_gimnasio["dias_semanas"]:
                    horario_dia = self.horario_gimnasio["dias_semanas"][dia_actual]
                    if horario_dia["activo"]:
                        mensaje = f"Cerrado - Abrimos a las {horario_dia['abre']}"
                    else:
                        mensaje = f"Cerrado - Los {dia_actual} no hay servicio"
                else:
                    mensaje = "Cerrado - Horario no disponible"
            
            return esta_abierto, mensaje
        
    def obtener_horarios_semana(self):
        """
        Obtiene el horario completo de la semana
        Retorna: dict con todos los días
        """
        return self.horario_gimnasio.get("dias_semanas", {})
    #gestion de entrenador
    def agregar_entrenador(self, entrenador):
        # se agrega un entrenador y si el rut es el mismo lo da por existente y si no, se crea en el diccionario
        for e in self.entrenadores:
            if e["rut"] == entrenador.rut:
                return False, "Ya existe un entrenador con ese RUT"
        self.entrenadores.append(entrenador.a_diccionario())
        exito, mensaje = self.guardar_datos()
        if exito:
            return True, f"Entrenador {entrenador.nombre} agregado exitosamente"
        return False, mensaje
    
    def buscar_entrenador_por_rut(self, rut):
        for e in self.entrenadores:
            if e["rut"] == rut:
                return True, e
        return False, "Entrenador no encontrado"
    
    def listar_todos_entrenadores(self):
        return self.entrenadores
    
    def modificar_entrenador(self, rut, nuevo_entrenador):
        for i, e in enumerate(self.entrenadores):
            if e["rut"] == rut:
                self.entrenadores[i] = nuevo_entrenador.a_diccionario()
                exito, mensaje = self.guardar_datos()
                
                if exito:
                    return True, "Entrenador modificado exitosamente"
                return False, mensaje
        
        return False, "Entrenador no encontrado"
    
    def eliminar_entrenador(self, rut):
        # se va a recorrer un ciclo que va a tomar a todos los entrenadores con sus rut y el elegido
        # se va a elimnar y se va a actualizar
        for i, e in enumerate(self.entrenadores):
            if e["rut"] == rut:
                nombre = e["nombre"]
                self.entrenadores.pop(i)
                exito, mensaje= self.guardar_datos()
                if exito:
                    return True, f"Entrenador {nombre} eliminado exitosamente"
                return False, mensaje
        
        return False, "Entrenador no encontrado"
    
    #gestion de ejercicios
    def registrar_ejercicio(self, ejercicio):
        exito_cliente, _ = self.buscar_cliente_por_rut(ejercicio.rut_cliente)
        if not exito_cliente:
            return False, "El cliente no existe en el sistema"
        
        exito_entrenador = False
        for e in self.entrenadores:
            if e["nombre"].lower() == ejercicio.nombre_entrenador.lower():
                exito_entrenador = True
                break
        
        if not exito_entrenador:
            return False, "El entrenador no existe en el sistema"
        
        self.ejercicios.append(ejercicio.a_diccionario())
        exito, mensaje = self.guardar_datos()
        
        if exito:
            return True, "Ejercicio registrado exitosamente"
        return False, mensaje
    
    def buscar_ejercicios_por_cliente(self, rut_cliente):
        # se va a generar un for que va a buscar todos los ejercicicios de un determinado cliente a traves de el rut
        ejercicios_cliente = [ej for ej in self.ejercicios if ej["rut_cliente"] == rut_cliente]
        if ejercicios_cliente:
            return True, ejercicios_cliente
        return False, "No se encontraron ejercicios para este cliente"
    
    def buscar_ejercicios_por_fecha(self, fecha):
        ejercicios_fecha = [ej for ej in self.ejercicios if ej["fecha"] == fecha]
        
        if ejercicios_fecha:
            return True, ejercicios_fecha
        return False, "No se encontraron ejercicios en esa fecha"
    
    def listar_todos_ejercicios(self):
        return self.ejercicios
    
    def modificar_ejercicio(self, indice, nuevo_ejercicio):
        #Aqui se va a poder modificar el ejercicio
        if 0 <= indice < len(self.ejercicios):
            #aqui se va a guardar el nuevo ejercicio
            self.ejercicios[indice] = nuevo_ejercicio.a_diccionario()
            exito, mensaje = self.guardar_datos()
            if exito:
                return True, "Ejercicio modificado exitosamente"
            return False, mensaje
        return False, "Índice de ejercicio inválido"
    
    def eliminar_ejercicio(self, indice):
        #se va a poder eliminar el ejercicio con pop y eso se modifica y se actualiza
        if 0 <= indice < len(self.ejercicios):
            ejercicio = self.ejercicios.pop(indice)
            exito, mensaje= self.guardar_datos()
            if exito:
                return True, f"Ejercicio eliminado exitosamente"
            return False, mensaje
        
        return False, "Índice de ejercicio inválido"


    def eliminar_suscripcion(self, id_suscripcion):
        """
        Elimina una suscripción por su ID.
        Retorna (True, "mensaje") si se elimina, o (False, "mensaje de error") si falla.
        """
        archivo_suscripciones = "suscripciones.json"
        if not os.path.exists(archivo_suscripciones):
            return False, "No se encontró archivo de suscripciones."
        
        try:
            with open(archivo_suscripciones, "r", encoding="utf-8") as f:
                suscripciones = json.load(f)
            
            # Buscar la suscripción por ID
            sus_a_eliminar = None
            for sus in suscripciones:
                if sus.get('id') == id_suscripcion:
                    sus_a_eliminar = sus
                    break
            
            if not sus_a_eliminar:
                return False, "No se encontró la suscripción."
            
            suscripciones.remove(sus_a_eliminar)
            
            # Guardar los cambios
            with open(archivo_suscripciones, "w", encoding="utf-8") as f:
                json.dump(suscripciones, f, indent=4, ensure_ascii=False)
            
            return True, "Suscripción eliminada correctamente."
        
        except Exception as e:
            return False, f"Error al eliminar suscripción: {str(e)}"
