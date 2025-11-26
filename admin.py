import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
from gimnasio import Gimnacio
from cliente import Cliente
from entrenador import Entrenador

class AdminGimnasio:
    def __init__(self, parent_frame, admin_data):
        self.frame = parent_frame
        self.admin_data = admin_data
        self.gimnasio = Gimnacio()
        self.ventanas_abiertas = {}  # Diccionario para rastrear ventanas abiertas
        self.botones = {}  # Diccionario para almacenar referencias a los botones
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        titulo = tk.Label(
            self.frame,
            text="PANEL ADMINISTRATIVO",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg="#333"
        )
        titulo.pack(pady=20)

        # Nombre del admin
        subtitulo = tk.Label(
            self.frame,
            text=f"Administrador: {self.admin_data.get('nombre', 'Admin')}",
            font=("Helvetica", 12),
            bg="white",
            fg="#666"
        )
        subtitulo.pack(pady=10)

        # Frame de botones
        frame_botones = tk.Frame(self.frame, bg="white")
        frame_botones.pack(expand=True, fill="both", padx=20, pady=20)

        # Botón Registrar (unificado)
        self.botones['registrar'] = tk.Button(
            frame_botones,
            text="Registrar Cliente/Entrenador",
            command=self.abrir_registro,
            font=("Helvetica", 12, "bold"),
            bg="#4a90e2",
            fg="white",
            height=3,
            relief="flat"
        )
        self.botones['registrar'].pack(fill="x", pady=10)

        # Botón Ver Clientes
        self.botones['ver_clientes'] = tk.Button(
            frame_botones,
            text="Ver Clientes",
            command=self.ver_clientes,
            font=("Helvetica", 12, "bold"),
            bg="#f39c12",
            fg="white",
            height=3,
            relief="flat"
        )
        self.botones['ver_clientes'].pack(fill="x", pady=10)

        # Botón Ver Entrenadores
        self.botones['ver_entrenadores'] = tk.Button(
            frame_botones,
            text="Ver Entrenadores",
            command=self.ver_entrenadores,
            font=("Helvetica", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            height=3,
            relief="flat"
        )
        self.botones['ver_entrenadores'].pack(fill="x", pady=10)

        # Botón Cerrar Sesión
        btn_cerrar_sesion = tk.Button(
            frame_botones,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            height=3,
            relief="flat"
        )
        btn_cerrar_sesion.pack(fill="x", pady=10)

    def bloquear_botones(self, excepto=None):
        """Bloquea todos los botones excepto el especificado"""
        for nombre, boton in self.botones.items():
            if nombre != excepto:
                boton.config(state="disabled")

    def desbloquear_botones(self):
        """Desbloquea todos los botones"""
        for boton in self.botones.values():
            boton.config(state="normal")

    def abrir_registro(self):
        # Verificar si ya hay una ventana de registro abierta
        if 'registro' in self.ventanas_abiertas and self.ventanas_abiertas['registro'].winfo_exists():
            self.ventanas_abiertas['registro'].lift()  # Traer al frente
            return

        try:
            # Bloquear botones
            self.bloquear_botones('registrar')
            
            # Abrir registro.py
            proceso = subprocess.Popen([sys.executable, "registro.py"])
            
            # Crear ventana invisible para monitorear el proceso
            ventana_monitor = tk.Toplevel(self.frame)
            ventana_monitor.withdraw()  # Ocultar ventana
            self.ventanas_abiertas['registro'] = ventana_monitor
            
            # Monitorear el proceso
            def verificar_proceso():
                if proceso.poll() is not None:  # Proceso terminado
                    self.desbloquear_botones()
                    if 'registro' in self.ventanas_abiertas:
                        del self.ventanas_abiertas['registro']
                    ventana_monitor.destroy()
                else:
                    ventana_monitor.after(500, verificar_proceso)
            
            verificar_proceso()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el registro: {e}")
            self.desbloquear_botones()

    def actualizar_lista_clientes(self, scrollable_frame):
        """Actualiza la lista de clientes en la interfaz"""
        # Limpiar el frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # Recargar datos del gimnasio
        self.gimnasio = Gimnacio()
        
        # Mostrar cada cliente
        if self.gimnasio.clientes:
            for i, cliente in enumerate(self.gimnasio.clientes):
                self.crear_card_cliente(scrollable_frame, cliente, i)
        else:
            tk.Label(
                scrollable_frame,
                text="No hay clientes registrados",
                font=("Helvetica", 12),
                bg="white",
                fg="#999"
            ).pack(pady=50)

    def ver_clientes(self):
        # Verificar si ya hay una ventana de clientes abierta
        if 'clientes' in self.ventanas_abiertas and self.ventanas_abiertas['clientes'].winfo_exists():
            self.ventanas_abiertas['clientes'].lift()  # Traer al frente
            return

        if not self.gimnasio.clientes:
            messagebox.showinfo("Información", "No hay clientes registrados")
            return

        # Bloquear botones
        self.bloquear_botones('ver_clientes')

        ventana = tk.Toplevel(self.frame)
        ventana.title("Clientes")
        ventana.geometry("700x500")
        self.ventanas_abiertas['clientes'] = ventana

        # Evento al cerrar la ventana
        def al_cerrar():
            self.desbloquear_botones()
            if 'clientes' in self.ventanas_abiertas:
                del self.ventanas_abiertas['clientes']
            ventana.destroy()

        ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

        # Frame principal con scroll
        frame_principal = tk.Frame(ventana)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas con scrollbar
        canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Guardar referencia del scrollable_frame para actualizaciones
        ventana.scrollable_frame = scrollable_frame

        # Mostrar cada cliente
        self.actualizar_lista_clientes(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def crear_card_cliente(self, parent, cliente, index):
        # Frame para cada cliente
        card = tk.Frame(parent, bg="#f0f0f0", relief="solid", bd=1)
        card.pack(fill="x", pady=10, padx=10)

        # Información del cliente
        info = f"Nombre: {cliente.get('nombre', 'N/A')} | RUT: {cliente.get('rut', 'N/A')} | Peso: {cliente.get('peso', 'N/A')} kg | Estatura: {cliente.get('estatura', 'N/A')} cm | IMC: {cliente.get('imc', 'N/A')}"
        
        tk.Label(card, text=info, font=("Helvetica", 10), bg="#f0f0f0", anchor="w", justify="left").pack(fill="x", padx=10, pady=5)

        # Frame de botones
        frame_botones = tk.Frame(card, bg="#f0f0f0")
        frame_botones.pack(fill="x", padx=10, pady=5)

        btn_modificar = tk.Button(
            frame_botones,
            text="Modificar",
            command=lambda: self.modificar_cliente(cliente),
            bg="#3498db",
            fg="white",
            font=("Helvetica", 9),
            relief="flat"
        )
        btn_modificar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            command=lambda: self.eliminar_cliente(cliente.get('rut')),
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 9),
            relief="flat"
        )
        btn_eliminar.pack(side="left", padx=5)

    def modificar_cliente(self, cliente):
        ventana_mod = tk.Toplevel(self.frame)
        ventana_mod.title("Modificar Cliente")
        ventana_mod.geometry("400x400")

        tk.Label(ventana_mod, text="Modificar Cliente", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Campos
        tk.Label(ventana_mod, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_mod, width=30)
        entry_nombre.insert(0, cliente.get('nombre', ''))
        entry_nombre.pack(pady=5)

        tk.Label(ventana_mod, text="Peso (kg):").pack()
        entry_peso = tk.Entry(ventana_mod, width=30)
        entry_peso.insert(0, cliente.get('peso', ''))
        entry_peso.pack(pady=5)

        tk.Label(ventana_mod, text="Estatura (cm):").pack()
        entry_estatura = tk.Entry(ventana_mod, width=30)
        entry_estatura.insert(0, cliente.get('estatura', ''))
        entry_estatura.pack(pady=5)

        tk.Label(ventana_mod, text="Contraseña:").pack()
        entry_contraseña = tk.Entry(ventana_mod, width=30, show="*")
        entry_contraseña.insert(0, cliente.get('contraseña', ''))
        entry_contraseña.pack(pady=5)

        def guardar_cambios():
            nombre = entry_nombre.get().strip()
            peso = entry_peso.get().strip()
            estatura = entry_estatura.get().strip()
            contraseña = entry_contraseña.get().strip()

            if not nombre or not peso or not estatura or not contraseña:
                messagebox.showerror("Error", "Complete todos los campos")
                return

            try:
                peso = float(peso)
                estatura = float(estatura)
            except ValueError:
                messagebox.showerror("Error", "Peso y estatura deben ser números")
                return

            cliente_modificado = Cliente(
                nombre=nombre,
                rut=cliente.get('rut'),
                fecha_nacimiento=cliente.get('fecha_nacimiento'),
                estatura=estatura,
                peso=peso,
                estado_civil=cliente.get('estado_civil', 'soltero'),
                direccion=cliente.get('direccion', ''),
                contraseña=contraseña
            )

            exito, mensaje = self.gimnasio.modificar_cliente(cliente.get('rut'), cliente_modificado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_mod.destroy()
                # Actualizar la lista si la ventana está abierta
                if 'clientes' in self.ventanas_abiertas:
                    ventana_clientes = self.ventanas_abiertas['clientes']
                    if hasattr(ventana_clientes, 'scrollable_frame'):
                        self.actualizar_lista_clientes(ventana_clientes.scrollable_frame)
            else:
                messagebox.showerror("Error", mensaje)

        tk.Button(ventana_mod, text="Guardar", command=guardar_cambios, bg="#50c878", fg="white", width=20).pack(pady=20)

    def eliminar_cliente(self, rut):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este cliente?"):
            exito, mensaje = self.gimnasio.eliminar_cliente(rut)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                # Actualizar la lista inmediatamente después de eliminar
                if 'clientes' in self.ventanas_abiertas:
                    ventana_clientes = self.ventanas_abiertas['clientes']
                    if hasattr(ventana_clientes, 'scrollable_frame'):
                        self.actualizar_lista_clientes(ventana_clientes.scrollable_frame)
            else:
                messagebox.showerror("Error", mensaje)

    def actualizar_lista_entrenadores(self, scrollable_frame):
        """Actualiza la lista de entrenadores en la interfaz"""
        # Limpiar el frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # Recargar datos del gimnasio
        self.gimnasio = Gimnacio()
        
        # Mostrar cada entrenador
        if self.gimnasio.entrenadores:
            for i, entrenador in enumerate(self.gimnasio.entrenadores):
                self.crear_card_entrenador(scrollable_frame, entrenador, i)
        else:
            tk.Label(
                scrollable_frame,
                text="No hay entrenadores registrados",
                font=("Helvetica", 12),
                bg="white",
                fg="#999"
            ).pack(pady=50)

    def ver_entrenadores(self):
        # Verificar si ya hay una ventana de entrenadores abierta
        if 'entrenadores' in self.ventanas_abiertas and self.ventanas_abiertas['entrenadores'].winfo_exists():
            self.ventanas_abiertas['entrenadores'].lift()  # Traer al frente
            return

        if not self.gimnasio.entrenadores:
            messagebox.showinfo("Información", "No hay entrenadores registrados")
            return

        # Bloquear botones
        self.bloquear_botones('ver_entrenadores')

        ventana = tk.Toplevel(self.frame)
        ventana.title("Entrenadores")
        ventana.geometry("700x500")
        self.ventanas_abiertas['entrenadores'] = ventana

        # Evento al cerrar la ventana
        def al_cerrar():
            self.desbloquear_botones()
            if 'entrenadores' in self.ventanas_abiertas:
                del self.ventanas_abiertas['entrenadores']
            ventana.destroy()

        ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

        # Frame principal con scroll
        frame_principal = tk.Frame(ventana)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas con scrollbar
        canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Guardar referencia del scrollable_frame para actualizaciones
        ventana.scrollable_frame = scrollable_frame

        # Mostrar cada entrenador
        self.actualizar_lista_entrenadores(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def crear_card_entrenador(self, parent, entrenador, index):
        # Frame para cada entrenador
        card = tk.Frame(parent, bg="#f0f0f0", relief="solid", bd=1)
        card.pack(fill="x", pady=10, padx=10)

        # Información del entrenador
        especialidades = ", ".join(entrenador.get('especialidades', []))
        info = f"Nombre: {entrenador.get('nombre', 'N/A')} | RUT: {entrenador.get('rut', 'N/A')} | Especialidades: {especialidades}"
        
        tk.Label(card, text=info, font=("Helvetica", 10), bg="#f0f0f0", anchor="w", justify="left").pack(fill="x", padx=10, pady=5)

        # Frame de botones
        frame_botones = tk.Frame(card, bg="#f0f0f0")
        frame_botones.pack(fill="x", padx=10, pady=5)

        btn_modificar = tk.Button(
            frame_botones,
            text="Modificar",
            command=lambda: self.modificar_entrenador(entrenador),
            bg="#3498db",
            fg="white",
            font=("Helvetica", 9),
            relief="flat"
        )
        btn_modificar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            command=lambda: self.eliminar_entrenador(entrenador.get('rut')),
            bg="#e74c3c",
            fg="white",
            font=("Helvetica", 9),
            relief="flat"
        )
        btn_eliminar.pack(side="left", padx=5)

    def modificar_entrenador(self, entrenador):
        ventana_mod = tk.Toplevel(self.frame)
        ventana_mod.title("Modificar Entrenador")
        ventana_mod.geometry("400x400")

        tk.Label(ventana_mod, text="Modificar Entrenador", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Campos
        tk.Label(ventana_mod, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana_mod, width=30)
        entry_nombre.insert(0, entrenador.get('nombre', ''))
        entry_nombre.pack(pady=5)

        tk.Label(ventana_mod, text="Peso (kg):").pack()
        entry_peso = tk.Entry(ventana_mod, width=30)
        entry_peso.insert(0, entrenador.get('peso', ''))
        entry_peso.pack(pady=5)

        tk.Label(ventana_mod, text="Estatura (cm):").pack()
        entry_estatura = tk.Entry(ventana_mod, width=30)
        entry_estatura.insert(0, entrenador.get('estatura', ''))
        entry_estatura.pack(pady=5)

        tk.Label(ventana_mod, text="Contraseña:").pack()
        entry_contraseña = tk.Entry(ventana_mod, width=30, show="*")
        entry_contraseña.insert(0, entrenador.get('contraseña', ''))
        entry_contraseña.pack(pady=5)

        def guardar_cambios():
            nombre = entry_nombre.get().strip()
            peso = entry_peso.get().strip()
            estatura = entry_estatura.get().strip()
            contraseña = entry_contraseña.get().strip()

            if not nombre or not peso or not estatura or not contraseña:
                messagebox.showerror("Error", "Complete todos los campos")
                return

            try:
                peso = float(peso)
                estatura = float(estatura)
            except ValueError:
                messagebox.showerror("Error", "Peso y estatura deben ser números")
                return

            entrenador_modificado = Entrenador(
                nombre=nombre,
                fecha_nacimiento=entrenador.get('fecha_nacimiento'),
                rut=entrenador.get('rut'),
                estatura=estatura,
                peso=peso,
                especialidades=entrenador.get('especialidades', []),
                contraseña=contraseña
            )

            exito, mensaje = self.gimnasio.modificar_entrenador(entrenador.get('rut'), entrenador_modificado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                ventana_mod.destroy()
                # Actualizar la lista si la ventana está abierta
                if 'entrenadores' in self.ventanas_abiertas:
                    ventana_entrenadores = self.ventanas_abiertas['entrenadores']
                    if hasattr(ventana_entrenadores, 'scrollable_frame'):
                        self.actualizar_lista_entrenadores(ventana_entrenadores.scrollable_frame)
            else:
                messagebox.showerror("Error", mensaje)

        tk.Button(ventana_mod, text="Guardar", command=guardar_cambios, bg="#50c878", fg="white", width=20).pack(pady=20)

    def eliminar_entrenador(self, rut):
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este entrenador?"):
            exito, mensaje = self.gimnasio.eliminar_entrenador(rut)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                # Actualizar la lista inmediatamente después de eliminar
                if 'entrenadores' in self.ventanas_abiertas:
                    ventana_entrenadores = self.ventanas_abiertas['entrenadores']
                    if hasattr(ventana_entrenadores, 'scrollable_frame'):
                        self.actualizar_lista_entrenadores(ventana_entrenadores.scrollable_frame)
            else:
                messagebox.showerror("Error", mensaje)

    def cerrar_sesion(self):
        """Cierra la sesión actual y regresa al login"""
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            try:
                # Cerrar todas las ventanas abiertas
                for ventana in self.ventanas_abiertas.values():
                    if ventana.winfo_exists():
                        ventana.destroy()
                
                # Abrir login.py
                subprocess.Popen([sys.executable, "login.py"])
                
                # Cerrar la ventana principal (buscar la ventana root)
                root = self.frame.winfo_toplevel()
                root.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cerrar sesión: {e}")