import tkinter as tk
from tkinter import messagebox, ttk
import os, json
from datetime import datetime
from validaciones import Validaciones 
from entrenador import Entrenador

class AppEntrenador:
    def __init__(self, parent_frame, gimnasio=None):
        self.frame = parent_frame
        self.gimnasio = gimnasio
        self.lista_especialidades_ui = []
        self.turnos_disponibles = self.gimnasio.turnos_disponibles if self.gimnasio else []
        self.dias_trabajo = {}
        self.turnos_seleccionados = []
        self.crear_widgets()
    
    def crear_widgets(self):
        frame_centro = tk.Frame(self.frame, bg="white")
        frame_centro.pack(expand=True)
        
        tk.Label(frame_centro, text="REGISTRO DE ENTRENADOR", font=("Helvetica", 18, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=3, pady=(0, 30))
        
        # Inputs básicos
        tk.Label(frame_centro, text="Nombre Completo:", bg="white", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.input_nombre = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_nombre.grid(row=1, column=1, sticky="w", padx=10)
        
        tk.Label(frame_centro, text="RUT:", bg="white", font=("Helvetica", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.input_rut = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_rut.grid(row=2, column=1, sticky="w", padx=10)
        
        tk.Label(frame_centro, text="Contraseña:", bg="white", font=("Helvetica", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.input_contra = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10), show="*")
        self.input_contra.grid(row=3, column=1, sticky="w", padx=10)
        
        tk.Label(frame_centro, text="Fecha Nacimiento:", bg="white", font=("Helvetica", 11)).grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self.input_fecha = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_fecha.grid(row=4, column=1, sticky="w", padx=10)
        tk.Label(frame_centro, text="(DD-MM-AAAA)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=4, column=2, sticky="w")
        
        tk.Label(frame_centro, text="Estatura (cm):", bg="white", font=("Helvetica", 11)).grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self.input_estatura = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_estatura.grid(row=5, column=1, sticky="w", padx=10)
        
        tk.Label(frame_centro, text="Peso (kg):", bg="white", font=("Helvetica", 11)).grid(row=6, column=0, sticky="e", padx=10, pady=10)
        self.input_peso = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_peso.grid(row=6, column=1, sticky="w", padx=10)
        
        # Especialidades
        tk.Label(frame_centro, text="Especialidad:", bg="white", font=("Helvetica", 11)).grid(row=7, column=0, sticky="ne", padx=10, pady=10)
        frame_esp = tk.Frame(frame_centro, bg="white")
        frame_esp.grid(row=7, column=1, sticky="w", padx=10, pady=10)
        
        self.input_especialidad = ttk.Combobox(frame_esp, values=Validaciones.ESPECIALIDADES_VALIDAS, width=18, font=("Helvetica", 10), state="readonly")
        self.input_especialidad.pack(side="left")
        ttk.Button(frame_esp, text="+", width=3, command=self.agregar_especialidad_ui).pack(side="left", padx=5)
        
        self.listbox = tk.Listbox(frame_centro, height=4, width=30, borderwidth=1, relief="solid")
        self.listbox.grid(row=8, column=1, sticky="w", padx=10)
        tk.Label(frame_centro, text="(Lista de especialidades)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=8, column=2, sticky="nw")
        
        # Botón para asignar turnos
        ttk.Button(frame_centro, text='Asignar Turnos', command=self.abrir_ventana_turnos).grid(row=9, column=0, columnspan=3, pady=10)
        
        # Label para mostrar turnos seleccionados
        self.label_turnos_info = tk.Label(frame_centro, text="Turnos asignados: 0", bg="white", fg="blue", font=("Helvetica", 9))
        self.label_turnos_info.grid(row=10, column=0, columnspan=3, pady=5)
        
        ttk.Button(frame_centro, text='REGISTRAR ENTRENADOR', command=self.registrar_entrenador, style="TButton").grid(row=11, column=0, columnspan=3, pady=30, ipadx=10, ipady=5)
    
    def agregar_especialidad_ui(self):
        esp = self.input_especialidad.get().strip()
        if esp:
            if esp.lower() not in self.lista_especialidades_ui:
                self.lista_especialidades_ui.append(esp.lower())
                self.listbox.insert(tk.END, esp)
                self.input_especialidad.set('') 
            else:
                messagebox.showwarning("Atención", "Esa especialidad ya está en la lista")
        else:
            messagebox.showwarning("Atención", "Selecciona una especialidad")
    
    def abrir_ventana_turnos(self):
        """Abre ventana para seleccionar turnos predefinidos"""
        v = tk.Toplevel(self.frame)
        v.title("Asignar Turnos")
        v.geometry("500x350")
        v.configure(bg="white")
        
        tk.Label(v, text="Seleccione los turnos de trabajo", font=("Helvetica", 14, "bold"), bg="white").pack(pady=15)
        
        frame_turnos = tk.Frame(v, bg="white")
        frame_turnos.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Separar turnos de lun-vie de fin de semana
        turnos_semana = [t for t in self.turnos_disponibles if "Lun-Vie" in t['nombre']]
        turno_sabado = next((t for t in self.turnos_disponibles if "Sabado" in t['nombre']), None)
        turno_domingo = next((t for t in self.turnos_disponibles if "Domingo" in t['nombre']), None)
        
        # TURNOS LUNES A VIERNES (obligatorio elegir uno)
        tk.Label(frame_turnos, text="Turno Lunes a Viernes:", bg="white", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(10, 5))
        
        self.var_turno_semana = tk.StringVar()
        for turno in turnos_semana:
            texto = f"{turno['nombre']} ({turno['hora_inicio'][:5]} - {turno['hora_fin'][:5]})"
            tk.Radiobutton(
                frame_turnos, 
                text=texto, 
                variable=self.var_turno_semana, 
                value=turno['nombre'],
                bg="white",
                font=("Helvetica", 10)
            ).pack(anchor="w", padx=20)
        
        # Separador
        ttk.Separator(frame_turnos, orient="horizontal").pack(fill="x", pady=15)
        
        # TURNOS OPCIONALES FIN DE SEMANA
        tk.Label(frame_turnos, text="Turnos Opcionales:", bg="white", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(5, 5))
        
        # Sábado
        self.var_sabado = tk.BooleanVar()
        if turno_sabado:
            texto_sabado = f"{turno_sabado['nombre']} ({turno_sabado['hora_inicio'][:5]} - {turno_sabado['hora_fin'][:5]})"
            tk.Checkbutton(
                frame_turnos, 
                text=texto_sabado, 
                variable=self.var_sabado,
                bg="white",
                font=("Helvetica", 10)
            ).pack(anchor="w", padx=20, pady=2)
        
        # Domingo
        self.var_domingo = tk.BooleanVar()
        if turno_domingo:
            texto_domingo = f"{turno_domingo['nombre']} ({turno_domingo['hora_inicio'][:5]} - {turno_domingo['hora_fin'][:5]})"
            tk.Checkbutton(
                frame_turnos, 
                text=texto_domingo, 
                variable=self.var_domingo,
                bg="white",
                font=("Helvetica", 10)
            ).pack(anchor="w", padx=20, pady=2)
        
        # Guardar referencias a los turnos
        self.turno_sabado_ref = turno_sabado
        self.turno_domingo_ref = turno_domingo
        
        ttk.Button(v, text="Guardar Turnos", command=lambda: self.guardar_turnos(v)).pack(pady=20)
    
    def guardar_turnos(self, ventana):
        """Guarda los turnos seleccionados"""
        self.turnos_seleccionados = []
        
        # Validar que se haya seleccionado turno de semana
        turno_semana = self.var_turno_semana.get()
        if not turno_semana:
            messagebox.showerror("Error", "Debe seleccionar un turno para Lunes a Viernes")
            return
        
        # Buscar el turno completo
        turno_obj = next((t for t in self.turnos_disponibles if t['nombre'] == turno_semana), None)
        if turno_obj:
            # Calcular horas por día
            horas_dia = self.calcular_horas(turno_obj['hora_inicio'], turno_obj['hora_fin'])
            
            # Agregar lunes a viernes
            for dia in ["lunes", "martes", "miércoles", "jueves", "viernes"]:
                self.turnos_seleccionados.append({
                    "dia": dia,
                    "hora_inicio": turno_obj['hora_inicio'],
                    "hora_fin": turno_obj['hora_fin'],
                    "horas_trabajo": horas_dia
                })
        
        # Agregar sábado si está seleccionado
        if self.var_sabado.get() and self.turno_sabado_ref:
            horas_sabado = self.calcular_horas(self.turno_sabado_ref['hora_inicio'], self.turno_sabado_ref['hora_fin'])
            self.turnos_seleccionados.append({
                "dia": "sábado",
                "hora_inicio": self.turno_sabado_ref['hora_inicio'],
                "hora_fin": self.turno_sabado_ref['hora_fin'],
                "horas_trabajo": horas_sabado
            })
        
        # Agregar domingo si está seleccionado
        if self.var_domingo.get() and self.turno_domingo_ref:
            horas_domingo = self.calcular_horas(self.turno_domingo_ref['hora_inicio'], self.turno_domingo_ref['hora_fin'])
            self.turnos_seleccionados.append({
                "dia": "domingo",
                "hora_inicio": self.turno_domingo_ref['hora_inicio'],
                "hora_fin": self.turno_domingo_ref['hora_fin'],
                "horas_trabajo": horas_domingo
            })
        
        # Calcular total de horas
        total_horas = sum(t["horas_trabajo"] for t in self.turnos_seleccionados)
        self.label_turnos_info.config(
            text=f"Turnos asignados: {len(self.turnos_seleccionados)} días ({total_horas:.1f}h/semana)"
        )
        
        messagebox.showinfo("Éxito", f"Se asignaron {len(self.turnos_seleccionados)} turnos correctamente")
        ventana.destroy()
    
    def limpiar_formulario(self):
        self.input_nombre.delete(0, tk.END)
        self.input_rut.delete(0, tk.END)
        self.input_contra.delete(0, tk.END)
        self.input_fecha.delete(0, tk.END)
        self.input_estatura.delete(0, tk.END)
        self.input_peso.delete(0, tk.END)
        self.input_especialidad.set('')
        self.listbox.delete(0, tk.END)
        self.lista_especialidades_ui.clear()
        self.dias_trabajo = {}
        self.turnos_seleccionados = []
        self.label_turnos_info.config(text="Turnos asignados: 0")
    
    def registrar_entrenador(self):
        nombre = self.input_nombre.get().strip()
        rut = self.input_rut.get().strip()
        contraseña = self.input_contra.get().strip()
        fecha = self.input_fecha.get().strip()
        estatura = self.input_estatura.get().strip()
        peso = self.input_peso.get().strip()
        
        # Validaciones
        validaciones = Validaciones()
        validar_rut_formato = validaciones.validar_rut(rut)
        if not validar_rut_formato[0]:
            messagebox.showerror("Error", validar_rut_formato[1])
            return
        
        validar_rut_unico = validaciones.validar_rut_unico(rut)
        if not validar_rut_unico[0]:
            messagebox.showerror("Error", validar_rut_unico[1])
            return
        
        try:
            estatura_float = float(estatura)
            peso_float = float(peso)
        except ValueError:
            messagebox.showerror("Error", "Estatura y peso deben ser números válidos")
            return
        
        errores, advertencias = Entrenador.validar_datos(nombre, fecha, estatura_float, peso_float, contraseña)
        if errores:
            messagebox.showerror("Errores", "\n".join(errores))
            return
        if advertencias:
            messagebox.showwarning("Advertencia", "\n".join(advertencias))
        
        # Validar que se hayan asignado turnos
        if not self.turnos_seleccionados:
            messagebox.showerror("Error", "Debe asignar turnos al entrenador antes de registrar")
            return
        
        nuevo_entrenador = Entrenador(
            nombre=nombre,
            fecha_nacimiento=fecha,
            rut=rut,
            estatura=estatura_float,
            peso=peso_float,
            especialidades=[],
            contraseña=contraseña
        )
        
        for esp in self.lista_especialidades_ui:
            nuevo_entrenador.agregar_especialidad(esp)
        
        # Guardar en JSON
        datos = []
        archivo = "entrenadores.json"
        if os.path.exists(archivo):
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
            except:
                datos = []
        
        # Convertir entrenador a diccionario
        entrenador_dict = nuevo_entrenador.a_diccionario()
        
        # CORRECCIÓN: Agregar los turnos al diccionario ANTES de guardar
        entrenador_dict["turnos"] = self.turnos_seleccionados
        
        # Agregar a la lista de datos
        datos.append(entrenador_dict)
        
        # Guardar en el archivo JSON
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        total_horas = sum(t["horas_trabajo"] for t in self.turnos_seleccionados)
        messagebox.showinfo("Éxito", 
            f"Entrenador {nombre} registrado exitosamente.\n"
            f"Turnos: {len(self.turnos_seleccionados)} días ({total_horas:.1f}h/semana)"
        )
        self.limpiar_formulario()
        
        ventana_actual = self.frame.winfo_toplevel()
        ventana_actual.destroy()
    
    def calcular_horas(self, hora_inicio, hora_fin):
        """Calcula las horas entre dos horarios"""
        inicio = datetime.strptime(hora_inicio, "%H:%M:%S")
        fin = datetime.strptime(hora_fin, "%H:%M:%S")
        diferencia = fin - inicio
        return round(diferencia.total_seconds() / 3600, 2)