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
ventana.state("zoomed")
ventana.configure(bg="white")  

# Crear notebook (pestañas)
notebook = ttk.Notebook(ventana)  
notebook.pack(expand=True, fill="both", padx=10, pady=10)  

validaciones = Validaciones() 

#login cliente
tab_cliente = tk.Frame(notebook, bg="white")  
notebook.add(tab_cliente, text="Cliente")  

# Frame centrado
frame_cliente_center = tk.Frame(tab_cliente, bg="white")
frame_cliente_center.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame_cliente_center, text="Login Cliente", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20) 
tk.Label(frame_cliente_center, text="RUT:", bg="white").pack() 
input_cliente_rut = tk.Entry(frame_cliente_center, width=30) 
input_cliente_rut.pack(pady=5)  

tk.Label(frame_cliente_center, text="Contraseña:", bg="white").pack(pady=(10, 0))  
input_cliente_contraseña = tk.Entry(frame_cliente_center, width=30, show="*") 
input_cliente_contraseña.pack(pady=5) 

def ingresar_cliente():
    rut = input_cliente_rut.get().strip() 
    contraseña = input_cliente_contraseña.get().strip() 

    if not rut or not contraseña:  # Verifica si algún campo está vacío
        messagebox.showerror("Error", "Complete todos los campos") 
        return  

    existe, resultado = verificar_login(rut, contraseña, "cliente")  

    if existe:  
        # Importar aquí para evitar referencias circulares
        from menu_cliente import MenuCliente
        
        # Limpiar la ventana
        for widget in ventana.winfo_children():
            widget.destroy()
        
        # Crear frame para el menú
        frame_cliente = tk.Frame(ventana, bg="white")
        frame_cliente.pack(fill="both", expand=True)
        
        # Inicializar menú del cliente
        MenuCliente(frame_cliente, resultado)
    else:
        messagebox.showerror("Error de login", resultado) 

tk.Button(frame_cliente_center, text="Ingresar", command=ingresar_cliente, width=20, height=2, fg="black").pack(pady=20)

#login entrenador
tab_entrenador = tk.Frame(notebook, bg="white")
notebook.add(tab_entrenador, text="Entrenador")

# Frame centrado
frame_entrenador_center = tk.Frame(tab_entrenador, bg="white")
frame_entrenador_center.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame_entrenador_center, text="Login Entrenador", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
tk.Label(frame_entrenador_center, text="RUT:", bg="white").pack()
input_entrenador_rut = tk.Entry(frame_entrenador_center, width=30)
input_entrenador_rut.pack(pady=5)

tk.Label(frame_entrenador_center, text="Contraseña:", bg="white").pack(pady=(10, 0))
input_entrenador_contraseña = tk.Entry(frame_entrenador_center, width=30, show="*")
input_entrenador_contraseña.pack(pady=5)

def ingresar_entrenador():
    rut = input_entrenador_rut.get().strip()
    contraseña = input_entrenador_contraseña.get().strip()

    if not rut or not contraseña:
        messagebox.showerror("Error", "Complete todos los campos")
        return

    existe, resultado = verificar_login(rut, contraseña, "entrenador")

    if existe:
        from menu_entrenador import MenuEntrenador
        
        # Limpiar la ventana
        for widget in ventana.winfo_children():
            widget.destroy()
        
        # Crear frame para el menú
        frame_entrenador = tk.Frame(ventana, bg="white")
        frame_entrenador.pack(fill="both", expand=True)
        
        # Inicializar menú del entrenador
        MenuEntrenador(frame_entrenador, resultado)
    else:
        messagebox.showerror("Error de login", resultado)

tk.Button(frame_entrenador_center, text="Ingresar", command=ingresar_entrenador, width=20, height=2, fg="black").pack(pady=20)

#login administrador
tab_admin = tk.Frame(notebook, bg="white")
notebook.add(tab_admin, text="Administrador")

# Frame centrado
frame_admin_center = tk.Frame(tab_admin, bg="white")
frame_admin_center.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame_admin_center, text="Login Administrador", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
tk.Label(frame_admin_center, text="RUT:", bg="white").pack()
input_admin_rut = tk.Entry(frame_admin_center, width=30)
input_admin_rut.pack(pady=5)

tk.Label(frame_admin_center, text="Contraseña:", bg="white").pack(pady=(10, 0))
input_admin_contraseña = tk.Entry(frame_admin_center, width=30, show="*")
input_admin_contraseña.pack(pady=5)

def ingresar_admin():
    rut = input_admin_rut.get().strip()
    contraseña = input_admin_contraseña.get().strip()

    if not rut or not contraseña:
        messagebox.showerror("Error", "Complete todos los campos")
        return

    existe, resultado = verificar_login(rut, contraseña, "administrador")

    if existe:
        # Limpiar la ventana
        for widget in ventana.winfo_children():
            widget.destroy()
        
        # Crear frame para el menú
        frame_admin = tk.Frame(ventana, bg="white")
        frame_admin.pack(fill="both", expand=True)
        
        # Inicializar menú del admin
        AdminGimnasio(frame_admin, resultado)
    else:
        messagebox.showerror("Error de login", resultado)

tk.Button(frame_admin_center, text="Ingresar", command=ingresar_admin, width=20, height=2, fg="black").pack(pady=20)

ventana.mainloop()