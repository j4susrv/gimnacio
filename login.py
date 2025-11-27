# Importar módulos necesarios para la interfaz gráfica y funcionalidades
import tkinter as tk  # Importa tkinter para la interfaz gráfica
from tkinter import messagebox, ttk  # Importa messagebox para ventanas de mensaje y ttk para widgets temáticos
import json  # Importa módulo para trabajar con archivos JSON
import os  # Importa módulo para operaciones del sistema operativo
from validaciones import Validaciones  # Importa clase de validaciones personalizada
from gimnasio import Gimnacio  # Importa la clase principal del gimnasio
from admin import AdminGimnasio  # Importa la clase del administrador

# Inicializar gimnasio al abrir login (crea archivos JSON)
gimnasio = Gimnacio()  # Crea una instancia de la clase Gimnacio

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
    # Captura cualquier error durante la carga
    except:
        # Retorna lista vacía en caso de error
        return []

# Función para verificar credenciales de login
def verificar_login(rut, contraseña, tipo):
    # Diccionario que mapea tipos de usuario con sus archivos correspondientes
    archivos = {
        "administrador": "administradores.json",  # Archivo para administradores
        "cliente": "clientes.json",  # Archivo para clientes
        "entrenador": "entrenadores.json"  # Archivo para entrenadores
    }

    # Obtiene el archivo correspondiente al tipo de usuario
    archivo = archivos.get(tipo)
    # Carga los datos del archivo
    datos = cargar_datos(archivo)

    # Verifica si no hay datos en el archivo
    if not datos:
        # Retorna fallo si no hay usuarios registrados
        return False, "No existen usuarios registrados"

    # Itera sobre cada usuario en los datos cargados
    for usuario in datos:
        # Debug: imprimir para ver qué hay en el archivo
        print(f"Verificando usuario: {usuario.get('nombre', 'Sin nombre')}")  # Muestra nombre del usuario
        print(f"RUT en archivo: '{usuario.get('rut')}' vs RUT ingresado: '{rut}'")  # Compara RUTs
        print(f"Contraseña en archivo existe: {usuario.get('contraseña') is not None}")  # Verifica existencia de contraseña
        
        # Verificar si el campo contraseña existe
        if usuario.get("rut") == rut:  # Compara el RUT del usuario con el ingresado
            # Si no existe el campo contraseña en el JSON
            if "contraseña" not in usuario:  # Verifica si el usuario no tiene contraseña
                return False, "Usuario sin contraseña configurada. Por favor contacte al administrador."  # Retorna error
            
            # Verificar contraseña
            if usuario.get("contraseña") == contraseña:  # Compara contraseñas
                return True, usuario  # Retorna éxito y datos del usuario
            else:
                return False, "Contraseña incorrecta"  # Retorna error de contraseña
    
    return False, "Usuario no encontrado"  # Retorna error si no encuentra el usuario


# Crear ventana principal
ventana = tk.Tk()  # Crea la ventana principal de tkinter
ventana.title("Gimnasio Mr. Fat - Login")  # Establece el título de la ventana
ventana.geometry("500x400")  # Define el tamaño de la ventana
ventana.configure(bg="white")  # Establece el color de fondo blanco

# Crear notebook (pestañas)
notebook = ttk.Notebook(ventana)  # Crea un widget de pestañas
notebook.pack(expand=True, fill="both", padx=10, pady=10)  # Empaqueta el notebook en la ventana

validaciones = Validaciones()  # Crea una instancia de la clase Validaciones

#login cliente
tab_cliente = tk.Frame(notebook, bg="white")  # Crea un frame para la pestaña de cliente
notebook.add(tab_cliente, text="Cliente")  # Añade la pestaña al notebook

tk.Label(tab_cliente, text="Login Cliente", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)  # Crea etiqueta de título
tk.Label(tab_cliente, text="RUT:", bg="white").pack()  # Crea etiqueta para RUT
input_cliente_rut = tk.Entry(tab_cliente, width=30)  # Crea campo de entrada para RUT
input_cliente_rut.pack(pady=5)  # Empaqueta el campo de entrada

tk.Label(tab_cliente, text="Contraseña:", bg="white").pack(pady=(10, 0))  # Crea etiqueta para contraseña
input_cliente_contraseña = tk.Entry(tab_cliente, width=30, show="*")  # Crea campo de entrada para contraseña (oculta caracteres)
input_cliente_contraseña.pack(pady=5)  # Empaqueta el campo de contraseña

def ingresar_cliente():
    rut = input_cliente_rut.get().strip()  # Obtiene y limpia el RUT ingresado
    contraseña = input_cliente_contraseña.get().strip()  # Obtiene y limpia la contraseña ingresada

    if not rut or not contraseña:  # Verifica si algún campo está vacío
        messagebox.showerror("Error", "Complete todos los campos")  # Muestra mensaje de error
        return  # Termina la función

    existe, resultado = verificar_login(rut, contraseña, "cliente")  # Verifica las credenciales

    if existe:  # Si el login es exitoso
        # Limpiar campos
        input_cliente_rut.delete(0, tk.END)  # Limpia el campo RUT
        input_cliente_contraseña.delete(0, tk.END)  # Limpia el campo contraseña
        
        # Cerrar ventana de login
        ventana.destroy()  # Cierra la ventana de login
        
        # Abrir menú del cliente
        from menu_cliente import MenuCliente  # Importa la clase del menú del cliente
        
        ventana_cliente = tk.Tk()  # Crea nueva ventana para el cliente
        ventana_cliente.title("Gimnasio Mr. Fat - Área Cliente")  # Establece título de la ventana
        ventana_cliente.geometry("700x600")  # Define tamaño de la ventana
        ventana_cliente.configure(bg="white")  # Establece color de fondo
        
        frame_cliente = tk.Frame(ventana_cliente, bg="white")  # Crea frame principal
        frame_cliente.pack(expand=True, fill="both")  # Empaqueta el frame
        
        MenuCliente(frame_cliente, resultado)  # Crea instancia del menú del cliente
        
        ventana_cliente.mainloop()  # Inicia el loop principal de la ventana
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")  # Muestra mensaje de error
        input_cliente_contraseña.delete(0, tk.END)  # Limpia el campo contraseña

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
        messagebox.showerror("Error", "Complete todos los campos")  # Muestra mensaje de error
        return  # Termina la función

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
        ventana_admin.geometry("700x600")  # Define tamaño de la ventana
        ventana_admin.configure(bg="white")  # Establece color de fondo
        
        frame_admin = tk.Frame(ventana_admin, bg="white")  # Crea frame principal
        frame_admin.pack(expand=True, fill="both")  # Empaqueta el frame
        
        AdminGimnasio(frame_admin, resultado)  # Crea instancia del panel administrativo
        
        ventana_admin.mainloop()  # Inicia el loop principal de la ventana
    else:
        messagebox.showerror("Error", f"Error de acceso: {resultado}")  # Muestra mensaje de error
        input_admin_contraseña.delete(0, tk.END)  # Limpia el campo contraseña

tk.Button(tab_admin, text="Ingresar", command=ingresar_admin, width=20, height=2,fg="black").pack(pady=20)  # Crea botón de ingreso

ventana.mainloop()  # Inicia el loop principal de la aplicación