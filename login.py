import tkinter as tk  
from tkinter import messagebox, ttk 
import json  
import os 
from validaciones import Validaciones 
from gimnasio import Gimnasio 
from admin import AdminGimnasio  

# Inicializar gimnasio al abrir login (crea archivos JSON)
gimnasio = Gimnasio()  # Crea una instancia de la clase Gimnacio

# Función para cargar datos desde archivos JSON
def cargar_datos(archivo):
    # Verifica si el archivo existe
    if not os.path.exists(archivo):
        # Retorna lista vacía si el archivo no existe
        return []
    try:
        # Abre el archivo en modo lectura
        with open(archivo, "r", encoding="utf-8") as f:
            # Carga los datos desde el archivo JSON
            datos = json.load(f)
            # Retorna los datos si existen, sino lista vacía
            return datos if datos else []
    except:
        return []

# Función para verificar credenciales de login
def verificar_login(rut, contraseña, tipo):
    archivos = {
        "administrador": "administradores.json", 
        "cliente": "clientes.json", 
        "entrenador": "entrenadores.json" 
    }

    # Obtiene el archivo correspondiente al tipo de usuario
    archivo = archivos.get(tipo)
    # Carga los datos del archivo
    datos = cargar_datos(archivo)

    # Verifica si no hay datos en el archivo
    if not datos:
        return False, "No existen usuarios registrados"

    # Itera sobre cada usuario en los datos cargados
    for usuario in datos:
        print(f"Verificando usuario: {usuario.get('nombre', 'Sin nombre')}")  
        print(f"RUT en archivo: '{usuario.get('rut')}' vs RUT ingresado: '{rut}'") 
        print(f"Contraseña en archivo existe: {usuario.get('contraseña') is not None}")  

        if usuario.get("rut") == rut: 

            if "contraseña" not in usuario:  # Verifica si el usuario no tiene contraseña
                return False, "Usuario sin contraseña configurada. Por favor contacte al administrador."  # Retorna error
            
            # Verificar contraseña
            if usuario.get("contraseña") == contraseña:  # Compara contraseñas
                return True, usuario  # Retorna éxito y datos del usuario
            else:
                return False, "Contraseña incorrecta"  # Retorna error de contraseña
    
    return False, "Usuario no encontrado"  # Retorna error si no encuentra el usuario


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

    if not rut or not contraseña:  # Verifica si algún campo está vacío
        messagebox.showerror("Error", "Complete todos los campos") 
        return  

    existe, resultado = verificar_login(rut, contraseña, "cliente")  

    if existe:  
        # Limpiar campos
        input_cliente_rut.delete(0, tk.END)  # Limpia el campo RUT
        input_cliente_contraseña.delete(0, tk.END)  # Limpia el campo contraseña
        
        # Cerrar ventana de login
        ventana.destroy()  # Cierra la ventana de login
        
        # Abrir menú del cliente
        from menu_cliente import MenuCliente  # Importa la clase del menú del cliente
        
        ventana_cliente = tk.Tk()  
        ventana_cliente.title("Gimnasio Mr. Fat - Área Cliente")  
        ventana_cliente.geometry("700x600")  
        ventana_cliente.configure(bg="white")  
        frame_cliente = tk.Frame(ventana_cliente, bg="white") 
        frame_cliente.pack(expand=True, fill="both") 
        
        MenuCliente(frame_cliente, resultado) 
        
        ventana_cliente.mainloop()  # Inicia el loop principal de la ventana
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")  
        input_cliente_contraseña.delete(0, tk.END)  

tk.Button(tab_cliente, text="Ingresar", command=ingresar_cliente, width=20, height=2,fg="black").pack(pady=20)  # Crea botón de ingreso

#login entrenador
tab_entrenador = tk.Frame(notebook, bg="white")  # Crea frame para pestaña de entrenador
notebook.add(tab_entrenador, text="Entrenador")  # Añade pestaña al notebook

tk.Label(tab_entrenador, text="Login Entrenador", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)  # Crea etiqueta de título
tk.Label(tab_entrenador, text="RUT:", bg="white").pack()  # Crea etiqueta para RUT
input_entrenador_rut = tk.Entry(tab_entrenador, width=30)  # Crea campo de entrada para RUT
input_entrenador_rut.pack(pady=5)  # Empaqueta el campo de entrada

tk.Label(tab_entrenador, text="Contraseña:", bg="white").pack(pady=(10, 0))  # Crea etiqueta para contraseña
input_entrenador_contraseña = tk.Entry(tab_entrenador, width=30, show="*")  # Crea campo de entrada para contraseña
input_entrenador_contraseña.pack(pady=5)  # Empaqueta el campo de contraseña

def ingresar_entrenador():
    rut = input_entrenador_rut.get().strip()  # Obtiene y limpia el RUT ingresado
    contraseña = input_entrenador_contraseña.get().strip()  # Obtiene y limpia la contraseña ingresada

    if not rut or not contraseña:  # Verifica si algún campo está vacío
        messagebox.showerror("Error", "Complete todos los campos") 
        return 

    existe, resultado = verificar_login(rut, contraseña, "entrenador")  # Verifica las credenciales

    if existe:  # Si el login es exitoso
        # Limpiar campos
        input_entrenador_rut.delete(0, tk.END)  # Limpia el campo RUT
        input_entrenador_contraseña.delete(0, tk.END)  # Limpia el campo contraseña
        
        # Cerrar ventana de login
        ventana.destroy()  # Cierra la ventana de login
        
        # Abrir menú del entrenador
        from menu_entrenador import MenuEntrenador  # Importa la clase del menú del entrenador
        
        ventana_entrenador = tk.Tk()  # Crea nueva ventana para el entrenador
        ventana_entrenador.title("Gimnasio Mr. Fat - Área Entrenador")  # Establece título de la ventana
        ventana_entrenador.geometry("700x600")  # Define tamaño de la ventana
        ventana_entrenador.configure(bg="white")  # Establece color de fondo
        
        frame_entrenador = tk.Frame(ventana_entrenador, bg="white")  # Crea frame principal
        frame_entrenador.pack(expand=True, fill="both")  # Empaqueta el frame
        
        MenuEntrenador(frame_entrenador, resultado)  # Crea instancia del menú del entrenador
        
        ventana_entrenador.mainloop()  # Inicia el loop principal de la ventana
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")  # Muestra mensaje de error
        input_entrenador_contraseña.delete(0, tk.END)  # Limpia el campo contraseña

tk.Button(tab_entrenador, text="Ingresar", command=ingresar_entrenador, width=20, height=2, fg="black").pack(pady=20)  # Crea botón de ingreso

#login administrador
tab_admin = tk.Frame(notebook, bg="white")  # Crea frame para pestaña de administrador
notebook.add(tab_admin, text="Administrador")  # Añade pestaña al notebook

tk.Label(tab_admin, text="Login Administrador", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)  # Crea etiqueta de título
tk.Label(tab_admin, text="RUT:", bg="white").pack()  # Crea etiqueta para RUT
input_admin_rut = tk.Entry(tab_admin, width=30)  # Crea campo de entrada para RUT
input_admin_rut.pack(pady=5)  # Empaqueta el campo de entrada

tk.Label(tab_admin, text="Contraseña:", bg="white").pack(pady=(10, 0))  # Crea etiqueta para contraseña
input_admin_contraseña = tk.Entry(tab_admin, width=30, show="*")  # Crea campo de entrada para contraseña
input_admin_contraseña.pack(pady=5)  # Empaqueta el campo de contraseña

def ingresar_admin():
    rut = input_admin_rut.get().strip()  # Obtiene y limpia el RUT ingresado
    contraseña = input_admin_contraseña.get().strip()  # Obtiene y limpia la contraseña ingresada

    if not rut or not contraseña:  # Verifica si algún campo está vacío
        messagebox.showerror("Error", "Complete todos los campos")  # Muestra mensaje de error
        return  # Termina la función

    existe, resultado = verificar_login(rut, contraseña, "administrador")  # Verifica las credenciales

    if existe:  # Si el login es exitoso
        # Limpiar campos
        input_admin_rut.delete(0, tk.END)  # Limpia el campo RUT
        input_admin_contraseña.delete(0, tk.END)  # Limpia el campo contraseña
        
        ventana.destroy()  # Cierra la ventana de login
        
        ventana_admin = tk.Tk()  # Crea nueva ventana para el administrador
        ventana_admin.title("Gimnasio Mr. Fat - Panel Administrativo")  # Establece título de la ventana
        ventana_admin.geometry("700x600")  
        ventana_admin.configure(bg="white") 
        
        frame_admin = tk.Frame(ventana_admin, bg="white") 
        frame_admin.pack(expand=True, fill="both") 
        
        AdminGimnasio(frame_admin, resultado)  # Crea instancia del panel administrativo
        
        ventana_admin.mainloop()  
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")  
        input_admin_contraseña.delete(0, tk.END)  # Limpia el campo contraseña

tk.Button(tab_admin, text="Ingresar", command=ingresar_admin, width=20, height=2,fg="black").pack(pady=20)  # Crea botón de ingreso

ventana.mainloop() 