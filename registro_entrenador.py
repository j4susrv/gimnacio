import tkinter as tk
from tkinter import messagebox, ttk
import os, json
from validaciones import Validaciones
# IMPORTACIÓN CLAVE: Traemos tu clase Entrenador desde tu archivo
from entrenador import Entrenador 

class AppEntrenador:
    def __init__(self, parent_frame):
        self.frame = parent_frame
        self.lista_especialidades_ui = [] # Lista temporal para la interfaz
        self.crear_widgets()

    def crear_widgets(self):
        # Frame central para centrar contenido
        frame_centro = tk.Frame(self.frame, bg="white")
        frame_centro.pack(expand=True)

        tk.Label(frame_centro, text="REGISTRO DE ENTRENADOR", font=("Helvetica", 18, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=3, pady=(0, 30))

        # Inputs
        tk.Label(frame_centro, text="Nombre Completo:", bg="white", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.input_nombre = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_nombre.grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(frame_centro, text="RUT:", bg="white", font=("Helvetica", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.input_rut = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_rut.grid(row=2, column=1, sticky="w", padx=10)

        tk.Label(frame_centro, text="Fecha Nacimiento:", bg="white", font=("Helvetica", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.input_fecha = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_fecha.grid(row=3, column=1, sticky="w", padx=10)
        tk.Label(frame_centro, text="(DD-MM-AAAA)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=3, column=2, sticky="w")

        tk.Label(frame_centro, text="Estatura (cm):", bg="white", font=("Helvetica", 11)).grid(row=4, column=0, sticky="e", padx=10, pady=10)
        self.input_estatura = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_estatura.grid(row=4, column=1, sticky="w", padx=10)

        tk.Label(frame_centro, text="Peso (kg):", bg="white", font=("Helvetica", 11)).grid(row=5, column=0, sticky="e", padx=10, pady=10)
        self.input_peso = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
        self.input_peso.grid(row=5, column=1, sticky="w", padx=10)

        # Especialidades
        tk.Label(frame_centro, text="Especialidad:", bg="white", font=("Helvetica", 11)).grid(row=6, column=0, sticky="ne", padx=10, pady=10)
        frame_esp = tk.Frame(frame_centro, bg="white")
        frame_esp.grid(row=6, column=1, sticky="w", padx=10, pady=10)

        # Usamos las validaciones para llenar el Combobox
        self.input_especialidad = ttk.Combobox(frame_esp, values=Validaciones.ESPECIALIDADES_VALIDAS, width=18, font=("Helvetica", 10), state="readonly")
        self.input_especialidad.pack(side="left")

        ttk.Button(frame_esp, text="+", width=3, command=self.agregar_especialidad_ui).pack(side="left", padx=5)

        self.listbox = tk.Listbox(frame_centro, height=4, width=30, borderwidth=1, relief="solid")
        self.listbox.grid(row=7, column=1, sticky="w", padx=10)
        tk.Label(frame_centro, text="(Lista de especialidades)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=7, column=2, sticky="nw")

        ttk.Button(frame_centro, text='REGISTRAR ENTRENADOR', command=self.registrar_entrenador, style="TButton").grid(row=8, column=0, columnspan=3, pady=30, ipadx=10, ipady=5)

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

    def limpiar_formulario(self):
        self.input_nombre.delete(0, tk.END)
        self.input_rut.delete(0, tk.END)
        self.input_fecha.delete(0, tk.END)
        self.input_estatura.delete(0, tk.END)
        self.input_peso.delete(0, tk.END)
        self.input_especialidad.set('')
        self.listbox.delete(0, tk.END)
        self.lista_especialidades_ui.clear()

    def registrar_entrenador(self):
        # 1. Recogemos datos de la interfaz
        nombre = self.input_nombre.get().strip()
        rut = self.input_rut.get().strip()
        fecha = self.input_fecha.get().strip()
        estatura = self.input_estatura.get().strip()
        peso = self.input_peso.get().strip()

        # 2. Validamos los datos básicos ANTES de crear el objeto
        # Usamos directamente la clase Validaciones para chequear campos
        errores = []
        if not Validaciones.validar_nombre(nombre)[0]: errores.append("Nombre inválido")
        if not Validaciones.validar_rut(rut)[0]: errores.append("RUT inválido")
        if not Validaciones.validar_fecha_nacimiento(fecha)[0]: errores.append("Fecha inválida")
        if not Validaciones.validar_estatura(estatura)[0]: errores.append("Estatura inválida")
        if not Validaciones.validar_peso(peso)[0]: errores.append("Peso inválido")

        if errores:
            messagebox.showerror("Errores de Validación", "\n".join(errores))
            return

        # 3. Creamos la instancia de TU clase Entrenador (importada)
        # Inicializamos con lista vacía y luego agregamos las especialidades validadas
        nuevo_entrenador = Entrenador(nombre, fecha, rut, estatura, peso, [])
        
        # Agregamos las especialidades usando el método de tu clase
        for esp in self.lista_especialidades_ui:
            nuevo_entrenador.agregar_especialidad(esp)

        # 4. Guardamos en JSON
        archivo = "entrenadores.json"
        datos = []
        if os.path.exists(archivo):
            try:
                with open(archivo, "r") as f:
                    datos = json.load(f)
            except: datos = []
        
        datos.append(nuevo_entrenador.a_diccionario())
        
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)

        messagebox.showinfo("Éxito", f"Entrenador {nombre} registrado correctamente.")
        self.limpiar_formulario()