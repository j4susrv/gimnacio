import json
import os
import re
from datetime import datetime, timedelta
from validaciones import Validaciones
from suscripcion import Suscripcion
from historial_peso import HistorialPeso
from cliente import Cliente

def crear_archivo():
    # Define diccionario con nombres de archivos y su contenido inicial
    archivos = {
        "clientes.json": [],  # Archivo para almacenar clientes (lista vacía)
        "ejercicios.json": [],  # Archivo para almacenar ejercicios (lista vacía)
        "entrenadores.json": [],  # Archivo para almacenar entrenadores (lista vacía)
        "historial_peso.json":[],  # Archivo para historial de pesos (lista vacía)
        "administradores.json":[  # Archivo para administradores con datos iniciales
            {
                "rut": "22297344-9",  # RUT del administrador por defecto
                "contraseña": "jesusrivera",  # Contraseña del administrador
                "nombre": "Jesus Rivera"  # Nombre del administrador
            }
        ],
        "suscripciones.json": [],  # Archivo para suscripciones (lista vacía)
        "turnos_entrenadores.json": [],  # Archivo para turnos de entrenadores (lista vacía)
        "horas_gimnasio.json": {  # Archivo para horarios del gimnasio
            "dias_semanas": {  # Diccionario con horarios por día
                "lunes": {"abre": "07:00", "cierra": "22:00", "activo": True},  # Horario lunes
                "martes": {"abre": "07:00", "cierra": "22:00", "activo": True},  # Horario martes
                "miercoles": {"abre": "07:00", "cierra": "22:00", "activo": True},  # Horario miércoles
                "jueves": {"abre": "07:00", "cierra": "22:00", "activo": True},  # Horario jueves
                "viernes": {"abre": "07:00", "cierra": "22:00", "activo": True},  # Horario viernes
                "sabado": {"abre": "09:00", "cierra": "17:00", "activo": True},  # Horario sábado
                "domingo": {"abre": "12:00", "cierra": "17:00", "activo": True}  # Horario domingo
            }
        }
    }
    # Itera sobre cada archivo y contenido definido
    for archivo, contenido_inicial in archivos.items():
        # Verifica si el archivo no existe
        if not os.path.exists(archivo):
            # Abre el archivo en modo escritura
            with open(archivo, "w", encoding="utf-8") as f:
                # Escribe el contenido inicial en formato JSON
                json.dump(contenido_inicial, f, indent=4, ensure_ascii=False)

# Define la clase principal Gimnasio
class Gimnacio:
    def __init__(self):
        # Inicializa lista de clientes vacía
        self.clientes = []
        # Inicializa lista de entrenadores vacía
        self.entrenadores = []
        # Inicializa lista de administradores vacía
        self.administradores = []
        # Inicializa lista de ejercicios vacía
        self.ejercicios = []
        # Inicializa lista de suscripciones vacía
        self.suscripciones = []
        # Inicializa lista de historial de pesos vacía
        self.historial_peso = []
        # Inicializa lista de turnos de entrenadores vacía
        self.turno_entrenadores = []
        # Inicializa diccionario de horarios del gimnasio vacío
        self.horario_gimnasio= {}
        # Llama función para crear archivos si no existen
        crear_archivo()
        # Carga datos desde archivos JSON
        self.cargar_datos()
    
    def cargar_datos(self):
        try:
            # Abre y carga datos de clientes desde JSON
            with open("clientes.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de clientes
                self.clientes = json.load(f)
            # Abre y carga datos de entrenadores desde JSON
            with open("entrenadores.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de entrenadores
                self.entrenadores = json.load(f)
            # Abre y carga datos de ejercicios desde JSON
            with open("ejercicios.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de ejercicios
                self.ejercicios = json.load(f)
            # Abre y carga datos de administradores desde JSON
            with open("administradores.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de administradores
                self.administradores = json.load(f)    
            # Abre y carga datos de suscripciones desde JSON
            with open("suscripciones.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de suscripciones
                self.suscripciones = json.load(f)
            # Abre y carga datos de historial de peso desde JSON
            with open("historial_peso.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de historial de peso
                self.historial_peso = json.load(f)
            # Abre y carga datos de turnos de entrenadores desde JSON
            with open("turnos_entrenadores.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a lista de turnos de entrenadores
                self.turno_entrenadores = json.load(f)
            # Abre y carga datos de horarios del gimnasio desde JSON
            with open("horas_gimnasio.json", "r", encoding="utf-8") as f:
                # Asigna datos cargados a diccionario de horarios
                self.horario_gimnasio = json.load(f)
        # Captura cualquier excepción durante la carga
        except Exception as e:
            # Imprime mensaje de error
            print(f"Error al cargar los datos {e}")
    
    def guardar_datos(self):
        try:
            # Abre archivo de clientes en modo escritura
            with open("clientes.json", "w", encoding="utf-8") as f:
                # Guarda lista de clientes en formato JSON
                json.dump(self.clientes, f, indent=4, ensure_ascii=False)
            # Abre archivo de entrenadores en modo escritura
            with open("entrenadores.json", "w", encoding="utf-8") as f:
                # Guarda lista de entrenadores en formato JSON
                json.dump(self.entrenadores, f, indent=4, ensure_ascii=False)
            # Abre archivo de ejercicios en modo escritura
            with open("ejercicios.json", "w", encoding="utf-8") as f:
                # Guarda lista de ejercicios en formato JSON
                json.dump(self.ejercicios, f, indent=4, ensure_ascii=False)
            # Abre archivo de administradores en modo escritura
            with open("administradores.json", "w", encoding="utf-8") as f:
                # Guarda lista de administradores en formato JSON
                json.dump(self.administradores, f, indent=4, ensure_ascii=False)
            # Abre archivo de suscripciones en modo escritura
            with open("suscripciones.json", "w", encoding="utf-8") as f:
                # Guarda lista de suscripciones en formato JSON
                json.dump(self.suscripciones, f, indent=4, ensure_ascii=False)
            # Abre archivo de historial de peso en modo escritura
            with open("historial_peso.json", "w", encoding="utf-8") as f:
                # Guarda lista de historial de peso en formato JSON
                json.dump(self.historial_peso, f, indent=4, ensure_ascii=False)
            # Abre archivo de turnos de entrenadores en modo escritura
            with open("turnos_entrenadores.json", "w", encoding="utf-8") as f:
                # Guarda lista de turnos de entrenadores en formato JSON
                json.dump(self.turno_entrenadores, f, indent=4, ensure_ascii=False)
            # Abre archivo de horarios del gimnasio en modo escritura
            with open("horas_gimnasio.json", "w", encoding="utf-8") as f:
                # Guarda diccionario de horarios en formato JSON
                json.dump(self.horario_gimnasio, f, indent=4, ensure_ascii=False)
            # Retorna éxito y mensaje de confirmación
            return True, "Datos guardados correctamente"
        # Captura cualquier excepción durante el guardado
        except Exception as e:
            # Retorna fallo y mensaje de error
            return False, f"Error al guardar los datos {e}"
    
    # Método para agregar un nuevo cliente
    def agregar_cliente(self, cliente):
        # Itera sobre clientes existentes
        for c in self.clientes:
            # Verifica si ya existe un cliente con el mismo RUT
            if c["rut"] == cliente.rut:
                # Retorna fallo si el cliente ya existe
                return False, "Ya existe un cliente con ese rut"
        
        # Agrega cliente convertido a diccionario a la lista
        self.clientes.append(cliente.a_diccionario())
        # Intenta guardar los datos
        exito, mensaje = self.guardar_datos()
        # Verifica si el guardado fue exitoso
        if exito:
            # Retorna éxito y mensaje de confirmación
            return True, f"Cliente {cliente.nombre} agregado exitosamente"
        # Retorna fallo y mensaje de error
        return False, mensaje
    
    # Método para modificar un cliente existente
    def modificar_cliente(self, rut, nuevo_cliente):
        # Itera sobre clientes con índice
        for i, c in enumerate(self.clientes):
            # Busca cliente por RUT
            if c["rut"] == rut:
                # Reemplaza cliente existente con nuevo cliente
                self.clientes[i] = nuevo_cliente.a_diccionario()
                # Intenta guardar los datos
                exito, mensaje = self.guardar_datos()
                # Verifica si el guardado fue exitoso
                if exito:
                    # Retorna éxito y mensaje de confirmación
                    return True, "Cliente modificado exitosamente"
                # Retorna fallo y mensaje de error
                return False, mensaje
        
        # Retorna fallo si no encuentra el cliente
        return False, "Cliente no encontrado"
    
    # Método para eliminar un cliente
    def eliminar_cliente(self, rut):
        # Itera sobre clientes con índice
        for i, c in enumerate(self.clientes):
            # Busca cliente por RUT
            if c["rut"] == rut:
                # Guarda nombre del cliente para mensaje
                nombre = c["nombre"]
                # Elimina cliente de la lista
                self.clientes.pop(i)
                # Intenta guardar los datos
                exito, mensaje = self.guardar_datos()
                # Verifica si el guardado fue exitoso
                if exito:
                    # Retorna éxito y mensaje de confirmación
                    return True, f"Cliente {nombre} eliminado exitosamente"
                # Retorna fallo y mensaje de error
                return False, mensaje
        
        # Retorna fallo si no encuentra el cliente
        return False, "Cliente no encontrado"
    
    # Método para buscar cliente por RUT
    def buscar_cliente_por_rut(self, rut):
        # Itera sobre clientes
        for c in self.clientes:
            # Busca cliente por RUT
            if c["rut"] == rut:
                # Retorna éxito y datos del cliente
                return True, c
        # Retorna fallo si no encuentra el cliente
        return False, "Cliente no encontrado"
    
    # Método para listar clientes por fecha de ejercicio
    def listar_clientes_fecha(self, fecha):
        # Inicializa lista vacía para clientes encontrados
        clientes_encontrados = []
        # Itera sobre ejercicios
        for ejercicio in self.ejercicios:
            # Verifica si el ejercicio coincide con la fecha
            if ejercicio["fecha"] == fecha:
                # Busca cliente por RUT del ejercicio
                exito, cliente = self.buscar_cliente_por_rut(ejercicio["rut_cliente"])
                # Verifica si se encontró el cliente y no está duplicado
                if exito and cliente not in clientes_encontrados:
                    # Agrega cliente a la lista
                    clientes_encontrados.append(cliente)
        # Retorna lista de clientes encontrados
        return clientes_encontrados
    
    # Método para listar clientes con IMC mayor a 30 en fecha específica
    def listar_clientes_imc_mayor30(self, fecha):
        # Obtiene clientes de la fecha específica
        clientes_fecha = self.listar_clientes_fecha(fecha)
        # Filtra clientes con IMC >= 30
        clientes_filtrados = [c for c in clientes_fecha if c["imc"] >= 30]
        # Retorna clientes filtrados
        return clientes_filtrados
    
    # Método para obtener clientes por entrenador
    def obtener_clientes_por_entrenador(self, nombre_entrenador):
        # Inicializa diccionario vacío para resultados
        resultado = {}
        # Itera sobre ejercicios
        for ejercicio in self.ejercicios:
            # Verifica si el entrenador coincide
            if ejercicio["nombre_entrenador"].lower() == nombre_entrenador.lower():
                # Obtiene RUT del cliente
                rut_cliente = ejercicio["rut_cliente"]
                # Obtiene fecha del ejercicio
                fecha = ejercicio["fecha"]
                # Busca cliente por RUT
                exito, cliente = self.buscar_cliente_por_rut(rut_cliente)
                # Verifica si se encontró el cliente
                if exito:
                    # Obtiene nombre del cliente
                    nombre_cliente = cliente["nombre"]
                    # Verifica si el cliente no está en resultados
                    if nombre_cliente not in resultado:
                        # Inicializa datos del cliente en resultados
                        resultado[nombre_cliente] = {
                            "rut": rut_cliente,
                            "fechas": [],
                            "total_sesiones": 0
                        }
                    # Verifica si la fecha no está registrada
                    if fecha not in resultado[nombre_cliente]["fechas"]:
                        # Agrega fecha a la lista
                        resultado[nombre_cliente]["fechas"].append(fecha)
                        # Incrementa contador de sesiones
                        resultado[nombre_cliente]["total_sesiones"] += 1
        # Retorna diccionario con resultados
        return resultado
    
    # Método para obtener ejercicios por entrenador
    def obtener_ejercicios_por_entrenador(self, nombre_entrenador):
        # Filtra ejercicios por nombre de entrenador
        ejercicios_entrenador = [
            ej for ej in self.ejercicios
            if ej["nombre_entrenador"].lower() == nombre_entrenador.lower()
        ]
        # Retorna lista de ejercicios del entrenador
        return ejercicios_entrenador
    
    # Método para contar clientes activos por entrenador
    def contar_clientes_activos_entrenador(self, nombre_entrenador):
        # Obtiene clientes del entrenador
        clientes = self.obtener_clientes_por_entrenador(nombre_entrenador)
        # Retorna cantidad de clientes
        return len(clientes)
    
    # Método para crear nueva suscripción
    def crear_suscripcion(self, suscripcion):
        # Verifica si el cliente existe
        exito, cliente = self.buscar_cliente_por_rut(suscripcion.rut_cliente)
        if not exito:
            # Retorna fallo si el cliente no existe
            return False, "El cliente no existe en el sistema"
        
        # Itera sobre suscripciones existentes
        for sus in self.suscripciones:
            # Busca suscripciones activas del mismo cliente
            if sus["rut_cliente"] == suscripcion.rut_cliente and sus.get("activa", True):
                # Desactiva suscripción anterior
                sus["activa"] = False
        
        # Agrega nueva suscripción a la lista
        self.suscripciones.append(suscripcion.a_diccionario())
        # Intenta guardar los datos
        exito, mensaje = self.guardar_datos()
        # Verifica si el guardado fue exitoso
        if exito:
            # Retorna éxito y mensaje de confirmación
            return True, f"Suscripcion {suscripcion.tipo_suscripcion} creada hasta {suscripcion.fecha_fin}"
        # Retorna fallo y mensaje de error
        return False, mensaje
    
    # Método para buscar suscripción activa por RUT de cliente
    def buscar_suscripcion_activa(self, rut_cliente):
        # Itera sobre suscripciones
        for sus in self.suscripciones:
            # Busca suscripción del cliente
            if sus["rut_cliente"] == rut_cliente:
                # Convierte fecha fin a objeto datetime si es string
                if isinstance(sus["fecha_fin"], str):
                    fecha_fin = datetime.strptime(sus["fecha_fin"], "%Y-%m-%d")
                else:
                    fecha_fin = sus["fecha_fin"]
                
                # Verifica si la suscripción está vigente
                if datetime.now() <= fecha_fin:
                    # Retorna éxito y datos de suscripción
                    return True, sus
        
        # Retorna fallo si no hay suscripción activa
        return False, "No hay suscripcion activa para este cliente"
    
    # Método para renovar suscripción existente
    def renovar_suscripcion(self, rut_cliente, tipo_suscripcion, monto):
        # Obtiene fecha actual en formato string
        fecha_inicio = datetime.now().strftime("%Y-%m-%d")
        # Crea nueva instancia de Suscripcion
        nueva_suscripcion = Suscripcion(rut_cliente, tipo_suscripcion, fecha_inicio, monto)
        # Llama método para crear suscripción
        return self.crear_suscripcion(nueva_suscripcion)
    
    # Método para listar suscripciones próximas a vencer
    def listar_suscripciones_por_vencer(self, dias=7):
        # Inicializa lista vacía para resultados
        suscripciones_por_vencer = []
        # Calcula fecha límite (hoy + días especificados)
        fecha_limite = datetime.now() + timedelta(days=dias)
        
        # Itera sobre suscripciones
        for sus in self.suscripciones:
            # Verifica si la suscripción está activa
            if sus.get("activa", True):
                # Convierte fecha fin a objeto datetime si es string
                if isinstance(sus["fecha_fin"], str):
                    fecha_fin = datetime.strptime(sus["fecha_fin"], "%Y-%m-%d")
                else:
                    fecha_fin = sus["fecha_fin"]
                
                # Verifica si la suscripción vence dentro del rango
                if datetime.now() < fecha_fin <= fecha_limite:
                    # Busca datos del cliente
                    exito, cliente = self.buscar_cliente_por_rut(sus["rut_cliente"])
                    # Verifica si se encontró el cliente
                    if exito:
                        # Crea copia de datos de suscripción
                        sus_completa = sus.copy()
                        # Agrega nombre del cliente
                        sus_completa["nombre_cliente"] = cliente["nombre"]
                        # Agrega suscripción a la lista
                        suscripciones_por_vencer.append(sus_completa)
        
        # Retorna lista de suscripciones por vencer
        return suscripciones_por_vencer
    
    # Método para registrar peso de cliente
    def registrar_peso(self, historial):
        # Verifica si el cliente existe
        exito, cliente = self.buscar_cliente_por_rut(historial.rut_cliente)
        if not exito:
            # Retorna fallo si el cliente no existe
            return False, "El cliente no existe en el sistema"
        
        # Itera sobre clientes con índice
        for i, c in enumerate(self.clientes):
            # Busca cliente por RUT
            if c["rut"] == historial.rut_cliente:
                # Actualiza peso del cliente
                self.clientes[i]["peso"] = historial.peso
                # Convierte estatura a metros
                estatura_m = c["estatura"] / 100
                # Calcula nuevo IMC
                nuevo_imc = round(historial.peso / (estatura_m ** 2), 2)
                # Actualiza IMC del cliente
                self.clientes[i]["imc"] = nuevo_imc
                # Termina el bucle
                break
        
        # Agrega registro al historial de peso
        self.historial_peso.append(historial.a_diccionario())
        # Intenta guardar los datos
        exito, mensaje = self.guardar_datos()
        # Verifica si el guardado fue exitoso
        if exito:
            # Retorna éxito y mensaje de confirmación
            return True, f"Peso {historial.peso} kg registrado para el cliente"
        # Retorna fallo y mensaje de error
        return False, mensaje
    
    # Método para obtener historial de peso por RUT de cliente
    def obtener_historial_peso_cliente(self, rut_cliente):
        # Filtra registros de peso por RUT de cliente
        historial = [h for h in self.historial_peso if h["rut_cliente"] == rut_cliente]
        # Ordena historial por fecha
        historial.sort(key=lambda x: x["fecha"])
        # Retorna historial ordenado
        return historial
    
    # Método para calcular progreso de peso
    def calcular_progreso_peso(self, rut_cliente):
        # Obtiene historial de peso del cliente
        historial = self.obtener_historial_peso_cliente(rut_cliente)
        # Verifica si hay suficientes registros
        if len(historial) < 2:
            # Retorna fallo si no hay suficientes datos
            return None, "No hay suficientes registros para calcular progreso"
        
        # Obtiene peso inicial (primer registro)
        peso_inicial = historial[0]["peso"]
        # Obtiene peso actual (último registro)
        peso_actual = historial[-1]["peso"]
        # Calcula diferencia de peso
        diferencia = peso_actual - peso_inicial
        
        # Retorna diccionario con resultados del progreso
        return {
            "peso_inicial": peso_inicial,
            "peso_actual": peso_actual,
            "diferencia": round(diferencia, 2),
            "progreso": "Bajó" if diferencia < 0 else "Subió" if diferencia > 0 else "Mantuvo"
        }, "Progreso calculado"
    
    # Método para asignar turno a entrenador
    def asignar_turno_entrenador(self, turno):
        # Verifica si el entrenador existe
        exito, _ = self.buscar_entrenador_por_rut(turno.rut_entrenador)
        if not exito:
            # Retorna fallo si el entrenador no existe
            return False, "El entrenador no existe en el sistema"
        # Itera sobre turnos existentes
        for t in self.turno_entrenadores:
            # Verifica si ya existe turno el mismo día
            if t["rut_entrenador"] == turno.rut_entrenador and t["dia_semana"] == turno.dia_semana:
                # Retorna fallo si ya tiene turno ese día
                return False, f"El entrenador ya tiene un turno asignado el {turno.dia_semana}"
        # Agrega nuevo turno a la lista
        self.turno_entrenadores.append(turno.a_diccionario())
        # Intenta guardar los datos
        exito, mensaje = self.guardar_datos()
        
        # Verifica si el guardado fue exitoso
        if exito:
            # Retorna éxito y mensaje de confirmación
            return True, f"Turno asignado: {turno.dia_semana} de {turno.hora_inicio} a {turno.hora_fin}"
        # Retorna fallo y mensaje de error
        return False, mensaje
    
    # Método para obtener turnos por RUT de entrenador
    def obtener_turnos_entrenador(self, rut_entrenador):
        # Filtra turnos por RUT de entrenador
        turnos = [t for t in self.turno_entrenadores if t["rut_entrenador"] == rut_entrenador]
        # Retorna lista de turnos
        return turnos
    
    # Método para calcular horas semanales de entrenador
    def calcular_horas_semanales_entrenador(self, rut_entrenador):
        # Obtiene turnos del entrenador
        turnos = self.obtener_turnos_entrenador(rut_entrenador)
        # Suma horas de trabajo de todos los turnos
        total_horas = sum(t["horas_trabajo"] for t in turnos)
        # Retorna total de horas redondeado
        return round(total_horas, 2)
    
    # Método para listar entrenadores disponibles en día y hora específicos
    def listar_entrenadores_disponibles(self, dia_semana, hora):
        # Inicializa lista vacía para entrenadores disponibles
        entrenadores_disponibles = []
        # Itera sobre todos los entrenadores
        for entrenador in self.entrenadores:
            # Obtiene turnos del entrenador actual
            turnos = self.obtener_turnos_entrenador(entrenador["rut"])
            # Itera sobre turnos del entrenador
            for turno in turnos:
                # Verifica si el turno coincide con el día solicitado
                if turno["dia_semana"] == dia_semana.lower():
                    # Convierte hora solicitada a objeto datetime
                    hora_dt = datetime.strptime(hora, "%H:%M")
                    # Convierte hora de inicio del turno a objeto datetime
                    hora_inicio = datetime.strptime(turno["hora_inicio"], "%H:%M")
                    # Convierte hora de fin del turno a objeto datetime
                    hora_fin = datetime.strptime(turno["hora_fin"], "%H:%M")
                    # Verifica si la hora solicitada está dentro del turno
                    if hora_inicio <= hora_dt <= hora_fin:
                        # Agrega entrenador a la lista de disponibles
                        entrenadores_disponibles.append({
                            "nombre": entrenador["nombre"],  # Nombre del entrenador
                            "rut": entrenador["rut"],  # RUT del entrenador
                            "especialidades": entrenador.get("especialidades", []),  # Especialidades del entrenador
                            "turno": f"{turno['hora_inicio']} - {turno['hora_fin']}"  # Horario del turno
                        })
                        # Termina bucle interno al encontrar turno válido
                        break
        # Retorna lista de entrenadores disponibles
        return entrenadores_disponibles
    
    # Método para eliminar turno de entrenador
    def eliminar_turno_entrenador(self, rut_entrenador, dia_semana):
        # Itera sobre turnos con índice
        for i, turno in enumerate(self.turno_entrenadores):
            # Busca turno por RUT de entrenador y día de semana
            if turno["rut_entrenador"] == rut_entrenador and turno["dia_semana"] == dia_semana.lower():
                # Elimina turno de la lista
                self.turno_entrenadores.pop(i)
                # Intenta guardar los datos
                exito, mensaje = self.guardar_datos()
                
                # Verifica si el guardado fue exitoso
                if exito:
                    # Retorna éxito y mensaje de confirmación
                    return True, f"Turno del {dia_semana} eliminado"
                # Retorna fallo y mensaje de error
                return False, mensaje
        
        # Retorna fallo si no encuentra el turno
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
