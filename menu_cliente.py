import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from suscripcion import Suscripcion
from gimnasio import Gimnasio
from ejercicios import Ejercicio
from cliente import Cliente
from validaciones import Validaciones
from entrenador import Entrenador,TurnoEntrenador
import subprocess
import sys
import json
import os

#AGREGAR QUE EL USUARIO PUEDA VER LA DISPONIBILIDAD DE EL ENTRENADOR
#Se define el menu de cliente
class MenuCliente:
    def __init__(self, parent_frame, cliente_data):
        self.frame = parent_frame
        self.cliente_data = cliente_data
        self.gimnasio = Gimnasio()
        self.ventanas_abiertas = {}  # Diccionario para rastrear ventanas abiertas
        self.botones = {}  # Diccionario para almacenar referencias a los botones
        self.crear_menu()
    
    def crear_menu(self):
        # Limpiar widgets anteriores
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Configurar el frame principal
        self.frame.configure(bg="white")

        # BARRA DE ESTADO (arriba de todo)
        esta_abierto, mensaje = self.gimnasio.obtener_estado_actual()
        color = "#27ae60" if esta_abierto else "#e74c3c"
        
        self.label_estado = tk.Label(
            self.frame,
            text=mensaje,
            font=("Helvetica", 11),
            bg=color,
            fg="white",
            pady=8
        )
        self.label_estado.pack(fill="x")
        
        # Actualizar cada minuto
        self.actualizar_estado_gimnasio()
        
        # Título de bienvenida
        nombre_cliente = self.cliente_data.get('nombre', 'Cliente')
        tk.Label(
            self.frame, 
            text=f"Bienvenido, {nombre_cliente}", 
            font=("Helvetica", 18, "bold"), 
            bg="white",
            fg="#333"
        ).pack(pady=30) #se define estructura visual
        
        # Mostrar información del entrenador asignado si existe
        entrenador_info = self.obtener_info_entrenador_completa()
        if entrenador_info:
            info_frame = tk.Frame(self.frame, bg="#e8f4fd", relief="solid", bd=1)
            info_frame.pack(fill="x", padx=40, pady=10)
            
            tk.Label(
                info_frame,
                text=f"Entrenador: {entrenador_info['nombre']}",
                font=("Helvetica", 12, "bold"),
                bg="#e8f4fd",
                fg="#2c3e50"
            ).pack(pady=(8, 2))
            
            tk.Label(
                info_frame,
                text=f"Especialidades: {entrenador_info['especialidades']}",
                font=("Helvetica", 10),
                bg="#e8f4fd",
                fg="#34495e"
            ).pack(pady=2)
            
            # Estado de disponibilidad
            disponible = entrenador_info['disponible']
            estado_color = "#27ae60" if disponible else "#e74c3c"
            estado_texto = "Disponible ahora" if disponible else "No disponible"
            
            tk.Label(
                info_frame,
                text=estado_texto,
                font=("Helvetica", 10, "bold"),
                bg="#e8f4fd",
                fg=estado_color
            ).pack(pady=2)
            
            # Botón para ver horarios
            tk.Button(
                info_frame,
                text="📅 Ver Horarios",
                command=self.ver_horarios_entrenador,
                bg="#3498db",
                fg="white",
                font=("Helvetica", 9, "bold"),
                relief="flat",
                cursor="hand2"
            ).pack(pady=(5, 8))
        
        # Frame para los botones
        frame_btn = tk.Frame(self.frame, bg="white")
        frame_btn.pack(expand=True, padx=40, pady=20)
        
        # Definir botones con sus comandos y colores
        botones_config = [
            ("Ver Suscripción", self.ver_suscripcion, "#4a90e2", "ver_suscripcion"),
            ("Adquirir Suscripción", self.adquirir_suscripcion, "#50c878", "adquirir_suscripcion"),
            ("Ver Rutinas", self.ver_rutinas, "#9b59b6", "ver_rutinas"),
            ("Mis Datos", self.ver_datos, "#3498db", "ver_datos"),
            ("Cerrar Sesión", self.cerrar_sesion, "#e74c3c", None)
        ]
        
        # Crear botones
        for texto, comando, color, key in botones_config:
            btn = tk.Button(
                frame_btn, 
                text=texto, 
                command=comando, 
                font=("Helvetica", 11, "bold"),
                bg=color, 
                fg="white", 
                height=2, 
                relief="flat",
                cursor="hand2"
            )
            btn.pack(fill="x", pady=8)
            
            # Guardar referencia del botón si tiene key
            if key:
                self.botones[key] = btn
    def actualizar_estado_gimnasio(self):
        """Actualiza el estado cada minuto"""
        try:
            esta_abierto, mensaje = self.gimnasio.obtener_estado_actual()
            color = "#27ae60" if esta_abierto else "#e74c3c"
            self.label_estado.config(text=mensaje, bg=color)
        except:
            pass
        
        self.frame.after(60000, self.actualizar_estado_gimnasio)
    def obtener_info_entrenador_completa(self):
        """Obtiene información completa del entrenador incluyendo disponibilidad"""
        rut_cliente = self.cliente_data.get('rut')
        if not rut_cliente:
            print("No se encontró RUT del cliente")
            return None
        
        
            # Leer clientes para obtener el RUT del entrenador asignado
        with open("clientes.json", "r", encoding="utf-8") as f:
            clientes = json.load(f)
            
        rut_entrenador = None
        for cliente in clientes:
            if cliente.get('rut') == rut_cliente:
                rut_entrenador = cliente.get('entrenador_asignado')
                print(f"RUT entrenador asignado: {rut_entrenador}")
                break
            
        if not rut_entrenador:
            print("No hay entrenador asignado")
            return None
            
            # Leer entrenadores para obtener la información completa
        with open("entrenadores.json", "r", encoding="utf-8") as f:
            entrenadores = json.load(f)
            
        for entrenador in entrenadores:
            if entrenador.get('rut') == rut_entrenador:
                nombre = entrenador.get('nombre', 'Entrenador')
                especialidades = ', '.join(entrenador.get('especialidades', []))
                turnos = entrenador.get('turnos', [])
                disponible = TurnoEntrenador.esta_disponible(rut_entrenador, entrenadores)
                
                return {
                    'rut': rut_entrenador,
                    'nombre': nombre,
                    'especialidades': especialidades if especialidades else 'Sin especialidades',
                    'disponible': disponible,
                    'turnos': turnos
                }
        return None
    
    def obtener_info_entrenador_asignado(self):
        rut_cliente = self.cliente_data.get('rut')
        if not rut_cliente:
            return None
        
        archivo_clientes = "clientes.json"
        if not os.path.exists(archivo_clientes):
            return None
        
        try:
            with open(archivo_clientes, "r", encoding="utf-8") as f:
                clientes = json.load(f)
            
            for cliente in clientes:
                if cliente.get('rut') == rut_cliente:
                    rut_entrenador = cliente.get('entrenador_asignado')
                    if rut_entrenador:
                        return self.obtener_nombre_entrenador(rut_entrenador)
                    break
        except Exception as e:
            print(f"Error al buscar entrenador asignado: {e}")
        
        return None
    
    def obtener_nombre_entrenador(self, rut_entrenador):
        """Obtiene el nombre y estado del entrenador para mostrar en 'Mis Datos'"""
        archivo_entrenadores = "entrenadores.json"
        if not os.path.exists(archivo_entrenadores):
            return "Entrenador (archivo no encontrado)"
        
        try:          
            with open(archivo_entrenadores, "r", encoding="utf-8") as f:
                entrenadores = json.load(f)
            
            for entrenador in entrenadores:
                if entrenador.get('rut') == rut_entrenador:
                    nombre = entrenador.get('nombre', 'Entrenador')
                    especialidades_lista = entrenador.get('especialidades', [])
                    especialidades = ', '.join(especialidades_lista) if especialidades_lista else 'Sin especialidades'
                    
                    # Verificar disponibilidad
                    disponible = TurnoEntrenador.esta_disponible(rut_entrenador, entrenadores)
                    estado = "Disponible" if disponible else "No disponible"
                    
                    return f"{nombre} - {especialidades} ({estado})"
        except Exception as e:
            print(f"Error en obtener_nombre_entrenador: {e}")
        
        return "Entrenador (error al cargar información)"
    
    def bloquear_botones(self, excepto=None):
        for nombre, boton in self.botones.items():
            if nombre != excepto:
                boton.config(state="disabled")
    
    def desbloquear_botones(self):
        for boton in self.botones.values():
            boton.config(state="normal")
    
    def verificar_ventana_abierta(self, nombre_ventana):
        if nombre_ventana in self.ventanas_abiertas:
            if self.ventanas_abiertas[nombre_ventana].winfo_exists():
                self.ventanas_abiertas[nombre_ventana].lift()
                return True
        return False
    
    def registrar_ventana(self, nombre_ventana, ventana, boton_key=None):
        self.ventanas_abiertas[nombre_ventana] = ventana
        if boton_key:
            self.bloquear_botones(boton_key)
        
        # Define el comportamiento cuando se cierra la ventana con la X
        def al_cerrar():
            self.desbloquear_botones()
            if nombre_ventana in self.ventanas_abiertas:
                del self.ventanas_abiertas[nombre_ventana]
            ventana.destroy()
        
        ventana.protocol("WM_DELETE_WINDOW", al_cerrar) 
        
    def ver_horarios_entrenador(self):
        """Muestra los horarios del entrenador asignado"""
        if self.verificar_ventana_abierta('horarios_entrenador'):
            return
        
        info_entrenador = self.obtener_info_entrenador_completa()
        if not info_entrenador:
            messagebox.showinfo("Información", "No tienes entrenador asignado o no se pudo cargar su información")
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Horarios del Entrenador")
        v.geometry("500x500")
        v.configure(bg="white")
        self.registrar_ventana('horarios_entrenador', v)
        
        # Título
        tk.Label(
            v, 
            text=f"Horarios de {info_entrenador['nombre']}", 
            font=("Helvetica", 14, "bold"), 
            bg="white"
        ).pack(pady=20)
        
        # Frame principal con scroll
        frame_principal = tk.Frame(v, bg="white")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Obtener turnos
        turnos = info_entrenador.get('turnos', [])
        
        if not turnos:
            tk.Label(
                scrollable_frame, 
                text="Sin horarios registrados para este entrenador", 
                font=("Helvetica", 11), 
                bg="white", 
                fg="#e74c3c"
            ).pack(pady=30)
        else:
            # Organizar turnos por día
            dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
            turnos_por_dia = {dia: [] for dia in dias_semana}
            
            for turno in turnos:
                dia = turno.get('dia', '').lower()
                if dia in turnos_por_dia:
                    turnos_por_dia[dia].append(turno)
            
            # Mostrar turnos organizados por día
            for dia in dias_semana:
                if turnos_por_dia[dia]:
                    # Frame para cada día
                    frame_dia = tk.Frame(
                        scrollable_frame, 
                        bg="#f8f9fa", 
                        relief="solid", 
                        bd=1
                    )
                    frame_dia.pack(fill="x", pady=5, padx=10)
                    
                    # Nombre del día
                    tk.Label(
                        frame_dia, 
                        text=dia.capitalize(), 
                        font=("Helvetica", 11, "bold"), 
                        bg="#f8f9fa", 
                        fg="#2c3e50"
                    ).pack(anchor="w", padx=10, pady=(8, 2))
                    
                    # Turnos del día
                    for turno in turnos_por_dia[dia]:
                        hora_inicio = turno.get('hora_inicio', 'N/A')
                        hora_fin = turno.get('hora_fin', 'N/A')
                        horas = turno.get('horas_trabajo', 0)
                        
                        # Formatear horas (quitar segundos si existen)
                        if len(hora_inicio) > 5:
                            hora_inicio = hora_inicio[:5]
                        if len(hora_fin) > 5:
                            hora_fin = hora_fin[:5]
                        
                        tk.Label(
                            frame_dia, 
                            text=f"   {hora_inicio} - {hora_fin} ({horas}h)", 
                            font=("Helvetica", 10), 
                            bg="#f8f9fa", 
                            fg="#34495e"
                        ).pack(anchor="w", padx=10, pady=2)
                    
                    # Espacio al final del frame
                    tk.Label(frame_dia, text="", bg="#f8f9fa").pack(pady=2)
            
            # Calcular total de horas semanales
            total_horas = sum(t.get('horas_trabajo', 0) for t in turnos)
            
            tk.Label(
                scrollable_frame,
                text=f"Total: {len(turnos)} turnos/semana ({total_horas:.1f} horas)",
                font=("Helvetica", 10, "bold"),
                bg="white",
                fg="#27ae60"
            ).pack(pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def ver_suscripcion(self):
        if self.verificar_ventana_abierta('ver_suscripcion'): 
            return
        
        self.gimnasio = Gimnasio()
        existe, sus = self.gimnasio.buscar_suscripcion_activa(self.cliente_data.get('rut'))
        
        v = tk.Toplevel(self.frame)
        v.title("Mi Suscripción")
        v.geometry("450x400")
        v.configure(bg="white")
        self.registrar_ventana('ver_suscripcion', v, 'ver_suscripcion')
        
        tk.Label(
            v, 
            text="Mi Suscripción", 
            font=("Helvetica", 16, "bold"), 
            bg="white"
        ).pack(pady=20)
        
        frame_info = tk.Frame(v, bg="white")
        frame_info.pack(expand=True, fill="both", padx=30, pady=20)
        
        if existe:
            # Parsear fecha de inicio (puede estar en formato DD-MM-YYYY o YYYY-MM-DD)
            try:
                fecha_inicio_str = sus.get('fecha_inicio', '')
                # Intentar formato chileno primero
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%d-%m-%Y')
                except ValueError:
                    # Si falla, intentar formato ISO
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
                
                fecha_inicio_display = fecha_inicio.strftime('%d-%m-%Y')
            except:
                fecha_inicio_display = sus.get('fecha_inicio', 'N/A')
            
            # Parsear fecha de vencimiento si existe, si no calcularla
            try:
                fecha_fin_str = sus.get('fecha_fin', '')
                if fecha_fin_str:
                    try:
                        fecha_vencimiento = datetime.strptime(fecha_fin_str, '%d-%m-%Y')
                    except ValueError:
                        fecha_vencimiento = datetime.strptime(fecha_fin_str, '%Y-%m-%d')
                else:
                    # Calcular fecha de vencimiento basada en días restantes
                    dias = sus.get('dias_restantes', 0)
                    fecha_vencimiento = fecha_inicio + timedelta(days=dias)
                
                fecha_vencimiento_str = fecha_vencimiento.strftime('%d-%m-%Y')
            except:
                fecha_vencimiento_str = "No disponible"
            
            info_items = [
                ("Tipo de Suscripción:", sus.get('tipo_suscripcion', 'N/A').upper()),
                ("Fecha de Inicio:", fecha_inicio_display),
                ("Fecha de Vencimiento:", fecha_vencimiento_str),
                ("Días Restantes:", f"{sus.get('dias_restantes', 0)} días"),
                ("Estado:", "ACTIVA" if sus.get('activa') else "VENCIDA")
            ]
            
            for label, valor in info_items:
                frame_fila = tk.Frame(frame_info, bg="white")
                frame_fila.pack(fill="x", pady=8)
                
                tk.Label(
                    frame_fila, 
                    text=label, 
                    font=("Helvetica", 11, "bold"), 
                    bg="white",
                    width=20,
                    anchor="e"
                ).pack(side="left", padx=5)
                
                tk.Label(
                    frame_fila, 
                    text=valor, 
                    font=("Helvetica", 11), 
                    bg="white",
                    fg="#2c3e50" if sus.get('activa') else "#e74c3c"
                ).pack(side="left", padx=10)
            
            # Bloquear adquirir mientras haya suscripción
            if 'adquirir_suscripcion' in self.botones:
                self.botones['adquirir_suscripcion'].config(state="disabled")
            
            # Botón para actualizar ventana
            def actualizar():
                if 'ver_suscripcion' in self.ventanas_abiertas:
                    ventana_actual = self.ventanas_abiertas['ver_suscripcion']
                    if ventana_actual.winfo_exists():
                        ventana_actual.destroy()
                    del self.ventanas_abiertas['ver_suscripcion']
                self.ver_suscripcion()
            
            tk.Button(
                v, 
                text="Actualizar", 
                command=actualizar, 
                bg="#3498db", 
                fg="white", 
                font=("Helvetica", 10, "bold"),
                relief="flat",
                cursor="hand2"
            ).pack(pady=5)
            
            # Botón para terminar suscripción
            def terminar_suscripcion():
                confirm = messagebox.askyesno("Confirmar", "¿Deseas terminar tu suscripción actual?")
                if confirm:
                    exito, msg = self.gimnasio.eliminar_suscripcion(sus.get('id'))
                    if exito:
                        messagebox.showinfo("Éxito", "Suscripción eliminada correctamente")
                        
                        # CRÍTICO: Recargar datos del gimnasio
                        self.gimnasio = Gimnasio()
                        
                        # Habilitar botón de adquirir
                        if 'adquirir_suscripcion' in self.botones:
                            self.botones['adquirir_suscripcion'].config(state="normal")
                        
                        # Cerrar y reabrir la ventana
                        if 'ver_suscripcion' in self.ventanas_abiertas:
                            ventana_actual = self.ventanas_abiertas['ver_suscripcion']
                            if ventana_actual.winfo_exists():
                                ventana_actual.destroy()
                            del self.ventanas_abiertas['ver_suscripcion']
                        
                        # Reabrir ventana con datos actualizados
                        self.ver_suscripcion()
                    else:
                        messagebox.showerror("Error", msg)
            
            tk.Button(
                v, 
                text="Terminar Suscripción", 
                command=terminar_suscripcion,
                bg="#e74c3c", 
                fg="white", 
                font=("Helvetica", 10, "bold"),
                relief="flat",
                cursor="hand2"
            ).pack(pady=10)
        
        else:
            tk.Label(
                frame_info, 
                text="No tienes suscripcion activa", 
                font=("Helvetica", 12, "bold"), 
                bg="white",
                fg="#e74c3c"
            ).pack(pady=20)
            
            tk.Label(
                frame_info, 
                text="Adquiere una suscripción para acceder a todos los beneficios del gimnasio", 
                font=("Helvetica", 10), 
                bg="white",
                fg="#7f8c8d",
                wraplength=350
            ).pack(pady=10)
            
            # Asegurar que botón de adquirir esté habilitado
            if 'adquirir_suscripcion' in self.botones:
                self.botones['adquirir_suscripcion'].config(state="normal")
    
    def adquirir_suscripcion(self):
        # Verificar si ya hay suscripción activa
        existe, _ = self.gimnasio.buscar_suscripcion_activa(self.cliente_data.get('rut'))
        if existe:
            messagebox.showwarning("Atención", "Ya tienes una suscripción activa. Finalízala para adquirir otra.")
            return
        
        if self.verificar_ventana_abierta('adquirir_suscripcion'):
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Adquirir Suscripción")
        v.geometry("400x350")
        v.configure(bg="white")
        self.registrar_ventana('adquirir_suscripcion', v, 'adquirir_suscripcion')
        
        tk.Label(
            v, 
            text="Selecciona tu Plan", 
            font=("Helvetica", 14, "bold"), 
            bg="white"
        ).pack(pady=20)
        
        tipo = tk.StringVar(value="mensual")
        frame_opciones = tk.Frame(v, bg="white")
        frame_opciones.pack(pady=20)
        
        planes = [
            ("Mensual - 30 días", "mensual"),
            ("Trimestral - 90 días", "trimestral"),
            ("Semestral - 180 días", "semestral"),
            ("Anual - 365 días", "anual")
        ]
        
        for texto, valor in planes:
            tk.Radiobutton(
                frame_opciones, 
                text=texto, 
                variable=tipo, 
                value=valor, 
                font=("Helvetica", 11),
                bg="white"
            ).pack(anchor="w", padx=40, pady=5)
        
        def confirmar():
            # CAMBIO IMPORTANTE: usar formato chileno DD-MM-YYYY
            fecha_hoy_chilena = datetime.now().strftime("%d-%m-%Y")
            
            nueva_sus = Suscripcion(
                self.cliente_data.get('rut'), 
                tipo.get(), 
                fecha_hoy_chilena  # Ahora en formato chileno
            )
            exito, msg = self.gimnasio.crear_suscripcion(nueva_sus)
            messagebox.showinfo("Resultado", msg)
            if exito:
                if 'adquirir_suscripcion' in self.ventanas_abiertas:
                    del self.ventanas_abiertas['adquirir_suscripcion']
                self.desbloquear_botones()
                v.destroy()
                
                # Recargar datos de gimnasio
                self.gimnasio = Gimnasio()
                
                # Cerrar ventana ver_suscripcion si está abierta
                if 'ver_suscripcion' in self.ventanas_abiertas:
                    ventana_suscripcion = self.ventanas_abiertas['ver_suscripcion']
                    if ventana_suscripcion.winfo_exists():
                        ventana_suscripcion.destroy()
                    del self.ventanas_abiertas['ver_suscripcion']
        
        tk.Button(
            v, 
            text="Confirmar Compra", 
            command=confirmar, 
            bg="#50c878", 
            fg="white", 
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(pady=20)
    
    def ver_rutinas(self):
        if self.verificar_ventana_abierta('ver_rutinas'):
            return
        
        existe, rutinas = self.gimnasio.buscar_ejercicios_por_cliente(self.cliente_data.get('rut'))
        
        if not existe:
            messagebox.showinfo("Rutinas", "No tienes rutinas registradas")
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Mis Rutinas")
        v.geometry("650x450")
        v.configure(bg="white")
        self.registrar_ventana('ver_rutinas', v, 'ver_rutinas')
        
        tk.Label(
            v, 
            text=f"Mis Rutinas Completadas ({len(rutinas)})", 
            font=("Helvetica", 14, "bold"), 
            bg="white"
        ).pack(pady=15)
        
        f = tk.Frame(v)
        f.pack(fill="both", expand=True, padx=15, pady=10)
        
        texto = tk.Text(f, wrap="word", font=("Courier", 10), bg="#f9f9f9")
        scroll = tk.Scrollbar(f, command=texto.yview)
        texto.config(yscrollcommand=scroll.set)
        
        for i, r in enumerate(rutinas, 1):
            texto.insert(
                "end", 
                f"{i}. {r.get('nombre_ejercicio')} - {r.get('tipo_ejercicio').upper()}\n"
            )
            texto.insert(
                "end", 
                f"   Entrenador: {r.get('nombre_entrenador')} | "
                f"Duración: {r.get('duracion_minutos')} min | "
                f"Fecha: {r.get('fecha')}\n\n"
            )
        
        texto.config(state="disabled")
        texto.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
    
    def ver_datos(self):
        # Recargar datos para obtener cambios recientes
        self.gimnasio.cargar_datos()
        
        if self.verificar_ventana_abierta('ver_datos'):
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Mis Datos")
        v.geometry("550x700")
        v.configure(bg="white")
        self.registrar_ventana('ver_datos', v, 'ver_datos')
        
        # Crear un canvas con scrollbar para contenido largo
        canvas = tk.Canvas(v, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(v, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            scrollable_frame, 
            text="Información Personal", 
            font=("Helvetica", 14, "bold"), 
            bg="white"
        ).pack(pady=20)
        
        f = tk.Frame(scrollable_frame, bg="white")
        f.pack(padx=40, pady=10)
        
        # Obtener entrenador asignado desde JSON
        entrenador_info = self.obtener_info_entrenador_asignado()
        entrenador = entrenador_info if entrenador_info else 'Sin asignar'
        
        datos = [
            ("Nombre:", self.cliente_data.get('nombre', 'N/A')),
            ("RUT:", self.cliente_data.get('rut', 'N/A')),
            ("Estatura:", f"{self.cliente_data.get('estatura', 'N/A')} cm"),
            ("Peso Actual:", f"{self.cliente_data.get('peso', 'N/A')} kg"),
            ("IMC:", str(self.cliente_data.get('imc', 'N/A'))),
            ("Categoría IMC:", self.cliente_data.get('categoria_imc', 'N/A')),
            ("Dirección:", self.cliente_data.get('direccion', 'N/A')),
            ("Estado Civil:", self.cliente_data.get('estado_civil', 'N/A')),
            ("Entrenador:", entrenador)
        ]
        
        for i, (label, valor) in enumerate(datos):
            tk.Label(
                f, 
                text=label, 
                font=("Helvetica", 10, "bold"), 
                bg="white"
            ).grid(row=i, column=0, sticky="e", pady=8, padx=5)
            
            tk.Label(
                f, 
                text=valor, 
                font=("Helvetica", 10), 
                bg="white"
            ).grid(row=i, column=1, sticky="w", pady=8, padx=15)
        
        # ==================== SECCIÓN DE SEGUIMIENTO DE PESO ====================
        peso_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
        peso_frame.pack(padx=30, pady=20, fill="x")
        
        tk.Label(
            peso_frame,
            text="Seguimiento de Peso",
            font=("Helvetica", 12, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        ).pack(pady=(15, 10))
        
        # Obtener datos de comparación de peso
        gimnasio_temp = Gimnasio()
        rut_cliente = self.cliente_data.get('rut')
        comparacion = gimnasio_temp.obtener_comparacion_peso(rut_cliente)
        
        if comparacion:
            # Frame para las métricas
            metricas_frame = tk.Frame(peso_frame, bg="white")
            metricas_frame.pack(padx=15, pady=10, fill="x")
            
            # Peso Inicial
            tk.Label(
                metricas_frame,
                text="Peso Inicial:",
                font=("Helvetica", 9, "bold"),
                bg="white"
            ).grid(row=0, column=0, sticky="e", pady=5, padx=5)
            
            tk.Label(
                metricas_frame,
                text=f"{comparacion['peso_inicial']} kg",
                font=("Helvetica", 9),
                bg="white"
            ).grid(row=0, column=1, sticky="w", pady=5, padx=5)
            
            # Peso Actual
            tk.Label(
                metricas_frame,
                text="Peso Actual:",
                font=("Helvetica", 9, "bold"),
                bg="white"
            ).grid(row=1, column=0, sticky="e", pady=5, padx=5)
            
            tk.Label(
                metricas_frame,
                text=f"{comparacion['peso_actual']} kg",
                font=("Helvetica", 9),
                bg="white"
            ).grid(row=1, column=1, sticky="w", pady=5, padx=5)
            
            # Diferencia vs Último
            color_diff_ultimo = "#e74c3c" if comparacion['diferencia_vs_ultimo'] > 0 else "#27ae60"
            signo_ultimo = "+" if comparacion['diferencia_vs_ultimo'] >= 0 else ""
            
            tk.Label(
                metricas_frame,
                text="Diferencia vs Último:",
                font=("Helvetica", 9, "bold"),
                bg="white"
            ).grid(row=2, column=0, sticky="e", pady=5, padx=5)
            
            tk.Label(
                metricas_frame,
                text=f"{signo_ultimo}{comparacion['diferencia_vs_ultimo']} kg",
                font=("Helvetica", 9, "bold"),
                bg="white",
                fg=color_diff_ultimo
            ).grid(row=2, column=1, sticky="w", pady=5, padx=5)
            
            # Diferencia vs Inicial
            color_diff_inicial = "#e74c3c" if comparacion['diferencia_vs_inicial'] > 0 else "#27ae60"
            signo_inicial = "+" if comparacion['diferencia_vs_inicial'] >= 0 else ""
            
            tk.Label(
                metricas_frame,
                text="Diferencia vs Inicial:",
                font=("Helvetica", 9, "bold"),
                bg="white"
            ).grid(row=3, column=0, sticky="e", pady=5, padx=5)
            
            tk.Label(
                metricas_frame,
                text=f"{signo_inicial}{comparacion['diferencia_vs_inicial']} kg",
                font=("Helvetica", 9, "bold"),
                bg="white",
                fg=color_diff_inicial
            ).grid(row=3, column=1, sticky="w", pady=5, padx=5)
            
            # Última actualización
            tk.Label(
                metricas_frame,
                text="Última Actualización:",
                font=("Helvetica", 9, "bold"),
                bg="white"
            ).grid(row=4, column=0, sticky="e", pady=5, padx=5)
            
            tk.Label(
                metricas_frame,
                text=comparacion['fecha_ultimo_registro'],
                font=("Helvetica", 9),
                bg="white"
            ).grid(row=4, column=1, sticky="w", pady=5, padx=5)
            
            # Total de registros
            tk.Label(
                metricas_frame,
                text="Total de Registros:",
                font=("Helvetica", 9, "bold"),
                bg="white"
            ).grid(row=5, column=0, sticky="e", pady=5, padx=5)
            
            tk.Label(
                metricas_frame,
                text=str(comparacion['total_registros']),
                font=("Helvetica", 9),
                bg="white"
            ).grid(row=5, column=1, sticky="w", pady=5, padx=5)
        
        # ===== Botones =====
        botones_frame = tk.Frame(scrollable_frame, bg="white")
        botones_frame.pack(pady=20)
        
        tk.Button(
            botones_frame, 
            text="Registrar Peso", 
            command=self.registrar_nuevo_peso, 
            bg="#3498db", 
            fg="white", 
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=20
        ).pack(pady=5)
        
        tk.Button(
            botones_frame, 
            text="Modificar Datos", 
            command=lambda: self.modificar_datos(v), 
            bg="#e67e22", 
            fg="white", 
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2",
            width=20
        ).pack(pady=5)
    
    def modificar_datos(self, v_padre):
        # Cerrar ventana de datos
        if 'ver_datos' in self.ventanas_abiertas:
            del self.ventanas_abiertas['ver_datos']
        v_padre.destroy()
        
        if self.verificar_ventana_abierta('modificar_datos'):
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Modificar Datos")
        v.geometry("450x450")
        v.configure(bg="white")
        self.registrar_ventana('modificar_datos', v, 'ver_datos')
        
        tk.Label(
            v, 
            text="Modificar Mis Datos", 
            font=("Helvetica", 14, "bold"), 
            bg="white"
        ).pack(pady=20)
        
        f = tk.Frame(v, bg="white")
        f.pack(padx=30)
        
        entry_peso = tk.Entry(f, width=25)
        entry_estatura = tk.Entry(f, width=25)
        entry_direccion = tk.Entry(f, width=25)
        combo_estado_civil = ttk.Combobox(
            f, 
            values=["soltero", "casado", "divorciado", "viudo", "conviviente"], 
            width=23, 
            state="readonly"
        )
        entry_contraseña = tk.Entry(f, width=25, show="*")
        
        campos = [
            ("Peso (kg):", entry_peso),
            ("Estatura (cm):", entry_estatura),
            ("Dirección:", entry_direccion),
            ("Estado Civil:", combo_estado_civil),
            ("Contraseña:", entry_contraseña)
        ]
        
        for i, (label, widget) in enumerate(campos):
            tk.Label(f, text=label, bg="white", font=("Helvetica", 10, "bold")).grid(
                row=i, column=0, sticky="e", pady=8
            )
            widget.grid(row=i, column=1, pady=8)
        
        # Valores actuales
        entry_peso.insert(0, self.cliente_data.get('peso', ''))
        entry_estatura.insert(0, self.cliente_data.get('estatura', ''))
        entry_direccion.insert(0, self.cliente_data.get('direccion', ''))
        combo_estado_civil.set(self.cliente_data.get('estado_civil', 'soltero'))
        
        def guardar():
            peso = entry_peso.get().strip()
            estatura = entry_estatura.get().strip()
            direccion = entry_direccion.get().strip()
            estado_civil = combo_estado_civil.get().strip()
            contraseña = entry_contraseña.get().strip()
            
            # Validación 1: Campos vacíos
            if not peso or not estatura or not direccion or not estado_civil or not contraseña:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            # Validación 2: Verificar contraseña actual
            if contraseña != self.cliente_data.get('contraseña'):
                messagebox.showerror("Error", "Contraseña incorrecta")
                return
            
            # Validación 3: Validar peso
            validaciones = Validaciones()
            es_valido, mensaje = validaciones.validar_peso(peso)
            if not es_valido:
                messagebox.showerror("Error", mensaje)
                return
            
            # Validación 4: Validar estatura
            es_valido, mensaje = validaciones.validar_estatura(estatura)
            if not es_valido:
                messagebox.showerror("Error", mensaje)
                return
            
            # Convertir a float después de validar
            try:
                peso_float = float(peso)
                estatura_float = float(estatura)
            except ValueError:
                messagebox.showerror("Error", "Peso y estatura deben ser números válidos")
                return
            
            # Validación 5: Validar IMC
            estatura_m = estatura_float / 100
            imc = round(peso_float / (estatura_m ** 2), 2)
            
            if imc < 13:
                messagebox.showerror("Error", f"IMC muy bajo ({imc}). El IMC no puede ser menor a 13. Verifique el peso y la estatura.")
                return
            
            # Validación 6: Validar dirección
            es_valido, mensaje = validaciones.validar_direccion(direccion)
            if not es_valido:
                messagebox.showerror("Error", mensaje)
                return
            
            # Validación 7: Validar estado civil
            if estado_civil.lower() not in ["soltero", "casado", "divorciado", "viudo", "conviviente"]:
                messagebox.showerror("Error", "Estado civil inválido")
                return
            
            # Si todas las validaciones pasan, crear el cliente modificado
            try:
                cliente_mod = Cliente(
                    nombre=self.cliente_data.get('nombre'), 
                    rut=self.cliente_data.get('rut'),
                    fecha_nacimiento=self.cliente_data.get('fecha_nacimiento'), 
                    estatura=estatura_float,
                    peso=peso_float,
                    estado_civil=estado_civil.lower(),
                    direccion=direccion,
                    contraseña=contraseña
                )
                
                exito, msg = self.gimnasio.modificar_cliente(
                    self.cliente_data.get('rut'), 
                    cliente_mod
                )
                
                if exito:
                    self.cliente_data = cliente_mod.a_diccionario()
                    messagebox.showinfo("Éxito", "Datos actualizados correctamente")
                    if 'modificar_datos' in self.ventanas_abiertas:
                        del self.ventanas_abiertas['modificar_datos']
                    self.desbloquear_botones()
                    v.destroy()
                    self.crear_menu()
                else:
                    messagebox.showerror("Error", msg)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
        
        tk.Button(
            v, 
            text="Guardar Cambios", 
            command=guardar, 
            bg="#50c878", 
            fg="white", 
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(pady=20)

    def registrar_nuevo_peso(self):
        """Modal para registrar un nuevo peso del cliente"""
        if self.verificar_ventana_abierta('registrar_peso'):
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Registrar Nuevo Peso")
        v.geometry("400x350")
        v.configure(bg="white")
        v.resizable(False, False)
        v.grab_set()
        
        self.registrar_ventana('registrar_peso', v, None)
        
        tk.Label(
            v,
            text="Registrar Peso",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=20)
        
        form_frame = tk.Frame(v, bg="white")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)
        
        tk.Label(
            form_frame,
            text="Peso (kg):",
            font=("Helvetica", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 5))
        
        var_peso = tk.StringVar()
        entry_peso = ttk.Entry(
            form_frame,
            textvariable=var_peso,
            font=("Helvetica", 11),
            width=25
        )
        entry_peso.pack(fill="x", pady=(0, 15))
        entry_peso.focus()
        
        tk.Label(
            form_frame,
            text="Fecha (DD-MM-YYYY):",
            font=("Helvetica", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 5))
        
        var_fecha = tk.StringVar()
        var_fecha.set(datetime.now().strftime("%d-%m-%Y"))
        entry_fecha = ttk.Entry(
            form_frame,
            textvariable=var_fecha,
            font=("Helvetica", 11),
            width=25
        )
        entry_fecha.pack(fill="x", pady=(0, 5))
        
        tk.Label(
            form_frame,
            text="(Si no especificas, se usa la fecha actual)",
            font=("Helvetica", 8),
            bg="white",
            fg="gray"
        ).pack(anchor="w")
        
        btn_frame = tk.Frame(v, bg="white")
        btn_frame.pack(padx=30, pady=20, fill="x", expand=True)
        
        def guardar_peso():
            peso_str = var_peso.get().strip()
            fecha_str = var_fecha.get().strip()
            
            if not peso_str:
                messagebox.showerror("Error", "Por favor ingresa un peso")
                return
            
            es_valido, mensaje = Validaciones.validar_peso(peso_str)
            if not es_valido:
                messagebox.showerror("Error", mensaje)
                return
            
            peso = float(peso_str)
            
            if fecha_str:
                try:
                    datetime.strptime(fecha_str, "%d-%m-%Y")
                except ValueError:
                    messagebox.showerror("Error", "Fecha inválida. Usa formato DD-MM-YYYY")
                    return
            else:
                fecha_str = datetime.now().strftime("%d-%m-%Y")
            
            from historial_peso import HistorialPeso
            
            rut_cliente = self.cliente_data.get('rut')
            historial = HistorialPeso(rut_cliente, peso, fecha_str)
            
            exito, mensaje = self.gimnasio.registrar_peso(historial)
            
            if exito:
                self.cliente_data['peso'] = peso
                estatura_m = self.cliente_data.get('estatura', 1) / 100
                nuevo_imc = round(peso / (estatura_m ** 2), 2)
                self.cliente_data['imc'] = nuevo_imc
                
                # Actualizar categoría IMC basada en nuevo IMC
                if nuevo_imc < 18.5:
                    categoria = "Peso bajo"
                elif nuevo_imc < 25:
                    categoria = "Peso normal"
                elif nuevo_imc < 30:
                    categoria = "Sobrepeso"
                else:
                    categoria = "Obesidad"
                self.cliente_data['categoria_imc'] = categoria
                
                self.gimnasio.cargar_datos()
                
                messagebox.showinfo("Exito", f"Peso registrado exitosamente\nPeso: {peso} kg\nFecha: {fecha_str}")
                v.destroy()
                if 'ver_datos' in self.ventanas_abiertas:
                    if self.ventanas_abiertas['ver_datos'].winfo_exists():
                        self.ventanas_abiertas['ver_datos'].destroy()
                        del self.ventanas_abiertas['ver_datos']
                self.ver_datos()
            else:
                messagebox.showerror("Error", f"No se pudo registrar el peso:\n{mensaje}")
        
        tk.Button(
            btn_frame,
            text="Guardar",
            command=guardar_peso,
            bg="#27ae60",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
            command=v.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=15
        ).pack(side="left", padx=5)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            try:
                # Cerrar todas las ventanas abiertas
                for ventana in list(self.ventanas_abiertas.values()):
                    if ventana.winfo_exists():
                        ventana.destroy()
                
                # Limpiar diccionario
                self.ventanas_abiertas.clear()
                
                # Abrir login.py desde gimnacio
                import os
                ruta_login = os.path.join(os.path.dirname(__file__), "login.py")
                subprocess.Popen([sys.executable, ruta_login])
                
                # Cerrar la ventana principal
                self.frame.winfo_toplevel().destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cerrar sesión: {e}")