import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import subprocess
from validaciones import Validaciones

# =======================
# FUNCIONES DE LOGIN
# =======================

def cargar_datos(archivo):
    if not os.path.exists(archivo):
        print(f"Archivo no existe: {archivo}")
        return []  
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            print(f"Cargado {archivo}: {datos}")
            return datos if datos else []
    except json.JSONDecodeError as e:
        print(f"Error JSON en {archivo}: {e}")
        return []
    except Exception as e:
        print(f"Error general: {e}")
        return []  

def verificar_login(rut, contraseña, tipo):
    archivos = {
        "administrador": "administradores.json",
        "cliente": "clientes.json",
        "entrenador": "entrenadores.json"
    }

    archivo = archivos.get(tipo)
    print(f"Buscando archivo: {archivo}")

    datos = cargar_datos(archivo)

    if not datos:
        print(f"No hay datos en {archivo}")
        return False, "No existen"

    for usuario in datos:
        if usuario.get("rut") == rut and usuario.get("contraseña") == contraseña:
            print(f"Usuario encontrado: {usuario}")
            return True, usuario

    print("Usuario no encontrado")
    return False, "Incorrecto"



ventana = tk.Tk()
ventana.title("Gimnasio Mr. Fat - Login")
ventana.geometry("600x400")

notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

validaciones = Validaciones()

# LOGIN CLIENTE

tab_cliente = tk.Frame(notebook)
notebook.add(tab_cliente, text="Cliente")

tk.Label(tab_cliente, text="Login Cliente", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(tab_cliente, text="RUT:").pack()
input_cliente_rut = tk.Entry(tab_cliente, width=30)
input_cliente_rut.pack(pady=5)

tk.Label(tab_cliente, text="Contraseña:").pack()
input_cliente_contraseña = tk.Entry(tab_cliente, width=30, show="*")
input_cliente_contraseña.pack(pady=5)

def ingresar_cliente():
    rut = input_cliente_rut.get().strip()
    contraseña = input_cliente_contraseña.get().strip()

    valido_rut, msg_rut = validaciones.validar_rut(rut)
    valido_contraseña, msg_contraseña = validaciones.validar_contraseña(contraseña)

    if not valido_rut or not valido_contraseña:
        errores = []
        if not valido_rut: errores.append(msg_rut)
        if not valido_contraseña: errores.append(msg_contraseña)
        messagebox.showerror("Error", "\n".join(errores))
        return

    existe, resultado = verificar_login(rut, contraseña, "cliente")

    if existe:
        messagebox.showinfo("Éxito", f"Bienvenido {resultado.get('nombre', 'Cliente')}")
    else:
        if resultado == "No existen":
            messagebox.showerror("Error", "No existen clientes registrados")
        else:
            messagebox.showerror("Error", "RUT o contraseña incorrectos")
        input_cliente_contraseña.delete(0, tk.END)

tk.Button(tab_cliente, text="Ingresar", command=ingresar_cliente, width=30, height=2).pack(pady=20)



# LOGIN ENTRENADOR

tab_entrenador = tk.Frame(notebook)
notebook.add(tab_entrenador, text="Entrenador")

tk.Label(tab_entrenador, text="Login Entrenador", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(tab_entrenador, text="RUT:").pack()
input_entrenador_rut = tk.Entry(tab_entrenador, width=30)
input_entrenador_rut.pack(pady=5)

tk.Label(tab_entrenador, text="Contraseña:").pack()
input_entrenador_contraseña = tk.Entry(tab_entrenador, width=30, show="*")
input_entrenador_contraseña.pack(pady=5)

def ingresar_entrenador():
    rut = input_entrenador_rut.get().strip()
    contraseña = input_entrenador_contraseña.get().strip()

    valido_rut, msg_rut = validaciones.validar_rut(rut)
    valido_contraseña, msg_contraseña = validaciones.validar_contraseña(contraseña)

    if not valido_rut or not valido_contraseña:
        errores = []
        if not valido_rut: errores.append(msg_rut)
        if not valido_contraseña: errores.append(msg_contraseña)
        messagebox.showerror("Error", "\n".join(errores))
        return

    existe, resultado = verificar_login(rut, contraseña, "entrenador")

    if existe:
        messagebox.showinfo("Éxito", f"Bienvenido {resultado.get('nombre', 'Entrenador')}")
    else:
        if resultado == "No existen":
            messagebox.showerror("Error", "No existen entrenadores registrados")
        else:
            messagebox.showerror("Error", "RUT o contraseña incorrectos")
        input_entrenador_contraseña.delete(0, tk.END)

tk.Button(tab_entrenador, text="Ingresar", command=ingresar_entrenador, width=30, height=2).pack(pady=20)

# LOGIN ADMIN

tab_admin = tk.Frame(notebook)
notebook.add(tab_admin, text="Administrador")

tk.Label(tab_admin, text="Login Administrador", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(tab_admin, text="RUT:").pack()
input_admin_rut = tk.Entry(tab_admin, width=30)
input_admin_rut.pack(pady=5)

tk.Label(tab_admin, text="Contraseña:").pack()
input_admin_contraseña = tk.Entry(tab_admin, width=30, show="*")
input_admin_contraseña.pack(pady=5)

def ingresar_admin():
    rut = input_admin_rut.get().strip()
    contraseña = input_admin_contraseña.get().strip()

    valido_rut, msg_rut = validaciones.validar_rut(rut)
    valido_contraseña, msg_contraseña = validaciones.validar_contraseña(contraseña)

    if not valido_rut or not valido_contraseña:
        errores = []
        if not valido_rut: errores.append(msg_rut)
        if not valido_contraseña: errores.append(msg_contraseña)
        messagebox.showerror("Error", "\n".join(errores))
        return

    existe, resultado = verificar_login(rut, contraseña, "administrador")

    if existe:
        messagebox.showinfo("Éxito", f"Bienvenido {resultado.get('nombre', 'Administrador')}")
    else:
        if resultado == "No existen":
            messagebox.showerror("Error", "No existen administradores registrados")
        else:
            messagebox.showerror("Error", "RUT o contraseña incorrectos")
        input_admin_contraseña.delete(0, tk.END)

tk.Button(tab_admin, text="Ingresar", command=ingresar_admin, width=30, height=2).pack(pady=20)


ventana.mainloop()
