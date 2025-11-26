import tkinter as tk
from tkinter import messagebox, ttk
import os, json
from validaciones import Validaciones 
from cliente import Cliente
from entrenador import Entrenador
from registro_entrenador import AppEntrenador

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

# Función para guardar cliente en JSON
def guardar_cliente_json(cliente_obj):
    """Guarda el cliente en clientes.json"""
    archivo = "clientes.json"
    
    try:
        # Leer datos existentes
        if os.path.exists(archivo):
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        else:
            datos = []
        
        # Convertir cliente a diccionario y agregarlo
        cliente_dict = cliente_obj.a_diccionario()
        datos.append(cliente_dict)
        
        # Guardar en archivo
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        return True, "Cliente guardado exitosamente"
    except Exception as e:
        return False, f"Error al guardar: {str(e)}"

# logica
def ingresar_usuario():
    nombre = input_nombre.get().strip()
    rut = input_rut.get().strip()
    fecha_nacimiento = input_fecha_nacimiento.get().strip()
    estatura = input_estatura.get().strip()
    peso = input_peso.get().strip()
    
    # CAMPOS ADICIONALES (valores por defecto)
    estado_civil = "No especificado"
    direccion = "No especificada"

    validaciones = Validaciones()
    validar_nombre = validaciones.validar_nombre(nombre)
    validar_rut = validaciones.validar_rut(rut)  
    validar_fecha_nacimiento = validaciones.validar_fecha_nacimiento(fecha_nacimiento)
    validar_estatura = validaciones.validar_estatura(estatura)
    validar_peso = validaciones.validar_peso(peso)

    print(f"Nombre: {validar_nombre}")
    print(f"RUT: {validar_rut}")
    print(f"Fecha: {validar_fecha_nacimiento}")
    print(f"Estatura: {validar_estatura}")
    print(f"Peso: {validar_peso}")

    if validar_nombre[0] and validar_rut[0] and validar_fecha_nacimiento[0] and validar_estatura[0] and validar_peso[0]:
        print("\n Los datos son validos")
        print(f"  - {validar_nombre[1]}")
        print(f"  - {validar_rut[1]}")
        print(f"  - {validar_fecha_nacimiento[1]}")
        print(f"  - {validar_estatura[1]}")
        print(f"  - {validar_peso[1]}")
        
        try:
            # CREAR OBJETO CLIENTE Y GUARDARLO
            nuevo_cliente = Cliente(
                nombre=nombre,
                rut=rut,
                fecha_nacimiento=fecha_nacimiento,
                estatura=float(estatura),
                peso=float(peso),
                estado_civil=estado_civil,
                direccion=direccion
            )
            
            # Guardar en JSON
            exito, mensaje = guardar_cliente_json(nuevo_cliente)
            
            if exito:
                messagebox.showinfo("Éxito", f"{mensaje}\n\nCliente {nombre} registrado correctamente")
                # Limpiar campos
                input_nombre.delete(0, tk.END)
                input_rut.delete(0, tk.END)
                input_fecha_nacimiento.delete(0, tk.END)
                input_estatura.delete(0, tk.END)
                input_peso.delete(0, tk.END)
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error al crear cliente", f"Error: {str(e)}")
    else:
        print("\n Errores encontrados")
        errores = ""
        if not validar_nombre[0]: errores += f"- {validar_nombre[1]}\n"
        if not validar_rut[0]: errores += f"- {validar_rut[1]}\n"
        if not validar_fecha_nacimiento[0]: errores += f"- {validar_fecha_nacimiento[1]}\n"
        if not validar_estatura[0]: errores += f"- {validar_estatura[1]}\n"
        if not validar_peso[0]: errores += f"- {validar_peso[1]}\n"
        
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

# Fecha Nacimiento
tk.Label(frame_centro, text="Fecha de nacimiento:", bg="white", font=("Helvetica", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
input_fecha_nacimiento = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_fecha_nacimiento.grid(row=3, column=1, sticky="w", padx=10)
tk.Label(frame_centro, text="(DD-MM-AAAA)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=3, column=2, sticky="w")

# Estatura
tk.Label(frame_centro, text="Estatura (cm):", bg="white", font=("Helvetica", 11)).grid(row=4, column=0, sticky="e", padx=10, pady=10)
input_estatura = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_estatura.grid(row=4, column=1, sticky="w", padx=10)

# Peso
tk.Label(frame_centro, text="Peso (kg):", bg="white", font=("Helvetica", 11)).grid(row=5, column=0, sticky="e", padx=10, pady=10)
input_peso = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_peso.grid(row=5, column=1, sticky="w", padx=10)

# Botón
boton = ttk.Button(frame_centro, text='REGISTRAR CLIENTE', command=ingresar_usuario, style="TButton")
boton.grid(row=6, column=0, columnspan=2, pady=30, ipadx=10, ipady=5)


# --- INTERFAZ ENTRENADOR
frame_centro_ent = tk.Frame(entrenador, bg="white")
frame_centro_ent.pack(expand=True)


ventana.mainloop()