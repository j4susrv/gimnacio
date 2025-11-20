from validaciones import Validaciones
class Ejercicio:
    def __init__(self,nombre_ejercicio,fecha,tipo_ejercicio,nombre_entrenador,duracion_minutos,rut_cliente):
        self.nombre_ejercicio = nombre_ejercicio
        self.fecha = fecha
        self.tipo_ejercicio = tipo_ejercicio
        self.nombre_entrenador = nombre_entrenador
        self.duracion_minutos = duracion_minutos
        self.rut_cliente = rut_cliente

    def a_diccionario(self):
        return {
            "nombre_ejercicio" : self.nombre_ejercicio,
            "fecha":self.fecha,
            "tipo_ejercicio": self.tipo_ejercicio,
            "nombre_entrenador":self.nombre_entrenador,
            "duracion_minutos": self.duracion_minutos,
            "rut_cliente":self.rut_cliente
        }
    def validar_datos(nombre_ejercicio,fecha,tipo_ejercicio,nombre_entrenador,duracion_minutos,rut_cliente):
        errores=[]
        advertencias=[]
        valido,mensaje = Validaciones.validar_nombre(nombre_ejercicio)
        if not valido:
            errores.append(f"Nombre ejercicio: {mensaje}")
        valido,mensaje = Validaciones.validar_fecha_nacimiento(fecha)
        if not valido:
            errores.append(f"Fecha: {mensaje}")
        valido,mensaje = Validaciones.validar_tipo_ejercicio(tipo_ejercicio)
        if not valido:
            errores.append(mensaje)
        valido, mensaje = Validaciones.validar_nombre(nombre_entrenador)
        if not valido:
            errores.append(f"Nombre del entrenador: {mensaje}")
        valido,mensaje = Validaciones.validar_duracion(duracion_minutos)
        if not valido:
            errores.append(mensaje)
        elif "Advertencia" in mensaje:
            advertencias.append(mensaje)
        return errores,advertencias