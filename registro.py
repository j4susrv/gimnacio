import tkinter as tk
from tkinter import messagebox, ttk
import os, json
from validaciones import Validaciones 
from registro_entrenador import AppEntrenador

def guardar_cliente(data):
    archivo = "clientes.json"

    # Crear archivo si no existe
    if not os.path.exists(archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

    # Cargar contenido existente
    with open(archivo, "r", encoding="utf-8") as f:
        clientes = json.load(f)

    # Agregar nuevo cliente
    clientes.append(data)

    # Guardar de nuevo
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4)


ventana = tk.Tk()
ventana.title("Sistema de Gestión - Gimnasio")
ventana.geometry("900x700")
ventana.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#f0f0f0")
style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[10, 5])
style.configure("TLabel", background="white", font=("Helvetica", 11))
style.configure("TButton", font=("Helvetica", 11, "bold"), background="#4a90e2", foreground="white", borderwidth=0)
style.map("TButton", background=[("active", "#357abd")])

notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Marcos de pestañas
cliente = tk.Frame(notebook, bg="white")
entrenador = tk.Frame(notebook, bg="white")

notebook.add(cliente, text="  Cliente  ")
notebook.add(entrenador, text="  Entrenador  ")

app_entrenador = AppEntrenador(entrenador)
# notebook.add(administrador, text="  Admin  ") # Descomentar cuando lo use

# logica
def ingresar_usuario():
    nombre = input_nombre.get().strip()
    rut = input_rut.get().strip()
    contraseña = input_contraseña.get().strip()
    fecha_nacimiento = input_fecha_nacimiento.get().strip()
    estatura = input_estatura.get().strip()
    peso = input_peso.get().strip()

    validaciones = Validaciones()
    validar_nombre = validaciones.validar_nombre(nombre)
    validar_rut = validaciones.validar_rut(rut)  
    validar_contraseña = validaciones.validar_contraseña(contraseña)
    validar_fecha_nacimiento = validaciones.validar_fecha_nacimiento(fecha_nacimiento)
    validar_estatura  = validaciones.validar_estatura(estatura)
    validar_peso = validaciones.validar_peso(peso)

    print(f"Nombre: {validar_nombre}")
    print(f"RUT: {validar_rut}")
    print(f"Contraseña: {validar_contraseña}")
    print(f"Fecha: {validar_fecha_nacimiento}")
    print(f"Estatura: {validar_estatura}")
    print(f"Peso: {validar_peso}")

    if validar_nombre[0] and validar_rut[0] and validar_contraseña[0] and validar_fecha_nacimiento[0] and validar_estatura[0] and validar_peso[0]:

        nuevo_cliente = {
            "nombre": nombre,
            "rut": rut,
            "contraseña": input_contraseña.get().strip(),
            "fecha_nacimiento": fecha_nacimiento,
            "estatura": estatura,
            "peso": peso
        }

        guardar_cliente(nuevo_cliente)

        messagebox.showinfo("Éxito", "Usuario registrado correctamente")

    else:
        print("\n Errores encontrados")
        errores = ""
        if not validar_nombre[0]: errores += f"- {validar_nombre[1]}\n"
        if not validar_rut[0]: errores += f"- {validar_rut[1]}\n"
        if not validar_fecha_nacimiento[0]: errores += f"- {validar_fecha_nacimiento[1]}\n"
        if not validar_estatura[0]: errores += f"- {validar_estatura[1]}\n"
        if not validar_peso[0]: errores += f"- {validar_peso[1]}\n"
        if not validar_contraseña[0]: errores += f"- {validar_contraseña[1]}"
        
        messagebox.showerror("Error de Validación", errores)


# --- INTERFAZ CLIENTE ---

# Frame contenedor para centrar el formulario
frame_centro = tk.Frame(cliente, bg="white")
frame_centro.pack(expand=True)

# Título
tk.Label(frame_centro, text="REGISTRO DE CLIENTE", font=("Helvetica", 18, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 30))

# Nombre
tk.Label(frame_centro, text="Nombre Completo:", bg="white", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
input_nombre = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_nombre.grid(row=1, column=1, sticky="w", padx=10)

# Rut
tk.Label(frame_centro, text="RUT:", bg="white", font=("Helvetica", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
input_rut = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_rut.grid(row=2, column=1, sticky="w", padx=10)

# Contraseña  ← NUEVO
tk.Label(frame_centro, text="Contraseña:", bg="white", font=("Helvetica", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
input_contraseña = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10), show="*")
input_contraseña.grid(row=3, column=1, sticky="w", padx=10)

# Fecha Nacimiento
tk.Label(frame_centro, text="Fecha de nacimiento:", bg="white", font=("Helvetica", 11)).grid(row=4, column=0, sticky="e", padx=10, pady=10)
input_fecha_nacimiento = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_fecha_nacimiento.grid(row=4, column=1, sticky="w", padx=10)
tk.Label(frame_centro, text="(DD-MM-AAAA)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=4, column=2, sticky="w")

# Estatura
tk.Label(frame_centro, text="Estatura (cm):", bg="white", font=("Helvetica", 11)).grid(row=5, column=0, sticky="e", padx=10, pady=10)
input_estatura = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_estatura.grid(row=5, column=1, sticky="w", padx=10)

# Peso
tk.Label(frame_centro, text="Peso (kg):", bg="white", font=("Helvetica", 11)).grid(row=6, column=0, sticky="e", padx=10, pady=10)
input_peso = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_peso.grid(row=6, column=1, sticky="w", padx=10)

# Botón
boton = ttk.Button(frame_centro, text='REGISTRAR CLIENTE', command=ingresar_usuario, style="TButton")
boton.grid(row=7, column=0, columnspan=2, pady=30, ipadx=10, ipady=5)

# --- INTERFAZ ENTRENADOR
frame_centro_ent = tk.Frame(entrenador, bg="white")
frame_centro_ent.pack(expand=True)


# --- INTERFAZ ADMIN ---
#frame_centro_adm = tk.Frame(administrador, bg="white")
#frame_centro_adm.pack(expand=True)
#tk.Label(frame_centro_adm, text="ADMINISTRACIÓN", font=("Helvetica", 18, "bold"), bg="white", fg="#333").pack(pady=20)


ventana.mainloop()