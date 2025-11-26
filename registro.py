import tkinter as tk
from tkinter import messagebox, ttk
import os, json
from validaciones import Validaciones 
from cliente import Cliente
from controlador import ControladorGUI
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

cliente_frame = tk.Frame(notebook, bg="white")
entrenador_frame = tk.Frame(notebook, bg="white")

notebook.add(cliente_frame, text="  Cliente  ")
notebook.add(entrenador_frame, text="  Entrenador  ")

controlador = ControladorGUI()
app_entrenador = AppEntrenador(entrenador_frame)

def ingresar_usuario():
    # ✅ ELIMINADO: input_apellido
    nombre = input_nombre.get().strip()
    rut = input_rut.get().strip()
    fecha_nacimiento = input_fecha_nacimiento.get().strip()
    estatura = input_estatura.get().strip()
    peso = input_peso.get().strip()
    
    validaciones = Validaciones()
    validar_nombre = validaciones.validar_nombre(nombre)
    validar_rut = validaciones.validar_rut(rut)  
    validar_fecha_nacimiento = validaciones.validar_fecha_nacimiento(fecha_nacimiento)
    validar_estatura = validaciones.validar_estatura(estatura)
    validar_peso = validaciones.validar_peso(peso)

    if validar_nombre[0] and validar_rut[0] and validar_fecha_nacimiento[0] and validar_estatura[0] and validar_peso[0]:
        try:
            # ✅ ELIMINADO: apellido del registro
            exito, mensaje = controlador.registrar_cliente(
                nombre=nombre,
                rut=rut,
                fecha_nacimiento=fecha_nacimiento,
                estatura=estatura,
                peso=peso
            )
            
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

frame_centro = tk.Frame(cliente_frame, bg="white")
frame_centro.pack(expand=True)

tk.Label(frame_centro, text="REGISTRO DE CLIENTE", font=("Helvetica", 18, "bold"), bg="white", fg="#333").grid(row=0, column=0, columnspan=2, pady=(0, 30))

# ✅ MODIFICADO: Solo "Nombre Completo"
tk.Label(frame_centro, text="Nombre Completo:", bg="white", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
input_nombre = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_nombre.grid(row=1, column=1, sticky="w", padx=10)

tk.Label(frame_centro, text="RUT:", bg="white", font=("Helvetica", 11)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
input_rut = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_rut.grid(row=2, column=1, sticky="w", padx=10)

tk.Label(frame_centro, text="Fecha de nacimiento:", bg="white", font=("Helvetica", 11)).grid(row=3, column=0, sticky="e", padx=10, pady=10)
input_fecha_nacimiento = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_fecha_nacimiento.grid(row=3, column=1, sticky="w", padx=10)
tk.Label(frame_centro, text="(DD-MM-AAAA)", bg="white", fg="gray", font=("Helvetica", 8)).grid(row=3, column=2, sticky="w")

tk.Label(frame_centro, text="Estatura (cm):", bg="white", font=("Helvetica", 11)).grid(row=4, column=0, sticky="e", padx=10, pady=10)
input_estatura = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_estatura.grid(row=4, column=1, sticky="w", padx=10)

tk.Label(frame_centro, text="Peso (kg):", bg="white", font=("Helvetica", 11)).grid(row=5, column=0, sticky="e", padx=10, pady=10)
input_peso = ttk.Entry(frame_centro, width=30, font=("Helvetica", 10))
input_peso.grid(row=5, column=1, sticky="w", padx=10)

boton = ttk.Button(frame_centro, text='REGISTRAR CLIENTE', command=ingresar_usuario, style="TButton")
boton.grid(row=6, column=0, columnspan=2, pady=30, ipadx=10, ipady=5)

ventana.mainloop()