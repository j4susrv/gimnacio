import tkinter as tk
from tkinter import messagebox,ttk
import os, json
from validaciones import Validaciones

ventana = tk.Tk()
ventana.title("REGISTRO")
ventana.geometry("800x600")
ventana.configure(bg="white")

notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both")
cliente = tk.Frame(notebook)
entrenador = tk.Frame(notebook)
administrador = tk.Frame(notebook)

notebook.add(cliente,text="Cliente")
notebook.add(entrenador,text="Entrenador")

#Login cliente


tk.Label(cliente, text="REGISTRO", font=900).pack(pady=20)

# CREAR TODOS LOS INPUTS PRIMERO
tk.Label(cliente, text="nombre").pack(pady=5)
input_nombre = tk.Entry(cliente)
input_nombre.pack()

tk.Label(cliente, text="Rut").pack(pady=10)
input_rut = tk.Entry(cliente)
input_rut.pack()

tk.Label(cliente, text="Fecha de nacimiento:").pack(pady=10)
input_fecha_nacimiento = tk.Entry(cliente)
input_fecha_nacimiento.pack()

tk.Label(cliente,text="Estatura en centimetros").pack(pady=10)
input_estatura = tk.Entry(cliente)
input_estatura.pack()

tk.Label(cliente,text="Peso").pack(pady=10)
input_peso = tk.Entry(cliente)
input_peso.pack()

def ingresar_usuario():
    nombre = input_nombre.get().strip()
    rut = input_rut.get().strip()
    fecha_nacimiento = input_fecha_nacimiento.get().strip()
    estatura = input_estatura.get().strip()
    peso = input_peso.get().strip()

    validaciones = Validaciones()
    validar_nombre = validaciones.validar_nombre(nombre)
    validar_rut = validaciones.validar_rut(rut)  
    validar_fecha_nacimiento = validaciones.validar_fecha_nacimiento(fecha_nacimiento)
    validar_estatura  = validaciones.validar_estatura(estatura)
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

    else:
        print("\n Errores encontrados")
        if not validar_nombre[0]:
            print(f"  - {validar_nombre[1]}")
        if not validar_rut[0]:
            print(f"  - {validar_rut[1]}")
        if not validar_fecha_nacimiento[0]:
            print(f"  - {validar_fecha_nacimiento[1]}")
        if not validar_estatura[0]:
            print(f"  - {validar_estatura[1]}")
        if not validar_peso[0]:
            print(f"  - {validar_peso[1]}")

boton = tk.Button(cliente, text='Ingresar', command=ingresar_usuario)
boton.pack(pady=20)

#Regisstro entrenador
tk.Label(entrenador,text="REGISTRO").pack(pady=20)

#Registro administrador
tk.Label(administrador,text="REGISTRO").pack(pady=20)
ventana.mainloop()