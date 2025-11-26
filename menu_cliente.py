import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from suscripcion import Suscripcion
from gimnasio import Gimnacio
from ejercicios import Ejercicio
from cliente import Cliente
from entrenador import Entrenador
import subprocess
import sys
import json
import os

class MenuCliente:
    def __init__(self, parent_frame, cliente_data):
        self.frame = parent_frame
        self.cliente_data = cliente_data
        self.gimnasio = Gimnacio()
        self.ventanas_abiertas = {}  # Diccionario para rastrear ventanas abiertas
        self.botones = {}  # Diccionario para almacenar referencias a los botones
        self.crear_menu()
    
    def crear_menu(self):
        # Limpiar widgets anteriores
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Configurar el frame principal
        self.frame.configure(bg="white")
        
        # Título de bienvenida
        nombre_cliente = self.cliente_data.get('nombre', 'Cliente')
        tk.Label(
            self.frame, 
            text=f"Bienvenido, {nombre_cliente}", 
            font=("Helvetica", 18, "bold"), 
            bg="white",
            fg="#333"
        ).pack(pady=30)
        
        # Mostrar información del entrenador asignado si existe
        entrenador_info = self.obtener_info_entrenador_asignado()
        if entrenador_info:
            info_frame = tk.Frame(self.frame, bg="#e8f4fd", relief="solid", bd=1)
            info_frame.pack(fill="x", padx=40, pady=10)
            
            tk.Label(
                info_frame,
                text=f"🏋️ Entrenador: {entrenador_info}",
                font=("Helvetica", 11, "bold"),
                bg="#e8f4fd",
                fg="#2c3e50"
            ).pack(pady=8)
        
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
        archivo_entrenadores = "entrenadores.json"
        if not os.path.exists(archivo_entrenadores):
            return "Entrenador (información no disponible)"
        
        try:
            with open(archivo_entrenadores, "r", encoding="utf-8") as f:
                entrenadores = json.load(f)
            
            for entrenador in entrenadores:
                if entrenador.get('rut') == rut_entrenador:
                    nombre = entrenador.get('nombre', 'Entrenador')
                    especialidades = ', '.join(entrenador.get('especialidades', []))
                    return f"{nombre} - {especialidades}"
        except Exception as e:
            print(f"Error al obtener nombre del entrenador: {e}")
        
        return "Entrenador (información no disponible)"
    
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
        
        def al_cerrar():
            self.desbloquear_botones()
            if nombre_ventana in self.ventanas_abiertas:
                del self.ventanas_abiertas[nombre_ventana]
            ventana.destroy()
        
        ventana.protocol("WM_DELETE_WINDOW", al_cerrar)
    
    def ver_suscripcion(self):
        if self.verificar_ventana_abierta('ver_suscripcion'):
            return
        
        self.gimnasio = Gimnacio()
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
            try:
                fecha_inicio = datetime.strptime(sus.get('fecha_inicio', ''), '%Y-%m-%d')
                dias = sus.get('dias_restantes', 0)
                fecha_vencimiento = fecha_inicio + timedelta(days=dias)
                fecha_vencimiento_str = fecha_vencimiento.strftime('%d-%m-%Y')
            except:
                fecha_vencimiento_str = "No disponible"
            
            info_items = [
                ("Tipo de Suscripción:", sus.get('tipo_suscripcion', 'N/A').upper()),
                ("Fecha de Inicio:", sus.get('fecha_inicio', 'N/A')),
                ("Fecha de Vencimiento:", fecha_vencimiento_str),
                ("Días Restantes:", f"{sus.get('dias_restantes', 0)} días"),
                ("Estado:", "✅ ACTIVA" if sus.get('activa') else "❌ VENCIDA")
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
                text="🔄 Actualizar", 
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
                        if 'adquirir_suscripcion' in self.botones:
                            self.botones['adquirir_suscripcion'].config(state="normal")
                        actualizar()
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
                text="❌ No tienes suscripción activa", 
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
            nueva_sus = Suscripcion(
                self.cliente_data.get('rut'), 
                tipo.get(), 
                datetime.now().strftime("%Y-%m-%d")
            )
            exito, msg = self.gimnasio.crear_suscripcion(nueva_sus)
            messagebox.showinfo("Resultado", msg)
            if exito:
                if 'adquirir_suscripcion' in self.ventanas_abiertas:
                    del self.ventanas_abiertas['adquirir_suscripcion']
                self.desbloquear_botones()
                v.destroy()
                
                # Recargar datos de gimnasio
                self.gimnasio = Gimnacio()
                
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
        if self.verificar_ventana_abierta('ver_datos'):
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Mis Datos")
        v.geometry("500x550")
        v.configure(bg="white")
        self.registrar_ventana('ver_datos', v, 'ver_datos')
        
        tk.Label(
            v, 
            text="Información Personal", 
            font=("Helvetica", 14, "bold"), 
            bg="white"
        ).pack(pady=20)
        
        f = tk.Frame(v, bg="white")
        f.pack(padx=40, pady=10)
        
        # Obtener entrenador asignado desde JSON
        entrenador_info = self.obtener_info_entrenador_asignado()
        entrenador = entrenador_info if entrenador_info else 'Sin asignar'
        
        datos = [
            ("Nombre:", self.cliente_data.get('nombre', 'N/A')),
            ("RUT:", self.cliente_data.get('rut', 'N/A')),
            ("Estatura:", f"{self.cliente_data.get('estatura', 'N/A')} cm"),
            ("Peso:", f"{self.cliente_data.get('peso', 'N/A')} kg"),
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
        
        tk.Button(
            v, 
            text="Modificar Datos", 
            command=lambda: self.modificar_datos(v), 
            bg="#e67e22", 
            fg="white", 
            font=("Helvetica", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(pady=20)
    
    def modificar_datos(self, v_padre):
        # Cerrar ventana de datos
        if 'ver_datos' in self.ventanas_abiertas:
            del self.ventanas_abiertas['ver_datos']
        v_padre.destroy()
        
        if self.verificar_ventana_abierta('modificar_datos'):
            return
        
        v = tk.Toplevel(self.frame)
        v.title("Modificar Datos")
        v.geometry("450x400")
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
            valores = [c[1].get() for c in campos]
            
            if not all(valores):
                messagebox.showerror("Error", "Complete todos los campos")
                return
            
            if valores[4] != self.cliente_data.get('contraseña'):
                messagebox.showerror("Error", "Contraseña incorrecta")
                return
            
            try:
                cliente_mod = Cliente(
                    self.cliente_data.get('nombre'), 
                    self.cliente_data.get('rut'),
                    self.cliente_data.get('fecha_nacimiento'), 
                    float(valores[1]),  # estatura
                    float(valores[0]),  # peso
                    valores[3],  # estado_civil
                    valores[2],  # direccion
                    valores[4]   # contraseña
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
            except ValueError:
                messagebox.showerror("Error", "Peso y estatura deben ser números válidos")
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
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            try:
                # Cerrar todas las ventanas abiertas
                for ventana in list(self.ventanas_abiertas.values()):
                    if ventana.winfo_exists():
                        ventana.destroy()
                
                # Limpiar diccionario
                self.ventanas_abiertas.clear()
                
                # Abrir login.py
                subprocess.Popen([sys.executable, "login.py"])
                
                # Cerrar la ventana principal
                self.frame.winfo_toplevel().destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cerrar sesión: {e}")