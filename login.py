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
tk.Label(cliente,text="Login",font=900 ).pack(pady=20)

#Login entrenador
tk.Label(entrenador,text="Login").pack(pady=20)

#Login administrador
tk.Label(administrador,text="Login").pack(pady=20)
ventana.mainloop()