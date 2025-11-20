import json
import os
import re
from datetime import datetime,timedelta
from validaciones import Validaciones
from suscripcion import Suscripcion
from historial_peso import HistorialPeso
from cliente import Cliente

def crear_archivo():
    archivos = {
        "clientes.json": [],
        "ejercicios.json": [],
        "entrenadores.json":[],
        "suscripciones.json":[],
        "turnos_entrenadores.json":[],
        "horas_gimnacion.json":{
            "dias_semanas":{
                "lunes":{"abre":"07:00","cierra":"22:00","activo":True},
                "martes":{"abre":"07:00","cierra":"22:00","activo":True},
                "miercoles":{"abre":"07:00","cierra":"22:00","activo":True},
                "jueves":{"abre":"07:00","cierra":"22:00","activo":True},
                "viernes":{"abre":"07:00","cierra":"22:00","activo":True},
                "sabado":{"abre":"09:00","cierra":"17:00","activado":True},
                "domingo":{"abre":"12:00","cierra":"17:00","activado":True}

            }
        }
    }
    for archivo, contenido_inicial in archivos.items():
        if not os.path.exists(archivo):
            with open(archivo,"w", encoding="utf-8") as f:
                json.dump(contenido_inicial, f, indent=4,ensure_ascii= False) 


class Gimnacio:
    def __init__(self):
        self.clientes = []
        self.entrenadores = []
        self.ejercicios = []
        self.suscripciones = []
        self.historial_peso =[]
        self.turno_entrenadores = []
        self.horario_gimnacio = []
        crear_archivo()
        self.cargar_datos()
    def cargar_datos(self):
        try:
            with open("clientes.json","r",encoding="uft-8") as f:
                self.clientes = json.load(f)
            with open("entrenadores.json","r",encoding="uft-8") as f:
                self.entrenadores = json.load(f)
            with open("ejercicios.json","r",encoding="utf-8") as f:
                self.ejercicios = json.load(f)
            with open("suscripciones.json","r",encoding="utf-8") as f:
                self.suscripciones = json.load(f)
            with open("historial_peso.json","r",encoding="utf-8") as f:
                self.historial_peso = json.load(f)
            with open("turnos_entrenadores.json","r",encoding="utf-8") as f:
                self.turno_entrenadores = json.load(f)
            with open("horario_gimnacio.json","r",encoding="utf-8") as f:
                self.horario_gimnacio = json.load(f)
        except Exception as e:
            print(f"Error al cargar los datos {e}")
    def guardar_datos(self):
        #se guardan los datos importantes dentro de un json
        try:
            with open("clientes.json","w",encoding="utf-8") as f:
                json.dump(self.clientes, indent=4,ensure_ascii=False)
            with open("entrenadores.json","w",encoding="utf-8") as f:
                json.dump(self.entrenadores, indent=4,ensure_ascii=False)
            with open("ejercicios.json","w",encoding="utf-8") as f:
                json.dump(self.ejercicios, indent=4,ensure_ascii=False)
            with open("suscripciones.json","w",encoding="utf-8") as f:
                json.dump(self.suscripciones, indent=4,ensure_ascii=False)
            with open("historial_peso.json","w",encoding="utf-8") as f:
                json.dump(self.historial_peso, indent=4,ensure_ascii=False)
            with open("turno_entrenadores.json","w",encoding="utf-8") as f:
                json.dump(self.turno_entrenadores, indent=4,ensure_ascii=False)
            with open("turno_gimnacio.json","w",encoding="utf-8") as f:
                json.dump(self.turno_entrenadores, indent=4,ensure_ascii=False)
            return True, "Datos guardados correctamente"
        except Exception as e:
            return False, f"Error al guardar los datos {e}"
    #Gestion de clientes
    def agregar_cliente(self,cliente):
        for c in self.clientes:
            if c["rut"] == cliente.rut:
                return False,"Ya existe un cliente con ese rut"
            self.clientes.append(cliente.a_diccionario())
            exito, mensaje = self.guardar_datos()
            if exito:
                return True, f"Cliente {cliente.nombre} agregado excitosamente"
            return False, mensaje
    def modificar_cliente(self,rut,nuevo_cliente):
        #se modifica un cliente existente
        for i, c in enumerate(self.clientes):
            if c["rut"] == rut:
                self.clientes[i] = nuevo_cliente.a_diccionario()
                exito, mensaje = self.guardar_datos()
                if exito:
                    return True,"Cliente modificado exitosamente"
                return False,mensaje
            return False,"Cliente no encontrado"
    def eliminar_cliente(self,rut):
        #Esta funcion elimina un cliente del gimnacio
        for i, c in enumerate(self.clientes): #buscamos con enumerate a los clientes desde el primero hasta el ultimo
                if c["rut"] == rut:
                    nombre = c["nombre"]
                    self.clientes.pop(i)
                    exito, mensaje = self.guardar_datos()
                    if exito:
                        return True,f"Cliente {nombre} eliminado exitosamente"
                    return False,mensaje
                return False, "Cliente no encontrado"
    def buscar_cliente_por_rut(self,rut):
        #Aqui vamos a buscar un cliente a traves del rut, recorriendolo con un for la lista completa
        for c in self.clientes:
            if c["rut"] == rut:
                return True,c
        return False,"Cliente no encontrado"
    #Reportes y consultas 
    def listar_clientes_fecha(self,fecha):
        # Se listara todos los clientes que asistieron dentro de una fecha especifica
        clientes_encontrados = []
        for ejercicio in self.ejercicios:
            if ejercicio["fecha"] == fecha:
                exito, cliente = self.buscar_cliente_por_rut(ejercicio["rut_cliente"])
                if exito and cliente not in clientes_encontrados:
                    clientes_encontrados.append(cliente)
        return clientes_encontrados
    def listar_clientes_imc_mayor30(self,fecha):
        #Se van a listar clientes con imc >30 que asistieron en una determinada fecha
        clientes_fecha = self.listar_clientes_fecha(fecha)
        clientes_filtrados = [c for c in clientes_fecha if c["imc"] >30]
        return clientes_filtrados
    def obtener_clientes_por_entrenador (self,nombre_entrenador):
        #Se van a obtener los clientes  y fechas de un entrenador especifico
        resultado = {}
        for ejercicio in self.ejercicios:
            if ejercicio["nombre_entrenador"].lower() == nombre_entrenador.lower():
                rut_cliente = ejercicio["rut_cliente"]
                fecha = ejercicio["fecha"]
                exito,cliente = self.buscar_cliente_por_rut(rut_cliente)
                if exito:
                    nombre_cliente = cliente["nombre"]
                    if nombre_cliente not in resultado:
                        resultado["nombre_cliente"] ={
                            "rut":rut_cliente,
                            "fechas":[],
                            "total_sesiones":0
                        }    
                    if fecha not in resultado["nombre_cliente"]["fechas"]:
                        resultado["nombre_cliente"]["fechas"].append(fecha)
                        resultado["nombre_cliente"]["total_sesiones"] +=1
        return resultado
    def obtener_ejercicios_por_entrenador(self, nombre_entrenador):
        #Obtiene todos los ejercicios registrados por un entrenador
        ejercicios_entrenador = [
            ej for ej in self.ejercicios 
            if ej["nombre_entrenador"].lower() == nombre_entrenador.lower()
        ]
        return ejercicios_entrenador
    
    def contar_clientes_activos_entrenador(self, nombre_entrenador):
        #Cuenta cuántos clientes diferentes ha atendido un entrenador
        clientes = self.obtener_clientes_por_entrenador(nombre_entrenador)
        return len(clientes)
#gestion de suscripciones
    def crear_suscripcion(self,suscripcion):
        exito, cliente = self.buscar_cliente_por_rut(suscripcion.rut_cliente)
        if not exito:
            return False, "El cliente no existe en el sistema"
        #Desactivar suscripciones anteriores de un mismo cliente
        for sus in self.suscripciones:
            if sus["rut_cliente"] == suscripcion.rut_cliente and sus.get("activa",True):
                sus["activa"] = False
        self.suscripciones.append(suscripcion.a_diccionario())
        exito,mensaje = self.guardar_datos()
        if exito:
            return True,f"Suscripcion {suscripcion.tipo_suscripcion} creada hasta {suscripcion.fecha_fin}"
        return False, mensaje
    def buscar_suscripcion_activa(self,rut_cliente):
        #Se aplica el read buscando una suscripcion activa de un cliente
        for sus in self.suscripciones:
            if sus["rut_cliente"] ==rut_cliente:
                fecha_fin = datetime.strftime(sus["fecha_fin"], "%Y-%m-%d")
                if datetime.now() <=fecha_fin:
                    return True,sus
        return False, "No hay suscripcion activa para este cliente"
    def renovar_suscripcion(self,rut_cliente,tipo_suscripcion,monto):
        #Update, se renueva una suscripcion de un cliente
        fecha_inicio = datetime.now().strftime("%Y-%m-%d")
        nueva_suscripcion = Suscripcion(rut_cliente,tipo_suscripcion,fecha_inicio,monto)
        return self.crear_suscripcion(nueva_suscripcion)
    def listar_suscripciones_por_vencer(self,dias=7):
        #read, listando suscripciones que vencen en X dias
        suscripciones_por_vencer = []
        fecha_limite = datetime.now() + timedelta(days = dias)
        for sus in self.suscripciones:
            if sus.get("activa",True):
                fecha_fin = datetime.strptime(sus["fecha_fin"], "%Y-%m-%d")
                if datetime.now() < fecha_fin <= fecha_limite:
                    exito, cliente = self.buscar_cliente_por_rut(sus["rut_cliente"])
                    if exito:
                        sus_completa = sus.copy()
                        sus_completa["nombre_cliente"] = cliente["nombre"]
                        suscripciones_por_vencer.append(sus_completa)
        return suscripciones_por_vencer
    