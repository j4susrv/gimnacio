import tkinter as tk
from tkinter import messagebox, ttk
import os, json
import re
from validaciones import Validaciones 
from registro_entrenador import AppEntrenador
from cliente import Cliente
from gimnasio import Gimnasio

def cargar_entrenadores():
    """Carga entrenadores desde el JSON"""
    archivo = "entrenadores.json"
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def guardar_cliente(cliente_obj):
    archivo = "clientes.json"
    
    if not os.path.exists(archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
    
    with open(archivo, "r", encoding="utf-8") as f:
        clientes = json.load(f)
    
    clientes.append(cliente_obj.a_diccionario())
    
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

ventana = tk.Tk()
ventana.title("Sistema de Gestión - Gimnasio")
ventana.geometry("900x750")
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

# CREAR GIMNASIO Y PASARLO
gimnasio = Gimnasio()
app_entrenador = AppEntrenador(entrenador, gimnasio=gimnasio)

# logica
def ingresar_usuario():
    nombre = input_nombre.get().strip()
    rut = input_rut.get().strip()
    contraseña = input_contraseña.get().strip()
    fecha_nacimiento = input_fecha_nacimiento.get().strip()
    estatura = input_estatura.get().strip()
    peso = input_peso.get().strip()
    estado_civil = combo_estado_civil.get().strip()
    direccion = input_direccion.get().strip()
    entrenador_seleccionado = combo_entrenador.get().strip()

    # Obtener RUT del entrenador seleccionado
    entrenador_asignado = None
    if entrenador_seleccionado != "Ninguno":
        match = re.search(r'\(([^)]+)\)', entrenador_seleccionado)
        if match:
            entrenador_asignado = match.group(1)

    # Validación 1: Validar que el formato del RUT sea correcto
    validaciones = Validaciones()
    validar_rut_formato = validaciones.validar_rut(rut)
    if not validar_rut_formato[0]:
        messagebox.showerror("Error", validar_rut_formato[1])
        return
    
    # Validación 2: Validar que no esté duplicado en NINGUNO de los JSONs
    validar_rut_unico = validaciones.validar_rut_unico(rut)
    if not validar_rut_unico[0]:
        messagebox.showerror("Error", validar_rut_unico[1])
        return
    try:
        estatura_float = float(estatura)
        peso_float = float(peso)
    except ValueError:
        return False, "Deben ser valores validos"
    # Validar todos los campos usando la clase Cliente
    errores, advertencias = Cliente.validar_datos(
        nombre, fecha_nacimiento, estatura_float, peso_float, 
        estado_civil, direccion, contraseña
    )

    if errores:
        messagebox.showerror("Error de Validación", "\n".join(errores))
        return
    
    if advertencias:
        if not messagebox.askyesno("Advertencias", "\n".join(advertencias) + "\n\n¿Continuar con el registro?"):
            return

    # Crear objeto Cliente
    try:
        nuevo_cliente = Cliente(
            nombre=nombre,
            rut=rut,
            fecha_nacimiento=fecha_nacimiento,
            estatura=estatura_float,
            peso=peso_float,
            estado_civil=estado_civil,
            direccion=direccion,
            contraseña=contraseña,
            entrenador_asignado=entrenador_asignado
        )

        # Guardar usando el objeto completo
        guardar_cliente(nuevo_cliente)

        mensaje = f"Cliente {nombre} registrado correctamente"
        if entrenador_asignado:
            nombre_entrenador = entrenador_seleccionado.split(' (')[0]
            mensaje += f"\nEntrenador asignado: {nombre_entrenador}"
        
        messagebox.showinfo("Éxito", mensaje)
        
        # Limpiar formulario
        input_nombre.delete(0, tk.END)
        input_rut.delete(0, tk.END)
        input_contraseña.delete(0, tk.END)
        input_fecha_nacimiento.delete(0, tk.END)
        input_estatura.delete(0, tk.END)
        input_peso.delete(0, tk.END)
        combo_estado_civil.set('')
        input_direccion.delete(0, tk.END)
        combo_entrenador.set('Ninguno')

    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar cliente: {str(e)}")

# --- INTERFAZ CLIENTE ---

# Frame contenedor para centrar el formulario
frame_centro = tk.Frame(cliente, bg="white")
frame_centro.pack(expand=True)

# Título
tk.Label(frame_centro, text="REGISTRO DE CLIENTE", font=("Helvetica", 18, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Nombre
tk.Label(frame_centro, text="Nombre Completo:", bg="white", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=8)
input_nombre = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_nombre.grid(row=1, column=1, sticky="w", padx=10)

# Rut
tk.Label(frame_centro, text="RUT:", bg="white", font=("Helvetica", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=8)
input_rut = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_rut.grid(row=2, column=1, sticky="w", padx=10)

# Contraseña
tk.Label(frame_centro, text="Contraseña:", bg="white", font=("Helvetica", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=8)
input_contraseña = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10), show="*")
input_contraseña.grid(row=3, column=1, sticky="w", padx=10)

# Fecha Nacimiento
tk.Label(frame_centro, text="Fecha de nacimiento:", bg="white", font=("Helvetica", 11)).grid(row=4, column=0, sticky="e", padx=10, pady=8)
input_fecha_nacimiento = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_fecha_nacimiento.grid(row=4, column=1, sticky="w", padx=10)
tk.Label(frame_centro, text="(DD-MM-AAAA)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=4, column=2, sticky="w")

# Estatura
tk.Label(frame_centro, text="Estatura (cm):", bg="white", font=("Helvetica", 11)).grid(row=5, column=0, sticky="e", padx=10, pady=8)
input_estatura = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_estatura.grid(row=5, column=1, sticky="w", padx=10)

# Peso
tk.Label(frame_centro, text="Peso (kg):", bg="white", font=("Helvetica", 11)).grid(row=6, column=0, sticky="e", padx=10, pady=8)
input_peso = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_peso.grid(row=6, column=1, sticky="w", padx=10)

# Estado Civil
tk.Label(frame_centro, text="Estado Civil:", bg="white", font=("Helvetica", 11)).grid(row=7, column=0, sticky="e", padx=10, pady=8)
estados_civiles = ["soltero", "casado", "divorciado", "viudo", "conviviente"]
combo_estado_civil = ttk.Combobox(frame_centro, values=estados_civiles, width=28, font=("Helvetica", 10), state="readonly")
combo_estado_civil.grid(row=7, column=1, sticky="w", padx=10)

# Dirección
tk.Label(frame_centro, text="Dirección:", bg="white", font=("Helvetica", 11)).grid(row=8, column=0, sticky="e", padx=10, pady=8)
input_direccion = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_direccion.grid(row=8, column=1, sticky="w", padx=10)

# Entrenador Asignado
tk.Label(frame_centro, text="Entrenador Asignado:", bg="white", font=("Helvetica", 11)).grid(row=9, column=0, sticky="e", padx=10, pady=8)
combo_entrenador = ttk.Combobox(frame_centro, width=28, font=("Helvetica", 10), state="readonly")
combo_entrenador.grid(row=9, column=1, sticky="w", padx=10)

def actualizar_lista_entrenadores():
    """Actualiza el combobox con entrenadores disponibles"""
    entrenadores = cargar_entrenadores()
    opciones = ["Ninguno"]
    
    for entrenador in entrenadores:
        nombre = entrenador.get('nombre', '')
        rut = entrenador.get('rut', '')
        especialidades = ', '.join(entrenador.get('especialidades', []))
        opciones.append(f"{nombre} ({rut}) - {especialidades}")
    
    combo_entrenador['values'] = opciones
    combo_entrenador.set('Ninguno')

# Botón para actualizar
btn_actualizar = ttk.Button(frame_centro, text='Actualizar Lista', command=actualizar_lista_entrenadores)
btn_actualizar.grid(row=9, column=2, sticky="w", padx=5)

# Botón de registro
boton = ttk.Button(frame_centro, text='REGISTRAR CLIENTE', command=ingresar_usuario, style="TButton")
boton.grid(row=10, column=0, columnspan=2, pady=25, ipadx=10, ipady=5)

# Información sobre entrenadores
tk.Label(
    frame_centro, 
    text="Nota: Seleccione un entrenador de la lista. Use 'Actualizar Lista' si agregó nuevos entrenadores.", 
    bg="white", 
    font=("Helvetica", 9),
    fg="gray",
    wraplength=400
).grid(row=11, column=0, columnspan=3, pady=10)

# Cargar entrenadores al iniciar
actualizar_lista_entrenadores()

# --- INTERFAZ ENTRENADOR
frame_centro_ent = tk.Frame(entrenador, bg="white")
frame_centro_ent.pack(expand=True)

ventana.mainloop()