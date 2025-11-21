import tkinter as tk
from tkinter import messagebox,ttk
import os, json
from validaciones import Validaciones

ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("800x600")
ventana.configure(bg="white")

notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both")
cliente = tk.Frame(notebook)
entrenador = tk.Frame(notebook)
administrador = tk.Frame(notebook)

notebook.add(cliente,text="Cliente")
notebook.add(entrenador,text="Entrenador")
notebook.add(administrador,text="Administrador")

#Login cliente


tk.Label(cliente, text="Login", font=900).pack(pady=20)

# CREAR TODOS LOS INPUTS PRIMERO

tk.Label(cliente, text="Rut").pack(pady=10)
input_rut = tk.Entry(cliente)
input_rut.pack()

tk.Label(cliente, text="Contraseña").pack(pady=5)
input_contraseña = tk.Entry(cliente, show="*")
input_contraseña.pack()

def ingresar_usuario():
    rut = input_rut.get().strip()
    contraseña = input_contraseña.get().strip()

    validaciones = Validaciones()
    validar_rut = validaciones.validar_rut(rut)  
    validar_contraseña = validaciones.validar_contraseña(contraseña)

    print(f"RUT: {validar_rut}")
    print(f"Nombre: {validar_contraseña}")

    if validar_rut[0] and validar_contraseña[0] :
        print("\n Los datos son validos")
        print(f"  - {validar_rut[1]}")
        print(f"  - {validar_contraseña[1]}")

    else:
        print("\n Errores encontrados")
        if not validar_contraseña[0]:
            print(f"  - {validar_contraseña[1]}")
        if not validar_rut[0]:
            print(f"  - {validar_rut[1]}")

boton = tk.Button(cliente, text='Ingresar', command=ingresar_usuario)
boton.pack(pady=20)

#Login entrenador
tk.Label(entrenador,text="Login").pack(pady=20)

#Login administrador
tk.Label(administrador,text="Login").pack(pady=20)
ventana.mainloop()