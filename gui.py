import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import subprocess
import sys

# IMPORTAR TU BACKEND
from gimnasio import Gimnacio 
from cliente import Cliente
from entrenador import Entrenador
from suscripcion import Suscripcion
from ejercicios import Ejercicio   
from historial_peso import HistorialPeso

class GymGUI:
    def __init__(self, root):
        self.gym = Gimnacio()
        self.root = root
        self.root.title("Sistema de Gestión - Gimnasio Python")
        self.root.geometry("1000x700")
        
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        
        # Crear el contenedor de pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        # --- PESTAÑAS ---
        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_entrenadores = ttk.Frame(self.notebook)
        self.frame_suscripciones = ttk.Frame(self.notebook)
        self.frame_ejercicios = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_clientes, text='Clientes')
        self.notebook.add(self.frame_entrenadores, text='Entrenadores')
        self.notebook.add(self.frame_suscripciones, text='Suscripciones')
        self.notebook.add(self.frame_ejercicios, text='Ejercicios')
        
        # Inicializar vistas
        self.init_tab_clientes()
        self.init_tab_entrenadores()
        
    # ==========================================
    # PESTAÑA CLIENTES
    # ==========================================
    def init_tab_clientes(self):
        # Frame izquierdo (Botones)
        frame_form = ttk.LabelFrame(self.frame_clientes, text="Acciones")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)
        
        # BOTÓN PARA ABRIR REGISTRO
        btn_add = ttk.Button(frame_form, text="Ir a Registrar Cliente", command=self.abrir_registro)
        btn_add.pack(fill="x", pady=10)
        
        btn_del = ttk.Button(frame_form, text="Eliminar Seleccionado", command=self.eliminar_cliente)
        btn_del.pack(fill="x", pady=5)
        
        btn_refresh = ttk.Button(frame_form, text="Actualizar Lista", command=self.cargar_tabla_clientes)
        btn_refresh.pack(fill="x", pady=5)
        
        # Frame derecho (Tabla)
        frame_table = ttk.Frame(self.frame_clientes)
        frame_table.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        cols = ("RUT", "Nombre", "Apellido", "Estado")
        self.tree_clientes = ttk.Treeview(frame_table, columns=cols, show='headings', height=20)
        
        # Configurar anchos de columnas
        self.tree_clientes.column("RUT", width=100)
        self.tree_clientes.column("Nombre", width=150)
        self.tree_clientes.column("Apellido", width=150)
        self.tree_clientes.column("Estado", width=100)
        
        for col in cols:
            self.tree_clientes.heading(col, text=col)
        
        self.tree_clientes.pack(fill="both", expand=True)
        
        # Cargar datos iniciales
        self.cargar_tabla_clientes()

    def abrir_registro(self):
        """Abre la ventana de registro.py"""
        try:
            subprocess.Popen([sys.executable, "registro.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir registro.py: {e}")

    def cargar_tabla_clientes(self):
        """Carga y recarga los clientes desde el backend"""
        # Limpiar tabla
        for i in self.tree_clientes.get_children():
            self.tree_clientes.delete(i)
        
        # DEBUG: Verificar si hay clientes
        print(f"Total de clientes en backend: {len(self.gym.clientes)}")
        print(f"Clientes: {self.gym.clientes}")
        
        # Llenar desde el backend
        if not self.gym.clientes:
            print("No hay clientes cargados")
        
        for c in self.gym.clientes:
            # Si c es un diccionario
            if isinstance(c, dict):
                self.tree_clientes.insert("", "end", values=(
                    c.get("rut", ""), 
                    c.get("nombre", ""), 
                    c.get("apellido", ""), 
                    "Activo"
                ))
            # Si c es un objeto Cliente
            else:
                self.tree_clientes.insert("", "end", values=(
                    c.rut, 
                    c.nombre, 
                    c.apellido, 
                    "Activo"
                ))

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista")
            return
        
        item = self.tree_clientes.item(selected)
        rut = item['values'][0]
        
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar cliente {rut}?")
        if confirm:
            exito, msg = self.gym.eliminar_cliente(str(rut))
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_tabla_clientes()
            else:
                messagebox.showerror("Error", msg)

    # ==========================================
    # PESTAÑA ENTRENADORES
    # ==========================================
    def init_tab_entrenadores(self):
        frame_top = ttk.Frame(self.frame_entrenadores)
        frame_top.pack(side="top", fill="x", padx=10, pady=10)
        
        ttk.Label(frame_top, text="Nombre Entrenador:").pack(side="left")
        self.entry_nom_ent = ttk.Entry(frame_top)
        self.entry_nom_ent.pack(side="left", padx=5)
        
        ttk.Button(frame_top, text="Registrar", command=self.agregar_entrenador).pack(side="left", padx=5)
        
        self.tree_entrenadores = ttk.Treeview(self.frame_entrenadores, columns=("RUT", "Nombre", "Especialidad"), show='headings')
        self.tree_entrenadores.heading("RUT", text="RUT")
        self.tree_entrenadores.heading("Nombre", text="Nombre")
        self.tree_entrenadores.heading("Especialidad", text="Especialidad")
        self.tree_entrenadores.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.cargar_tabla_entrenadores()

    def cargar_tabla_entrenadores(self):
        for i in self.tree_entrenadores.get_children():
            self.tree_entrenadores.delete(i)
        
        for e in self.gym.entrenadores:
            self.tree_entrenadores.insert("", "end", values=(e.get("rut"), e.get("nombre"), e.get("especialidad", "General")))

    def agregar_entrenador(self):
        nombre = self.entry_nom_ent.get()
        if nombre:
            nuevo_ent = Entrenador("1-9", nombre, "General") 
            exito, msg = self.gym.agregar_entrenador(nuevo_ent)
            if exito:
                self.cargar_tabla_entrenadores()
            else:
                messagebox.showerror("Error", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = GymGUI(root)
    root.mainloop()