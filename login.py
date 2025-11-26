import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from validaciones import Validaciones
from gimnasio import Gimnacio
from admin import AdminGimnasio

# Inicializar gimnasio al abrir login (crea archivos JSON)
gimnasio = Gimnacio()

def cargar_datos(archivo):
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos if datos else []
    except:
        return []

def verificar_login(rut, contraseña, tipo):
    archivos = {
        "administrador": "administradores.json",
        "cliente": "clientes.json",
        "entrenador": "entrenadores.json"
    }

    archivo = archivos.get(tipo)
    datos = cargar_datos(archivo)

    if not datos:
        return False, "No existen usuarios registrados"

    for usuario in datos:
        # Debug: imprimir para ver qué hay en el archivo
        print(f"Verificando usuario: {usuario.get('nombre', 'Sin nombre')}")
        print(f"RUT en archivo: '{usuario.get('rut')}' vs RUT ingresado: '{rut}'")
        print(f"Contraseña en archivo existe: {usuario.get('contraseña') is not None}")
        
        # Verificar si el campo contraseña existe
        if usuario.get("rut") == rut:
            # Si no existe el campo contraseña en el JSON
            if "contraseña" not in usuario:
                return False, "Usuario sin contraseña configurada. Por favor contacte al administrador."
            
            # Verificar contraseña
            if usuario.get("contraseña") == contraseña:
                return True, usuario
            else:
                return False, "Contraseña incorrecta"
    
    return False, "Usuario no encontrado"


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Gimnasio Mr. Fat - Login")
ventana.geometry("500x400")
ventana.configure(bg="white")

# Crear notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

validaciones = Validaciones()

#login cliente
tab_cliente = tk.Frame(notebook, bg="white")
notebook.add(tab_cliente, text="Cliente")

tk.Label(tab_cliente, text="Login Cliente", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
tk.Label(tab_cliente, text="RUT:", bg="white").pack()
input_cliente_rut = tk.Entry(tab_cliente, width=30)
input_cliente_rut.pack(pady=5)

tk.Label(tab_cliente, text="Contraseña:", bg="white").pack(pady=(10, 0))
input_cliente_contraseña = tk.Entry(tab_cliente, width=30, show="*")
input_cliente_contraseña.pack(pady=5)

def ingresar_cliente():
    rut = input_cliente_rut.get().strip()
    contraseña = input_cliente_contraseña.get().strip()

    if not rut or not contraseña:
        messagebox.showerror("Error", "Complete todos los campos")
        return

    existe, resultado = verificar_login(rut, contraseña, "cliente")

    if existe:
        # Limpiar campos
        input_cliente_rut.delete(0, tk.END)
        input_cliente_contraseña.delete(0, tk.END)
        
        # Cerrar ventana de login
        ventana.destroy()
        
        # Abrir menú del cliente
        from menu_cliente import MenuCliente
        
        ventana_cliente = tk.Tk()
        ventana_cliente.title("Gimnasio Mr. Fat - Área Cliente")
        ventana_cliente.geometry("700x600")
        ventana_cliente.configure(bg="white")
        
        frame_cliente = tk.Frame(ventana_cliente, bg="white")
        frame_cliente.pack(expand=True, fill="both")
        
        MenuCliente(frame_cliente, resultado)
        
        ventana_cliente.mainloop()
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")
        input_cliente_contraseña.delete(0, tk.END)

tk.Button(tab_cliente, text="Ingresar", command=ingresar_cliente, width=20, height=2,fg="black").pack(pady=20)

#login entrenador
tab_entrenador = tk.Frame(notebook, bg="white")
notebook.add(tab_entrenador, text="Entrenador")

tk.Label(tab_entrenador, text="Login Entrenador", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
tk.Label(tab_entrenador, text="RUT:", bg="white").pack()
input_entrenador_rut = tk.Entry(tab_entrenador, width=30)
input_entrenador_rut.pack(pady=5)

tk.Label(tab_entrenador, text="Contraseña:", bg="white").pack(pady=(10, 0))
input_entrenador_contraseña = tk.Entry(tab_entrenador, width=30, show="*")
input_entrenador_contraseña.pack(pady=5)

def ingresar_entrenador():
    rut = input_entrenador_rut.get().strip()
    contraseña = input_entrenador_contraseña.get().strip()

    if not rut or not contraseña:
        messagebox.showerror("Error", "Complete todos los campos")
        return

    existe, resultado = verificar_login(rut, contraseña, "entrenador")

    if existe:
        # Limpiar campos
        input_entrenador_rut.delete(0, tk.END)
        input_entrenador_contraseña.delete(0, tk.END)
        
        # Cerrar ventana de login
        ventana.destroy()
        
        # Abrir menú del entrenador
        from menu_entrenador import MenuEntrenador
        
        ventana_entrenador = tk.Tk()
        ventana_entrenador.title("Gimnasio Mr. Fat - Área Entrenador")
        ventana_entrenador.geometry("700x600")
        ventana_entrenador.configure(bg="white")
        
        frame_entrenador = tk.Frame(ventana_entrenador, bg="white")
        frame_entrenador.pack(expand=True, fill="both")
        
        MenuEntrenador(frame_entrenador, resultado)
        
        ventana_entrenador.mainloop()
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")
        input_entrenador_contraseña.delete(0, tk.END)

tk.Button(tab_entrenador, text="Ingresar", command=ingresar_entrenador, width=20, height=2, fg="black").pack(pady=20)

#login administrador
tab_admin = tk.Frame(notebook, bg="white")
notebook.add(tab_admin, text="Administrador")

tk.Label(tab_admin, text="Login Administrador", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
tk.Label(tab_admin, text="RUT:", bg="white").pack()
input_admin_rut = tk.Entry(tab_admin, width=30)
input_admin_rut.pack(pady=5)

tk.Label(tab_admin, text="Contraseña:", bg="white").pack(pady=(10, 0))
input_admin_contraseña = tk.Entry(tab_admin, width=30, show="*")
input_admin_contraseña.pack(pady=5)

def ingresar_admin():
    rut = input_admin_rut.get().strip()
    contraseña = input_admin_contraseña.get().strip()

    if not rut or not contraseña:
        messagebox.showerror("Error", "Complete todos los campos")
        return

    existe, resultado = verificar_login(rut, contraseña, "administrador")

    if existe:
        # Limpiar campos
        input_admin_rut.delete(0, tk.END)
        input_admin_contraseña.delete(0, tk.END)
        
        ventana.destroy()
        
        ventana_admin = tk.Tk()
        ventana_admin.title("Gimnasio Mr. Fat - Panel Administrativo")
        ventana_admin.geometry("700x600")
        ventana_admin.configure(bg="white")
        
        frame_admin = tk.Frame(ventana_admin, bg="white")
        frame_admin.pack(expand=True, fill="both")
        
        AdminGimnasio(frame_admin, resultado)
        
        ventana_admin.mainloop()
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")
        input_admin_contraseña.delete(0, tk.END)

tk.Button(tab_admin, text="Ingresar", command=ingresar_admin, width=20, height=2,fg="black").pack(pady=20)

ventana.mainloop()