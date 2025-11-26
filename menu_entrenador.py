import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from gimnasio import Gimnacio
from ejercicios import Ejercicio
import json
import os

class MenuEntrenador:
    def __init__(self, parent_frame, entrenador_data):
        self.frame = parent_frame
        self.entrenador_data = entrenador_data
        self.gimnasio = Gimnacio()
        self.crear_widgets()
    
    def crear_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        titulo = tk.Label(
            self.frame,
            text=f"Bienvenido, {self.entrenador_data.get('nombre', 'Entrenador')}",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg="#333"
        )
        titulo.pack(pady=20)
        
        especialidades = ", ".join(self.entrenador_data.get('especialidades', []))
        info_frame = tk.Frame(self.frame, bg="#f0f0f0", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text=f"RUT: {self.entrenador_data.get('rut', 'N/A')} | Especialidades: {especialidades or 'Ninguna'}",
            font=("Helvetica", 11),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        frame_botones = tk.Frame(self.frame, bg="white")
        frame_botones.pack(expand=True, fill="both", padx=20, pady=20)
        
        btn_clientes = tk.Button(
            frame_botones,
            text="Ver Mis Clientes",
            command=self.ver_mis_clientes,
            font=("Helvetica", 12, "bold"),
            bg="#4a90e2",
            fg="white",
            height=3,
            relief="flat"
        )
        btn_clientes.pack(fill="x", pady=10)
        
        btn_ejercicios = tk.Button(
            frame_botones,
            text="Ver Ejercicios que Supervisé",
            command=self.ver_ejercicios,
            font=("Helvetica", 12, "bold"),
            bg="#50c878",
            fg="white",
            height=3,
            relief="flat"
        )
        btn_ejercicios.pack(fill="x", pady=10)
        
        btn_turnos = tk.Button(
            frame_botones,
            text="Ver Mis Turnos",
            command=self.ver_turnos,
            font=("Helvetica", 12, "bold"),
            bg="#f39c12",
            fg="white",
            height=3,
            relief="flat"
        )
        btn_turnos.pack(fill="x", pady=10)
        
        btn_stats = tk.Button(
            frame_botones,
            text="Mis Estadísticas",
            command=self.ver_estadisticas,
            font=("Helvetica", 12, "bold"),
            bg="#9b59b6",
            fg="white",
            height=3,
            relief="flat"
        )
        btn_stats.pack(fill="x", pady=10)
        
        btn_cerrar = tk.Button(
            frame_botones,
            text="Cerrar Sesión",
            command=self.cerrar_sesion,
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            height=3,
            relief="flat"
        )
        btn_cerrar.pack(fill="x", pady=10)
    
    def obtener_clientes_desde_json(self):
        """NUEVO MÉTODO: Obtiene clientes asignados desde el JSON"""
        archivo = "clientes.json"
        if not os.path.exists(archivo):
            return {}
        
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                clientes = json.load(f)
            
            mis_clientes = {}
            rut_entrenador = self.entrenador_data.get('rut')
            
            for cliente in clientes:
                if cliente.get('entrenador_asignado') == rut_entrenador:
                    # Contar sesiones desde ejercicios.json si existe
                    sesiones = 0
                    ejercicios_archivo = "ejercicios.json"
                    if os.path.exists(ejercicios_archivo):
                        try:
                            with open(ejercicios_archivo, "r", encoding="utf-8") as f_ej:
                                ejercicios = json.load(f_ej)
                                for ejercicio in ejercicios:
                                    if ejercicio.get('rut_cliente') == cliente['rut']:
                                        sesiones += 1
                        except:
                            pass
                    
                    mis_clientes[cliente['nombre']] = {
                        'rut': cliente['rut'],
                        'total_sesiones': sesiones,
                        'imc': cliente.get('imc', 'N/A'),
                        'categoria_imc': cliente.get('categoria_imc', 'N/A'),
                        'rutina_mensual': cliente.get('rutina_mensual', 'N/A')
                    }
            
            return mis_clientes
        
        except Exception as e:
            print(f"Error al cargar clientes desde JSON: {e}")
            return {}
    
    def ver_mis_clientes(self):
        # PRIMERO intenta obtener clientes desde el JSON
        clientes_json = self.obtener_clientes_desde_json()
        
        # LUEGO intenta con el método del gimnasio (para compatibilidad)
        try:
            clientes_gimnasio = self.gimnasio.obtener_clientes_por_entrenador(self.entrenador_data.get('nombre'))
        except:
            clientes_gimnasio = {}
        
        # Combina ambos resultados (priorizando JSON)
        clientes = {**clientes_gimnasio, **clientes_json}
        
        ventana = tk.Toplevel(self.frame)
        ventana.title("Mis Clientes")
        ventana.geometry("700x500")
        ventana.configure(bg="white")
        
        tk.Label(
            ventana,
            text="Clientes Asignados",
            font=("Helvetica", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        if not clientes:
            tk.Label(
                ventana,
                text="No tienes clientes asignados aún",
                font=("Helvetica", 12),
                bg="white",
                fg="#666"
            ).pack(pady=20)
            return
        
        frame_principal = tk.Frame(ventana)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for nombre_cliente, datos in clientes.items():
            card = tk.Frame(scrollable_frame, bg="#f0f0f0", relief="solid", bd=1)
            card.pack(fill="x", pady=5, padx=10)
            
            info = f"Nombre: {nombre_cliente}\nRUT: {datos.get('rut', 'N/A')}\nSesiones: {datos.get('total_sesiones', 0)}"
            
            # Añadir información adicional si está disponible desde JSON
            if 'imc' in datos and datos['imc'] != 'N/A':
                info += f"\nIMC: {datos.get('imc', 'N/A')}"
            if 'categoria_imc' in datos and datos['categoria_imc'] != 'N/A':
                info += f"\nCategoría: {datos.get('categoria_imc', 'N/A')}"
            
            tk.Label(
                card,
                text=info,
                font=("Helvetica", 10),
                bg="#f0f0f0",
                justify="left"
            ).pack(pady=10, padx=10, side="left", fill="both", expand=True)
            
            btn_frame = tk.Frame(card, bg="#f0f0f0")
            btn_frame.pack(pady=10, padx=10, side="right")
            
            tk.Button(
                btn_frame,
                text="Añadir Rutina",
                command=lambda rut=datos.get('rut'), nom=nombre_cliente: self.anadir_rutina_cliente(rut, nom),
                bg="#50c878",
                fg="white",
                font=("Helvetica", 9, "bold")
            ).pack()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            ventana,
            text=f"Total de clientes: {len(clientes)}",
            font=("Helvetica", 11, "bold"),
            bg="white"
        ).pack(pady=10)
    
    def anadir_rutina_cliente(self, rut_cliente, nombre_cliente):
        v = tk.Toplevel(self.frame)
        v.title(f"Añadir Rutina a {nombre_cliente}")
        v.geometry("450x400")
        
        tk.Label(v, text=f"Nueva Rutina para {nombre_cliente}", 
                font=("Helvetica", 14, "bold")).pack(pady=20)
        
        f = tk.Frame(v)
        f.pack(padx=30)
        
        campos = [
            ("Nombre Ejercicio:", tk.Entry(f, width=25)),
            ("Tipo:", ttk.Combobox(f, values=["cardio", "fuerza", "resistencia", "flexibilidad", "funcional"], width=23, state="readonly")),
            ("Duración (min):", tk.Entry(f, width=25)),
            ("Fecha:", tk.Entry(f, width=25))
        ]
        
        for i, (label, widget) in enumerate(campos):
            tk.Label(f, text=label).grid(row=i, column=0, sticky="e", pady=5)
            widget.grid(row=i, column=1, pady=5)
            if i == 1: widget.set("cardio")
            if i == 3: widget.insert(0, datetime.now().strftime("%d-%m-%Y"))
        
        def guardar():
            valores = [c[1].get() for c in campos]
            if not all(valores):
                return messagebox.showerror("Error", "Complete todos los campos")
            
            ej = Ejercicio(valores[0], valores[3], valores[1], self.entrenador_data.get('nombre'), valores[2], rut_cliente)
            exito, msg = self.gimnasio.registrar_ejercicio(ej)
            messagebox.showinfo("Resultado", msg)
            if exito: v.destroy()
        
        tk.Button(v, text="Guardar", command=guardar, bg="#50c878", fg="white", 
                 font=("Helvetica", 11, "bold")).pack(pady=20)
    
    def ver_ejercicios(self):
        ejercicios = self.gimnasio.obtener_ejercicios_por_entrenador(
            self.entrenador_data.get('nombre')
        )
        
        ventana = tk.Toplevel(self.frame)
        ventana.title("Ejercicios Supervisados")
        ventana.geometry("700x500")
        ventana.configure(bg="white")
        
        tk.Label(
            ventana,
            text="Ejercicios que he Supervisado",
            font=("Helvetica", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        if not ejercicios:
            tk.Label(
                ventana,
                text="No has supervisado ejercicios aún",
                font=("Helvetica", 12),
                bg="white",
                fg="#666"
            ).pack(pady=20)
            return
        
        frame_principal = tk.Frame(ventana)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame_principal, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for ejercicio in ejercicios:
            card = tk.Frame(scrollable_frame, bg="#f0f0f0", relief="solid", bd=1)
            card.pack(fill="x", pady=5, padx=10)
            
            exito, cliente = self.gimnasio.buscar_cliente_por_rut(ejercicio.get('rut_cliente'))
            nombre_cliente = cliente.get('nombre', 'N/A') if exito else 'N/A'
            
            info = f"Ejercicio: {ejercicio.get('nombre_ejercicio', 'N/A')}\nCliente: {nombre_cliente} | Tipo: {ejercicio.get('tipo_ejercicio', 'N/A')}\nDuración: {ejercicio.get('duracion_minutos', 'N/A')} min | Fecha: {ejercicio.get('fecha', 'N/A')}"
            
            tk.Label(
                card,
                text=info,
                font=("Helvetica", 10),
                bg="#f0f0f0",
                justify="left"
            ).pack(pady=10, padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(
            ventana,
            text=f"Total de ejercicios: {len(ejercicios)}",
            font=("Helvetica", 11, "bold"),
            bg="white"
        ).pack(pady=10)
    
    def ver_turnos(self):
        turnos = self.gimnasio.obtener_turnos_entrenador(self.entrenador_data.get('rut'))
        
        ventana = tk.Toplevel(self.frame)
        ventana.title("Mis Turnos")
        ventana.geometry("500x400")
        ventana.configure(bg="white")
        
        tk.Label(
            ventana,
            text="Horario de Trabajo",
            font=("Helvetica", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        if not turnos:
            tk.Label(
                ventana,
                text="No tienes turnos asignados",
                font=("Helvetica", 12),
                bg="white",
                fg="#666"
            ).pack(pady=20)
            return
        
        frame_turnos = tk.Frame(ventana, bg="white")
        frame_turnos.pack(expand=True, padx=20, pady=10)
        
        for turno in turnos:
            card = tk.Frame(frame_turnos, bg="#f0f0f0", relief="solid", bd=1)
            card.pack(fill="x", pady=5)
            
            info = f"{turno.get('dia_semana', 'N/A').upper()}: {turno.get('hora_inicio', 'N/A')} - {turno.get('hora_fin', 'N/A')} ({turno.get('horas_trabajo', 0):.1f} horas)"
            
            tk.Label(
                card,
                text=info,
                font=("Helvetica", 11),
                bg="#f0f0f0"
            ).pack(pady=10, padx=10)
        
        total_horas = self.gimnasio.calcular_horas_semanales_entrenador(
            self.entrenador_data.get('rut')
        )
        
        tk.Label(
            ventana,
            text=f"Total horas semanales: {total_horas}",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="#50c878"
        ).pack(pady=20)
    
    def ver_estadisticas(self):
        ventana = tk.Toplevel(self.frame)
        ventana.title("Mis Estadísticas")
        ventana.geometry("500x400")
        ventana.configure(bg="white")
        
        tk.Label(
            ventana,
            text="Estadísticas de Desempeño",
            font=("Helvetica", 16, "bold"),
            bg="white"
        ).pack(pady=20)
        
        # Obtiene clientes desde JSON para estadísticas más precisas
        clientes_json = self.obtener_clientes_desde_json()
        total_clientes = len(clientes_json)
        
        ejercicios = self.gimnasio.obtener_ejercicios_por_entrenador(
            self.entrenador_data.get('nombre')
        )
        total_ejercicios = len(ejercicios)
        
        turnos = self.gimnasio.obtener_turnos_entrenador(self.entrenador_data.get('rut'))
        total_horas = self.gimnasio.calcular_horas_semanales_entrenador(
            self.entrenador_data.get('rut')
        )
        
        frame_stats = tk.Frame(ventana, bg="white")
        frame_stats.pack(expand=True, padx=40)
        
        stats = [
            ("Clientes Asignados", total_clientes, "#4a90e2"),
            ("Ejercicios Supervisados", total_ejercicios, "#50c878"),
            ("Turnos Asignados", len(turnos), "#f39c12"),
            ("Horas Semanales", f"{total_horas:.1f}", "#9b59b6")
        ]
        
        for titulo, valor, color in stats:
            card = tk.Frame(frame_stats, bg=color, relief="raised", bd=2)
            card.pack(fill="x", pady=10)
            
            tk.Label(
                card,
                text=titulo,
                font=("Helvetica", 11),
                bg=color,
                fg="white"
            ).pack(pady=5)
            
            tk.Label(
                card,
                text=str(valor),
                font=("Helvetica", 20, "bold"),
                bg=color,
                fg="white"
            ).pack(pady=5)
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Desea cerrar sesión?"):
            ventana_actual = self.frame.winfo_toplevel()
            ventana_actual.destroy()
            
            import subprocess
            import sys
            subprocess.Popen([sys.executable, "login.py"])