import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import subprocess
import sys

from gimnasio import Gimnacio 
from controlador import ControladorGUI
from suscripcion import Suscripcion
from historial_peso import HistorialPeso

class GymGUI:
    def __init__(self, root):
        self.controlador = ControladorGUI()
        self.root = root
        self.root.title("Sistema de Gestión - Gimnasio Python")
        self.root.geometry("1000x700")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("TLabel", font=("Helvetica", 10))
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')
        
        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_entrenadores = ttk.Frame(self.notebook)
        self.frame_suscripciones = ttk.Frame(self.notebook)
        self.frame_ejercicios = ttk.Frame(self.notebook)
        
        self.notebook.add(self.frame_clientes, text='Clientes')
        self.notebook.add(self.frame_entrenadores, text='Entrenadores')
        self.notebook.add(self.frame_suscripciones, text='Suscripciones')
        self.notebook.add(self.frame_ejercicios, text='Ejercicios')
        
        self.init_tab_clientes()
        self.init_tab_entrenadores()
        self.init_tab_suscripciones()
        self.init_tab_ejercicios()
        
        self.auto_refresh()
    
    def auto_refresh(self):
        """Auto-actualiza los datos cada 3 segundos."""
        self.cargar_tabla_clientes()
        self.cargar_tabla_entrenadores()
        self.cargar_tabla_suscripciones()
        self.root.after(3000, self.auto_refresh)
    
    # ==================== PESTAÑA CLIENTES ====================
    def init_tab_clientes(self):
        frame_form = ttk.LabelFrame(self.frame_clientes, text="Acciones")
        frame_form.pack(side="left", fill="y", padx=10, pady=10)
        
        btn_add = ttk.Button(frame_form, text="Ir a Registrar Cliente", command=self.abrir_registro)
        btn_add.pack(fill="x", pady=10)
        
        btn_edit = ttk.Button(frame_form, text="Editar Seleccionado", command=self.editar_cliente)
        btn_edit.pack(fill="x", pady=5)
        
        btn_peso = ttk.Button(frame_form, text="Registrar Pesaje", command=self.registrar_peso)
        btn_peso.pack(fill="x", pady=5)
        
        btn_progreso = ttk.Button(frame_form, text="Ver Progreso", command=self.ver_progreso_peso)
        btn_progreso.pack(fill="x", pady=5)
        
        btn_suscripcion = ttk.Button(frame_form, text="Renovar Suscripción", command=self.renovar_suscripcion)
        btn_suscripcion.pack(fill="x", pady=5)
        
        btn_del = ttk.Button(frame_form, text="Eliminar Seleccionado", command=self.eliminar_cliente)
        btn_del.pack(fill="x", pady=5)
        
        btn_refresh = ttk.Button(frame_form, text="Actualizar Lista", command=self.cargar_tabla_clientes)
        btn_refresh.pack(fill="x", pady=5)
        
        btn_backup = ttk.Button(frame_form, text="Hacer Backup", command=self.hacer_backup)
        btn_backup.pack(fill="x", pady=5)
        
        frame_table = ttk.Frame(self.frame_clientes)
        frame_table.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        cols = ("RUT", "Nombre", "IMC", "Peso (kg)", "Estado")
        self.tree_clientes = ttk.Treeview(frame_table, columns=cols, show='headings', height=20)
        
        self.tree_clientes.column("RUT", width=100)
        self.tree_clientes.column("Nombre", width=150)
        self.tree_clientes.column("IMC", width=80)
        self.tree_clientes.column("Peso (kg)", width=100)
        self.tree_clientes.column("Estado", width=100)
        
        for col in cols:
            self.tree_clientes.heading(col, text=col)
        
        self.tree_clientes.pack(fill="both", expand=True)
        
        self.cargar_tabla_clientes()

    def abrir_registro(self):
        """Abre registro.py como subproceso."""
        try:
            subprocess.Popen([sys.executable, "registro.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir registro.py: {e}")

    def cargar_tabla_clientes(self):
        """Carga clientes desde controlador."""
        try:
            for i in self.tree_clientes.get_children():
                self.tree_clientes.delete(i)
            
            clientes = self.controlador.obtener_clientes()
            
            if not clientes:
                print("📭 No hay clientes registrados")
                return
            
            for c in clientes:
                self.tree_clientes.insert("", "end", values=(
                    c.get("rut", ""), 
                    c.get("nombre", ""), 
                    c.get("imc", "N/A"),
                    c.get("peso", "N/A"),
                    c.get("categoria_imc", "N/A")
                ))
                
            print(f"✅ {len(clientes)} clientes cargados")
            
        except Exception as e:
            messagebox.showerror("Error al cargar", f"Error: {str(e)}")

    def editar_cliente(self):
        """Abre ventana para editar cliente seleccionado."""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista")
            return
        
        item = self.tree_clientes.item(selected)
        rut = item['values'][0]
        
        clientes = self.controlador.obtener_clientes()
        cliente_actual = None
        for c in clientes:
            if c.get("rut") == rut:
                cliente_actual = c
                break
        
        if not cliente_actual:
            messagebox.showerror("Error", "No se encontró el cliente")
            return
        
        self._abrir_ventana_editar(cliente_actual)
    
    def _abrir_ventana_editar(self, cliente):
        """Ventana modal para editar cliente."""
        ventana_edit = tk.Toplevel(self.root)
        ventana_edit.title(f"Editar Cliente - {cliente.get('nombre')}")
        ventana_edit.geometry("400x450")
        ventana_edit.transient(self.root)
        ventana_edit.grab_set()
        
        frame = tk.Frame(ventana_edit, bg="white")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(frame, text="Editar Cliente", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        
        tk.Label(frame, text="Nombre:", bg="white").pack(anchor="w", pady=(10, 0))
        entry_nombre = ttk.Entry(frame, width=30)
        entry_nombre.insert(0, cliente.get("nombre", ""))
        entry_nombre.pack(fill="x", pady=5)
        
        tk.Label(frame, text="Estatura (cm):", bg="white").pack(anchor="w", pady=(10, 0))
        entry_estatura = ttk.Entry(frame, width=30)
        entry_estatura.insert(0, str(cliente.get("estatura", "")))
        entry_estatura.pack(fill="x", pady=5)
        
        tk.Label(frame, text="Peso (kg):", bg="white").pack(anchor="w", pady=(10, 0))
        entry_peso = ttk.Entry(frame, width=30)
        entry_peso.insert(0, str(cliente.get("peso", "")))
        entry_peso.pack(fill="x", pady=5)
        
        tk.Label(frame, text="Dirección:", bg="white").pack(anchor="w", pady=(10, 0))
        entry_direccion = ttk.Entry(frame, width=30)
        entry_direccion.insert(0, cliente.get("direccion", ""))
        entry_direccion.pack(fill="x", pady=5)
        
        def guardar_cambios():
            try:
                from cliente import Cliente
                cliente_modificado = Cliente(
                    nombre=entry_nombre.get().strip(),
                    rut=cliente.get("rut"),
                    fecha_nacimiento=cliente.get("fecha_nacimiento"),
                    estatura=float(entry_estatura.get()),
                    peso=float(entry_peso.get()),
                    estado_civil=cliente.get("estado_civil", "No especificado"),
                    direccion=entry_direccion.get().strip()
                )
                
                exito, msg = self.controlador.gym.modificar_cliente(
                    cliente.get("rut"),
                    cliente_modificado
                )
                
                if exito:
                    messagebox.showinfo("Éxito", msg)
                    self.cargar_tabla_clientes()
                    ventana_edit.destroy()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        ttk.Button(frame, text="Guardar Cambios", command=guardar_cambios).pack(pady=20, ipadx=10, ipady=5)

    # ✅ NUEVO: Registrar Peso
    def registrar_peso(self):
        """Abre ventana para registrar peso del cliente seleccionado."""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista")
            return
        
        item = self.tree_clientes.item(selected)
        rut = item['values'][0]
        nombre_cliente = item['values'][1]
        
        # Validar que el cliente exista
        clientes = self.controlador.obtener_clientes()
        cliente_existe = False
        for c in clientes:
            if c.get("rut") == rut:
                cliente_existe = True
                break
        
        if not cliente_existe:
            messagebox.showerror("Error", "No se encontró el cliente")
            return
        
        self._abrir_ventana_peso(rut, nombre_cliente)
    
    def _abrir_ventana_peso(self, rut, nombre_cliente):
        """Ventana modal para registrar peso."""
        # ✅ MODIFICADO: Aumentado de 350x250 a 400x350
        ventana_peso = tk.Toplevel(self.root)
        ventana_peso.title(f"Registrar Peso - {nombre_cliente}")
        ventana_peso.geometry("400x350")
        ventana_peso.transient(self.root)
        ventana_peso.grab_set()
        
        frame = tk.Frame(ventana_peso, bg="white")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(frame, text="Registrar Pesaje", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text=f"Cliente: {nombre_cliente}", font=("Helvetica", 11, "italic"), bg="white", fg="#4a90e2").pack(pady=5)
        
        tk.Label(frame, text="Nuevo Peso (kg):", bg="white").pack(anchor="w", pady=(15, 0))
        entry_peso = ttk.Entry(frame, width=20)
        entry_peso.pack(fill="x", pady=5)
        
        tk.Label(frame, text="Fecha (YYYY-MM-DD):", bg="white").pack(anchor="w", pady=(10, 0))
        entry_fecha = ttk.Entry(frame, width=20)
        fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
        entry_fecha.insert(0, fecha_hoy)
        entry_fecha.pack(fill="x", pady=5)
        
        def guardar_peso():
            try:
                peso_nuevo = float(entry_peso.get().strip())
                fecha = entry_fecha.get().strip()
                
                # Validar peso
                if peso_nuevo <= 0:
                    messagebox.showerror("Error", "El peso debe ser un valor positivo")
                    return
                
                if peso_nuevo < 30 or peso_nuevo > 300:
                    respuesta = messagebox.askyesno("Advertencia", f"Peso inusual: {peso_nuevo} kg. ¿Continuar?")
                    if not respuesta:
                        return
                
                # Crear historial de peso
                historial = HistorialPeso(rut, peso_nuevo, fecha)
                
                # Registrar en backend
                exito, msg = self.controlador.gym.registrar_peso(historial)
                
                if exito:
                    messagebox.showinfo("Éxito", f"Peso registrado: {peso_nuevo} kg\n{msg}")
                    self.cargar_tabla_clientes()
                    ventana_peso.destroy()
                else:
                    messagebox.showerror("Error", msg)
            
            except ValueError:
                messagebox.showerror("Error", "El peso debe ser un número válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar peso: {str(e)}")
        
        # ✅ MODIFICADO: Aumentado padding vertical
        ttk.Button(frame, text="Registrar Peso", command=guardar_peso).pack(pady=25, ipadx=10, ipady=8)

    # ✅ NUEVO: Ver Progreso de Peso
    def ver_progreso_peso(self):
        """Muestra el progreso de peso del cliente seleccionado."""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista")
            return
        
        item = self.tree_clientes.item(selected)
        rut = item['values'][0]
        nombre_cliente = item['values'][1]
        
        try:
            progreso, msg = self.controlador.gym.calcular_progreso_peso(rut)
            
            if progreso is None:
                messagebox.showinfo("Información", f"Cliente: {nombre_cliente}\n\n{msg}")
                return
            
            # Formatear mensaje de progreso
            mensaje = f"""
PROGRESO DE PESO - {nombre_cliente}
{'='*40}

Peso Inicial:  {progreso['peso_inicial']} kg
Peso Actual:   {progreso['peso_actual']} kg
Cambio:        {progreso['diferencia']} kg

Estado:        {progreso['progreso']}
            """
            
            messagebox.showinfo("Progreso de Peso", mensaje)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular progreso: {str(e)}")

    # ✅ NUEVO: Renovar Suscripción
    def renovar_suscripcion(self):
        """Abre ventana para renovar suscripción del cliente seleccionado."""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista")
            return
        
        item = self.tree_clientes.item(selected)
        rut = item['values'][0]
        nombre_cliente = item['values'][1]
        
        # Validar que el cliente exista
        clientes = self.controlador.obtener_clientes()
        cliente_existe = False
        for c in clientes:
            if c.get("rut") == rut:
                cliente_existe = True
                break
        
        if not cliente_existe:
            messagebox.showerror("Error", "No se encontró el cliente")
            return
        
        self._abrir_ventana_suscripcion(rut, nombre_cliente)
    
    def _abrir_ventana_suscripcion(self, rut, nombre_cliente):
        """Ventana modal para renovar suscripción."""
        # ✅ MODIFICADO: Aumentado de 400x300 a 450x450
        ventana_sus = tk.Toplevel(self.root)
        ventana_sus.title(f"Renovar Suscripción - {nombre_cliente}")
        ventana_sus.geometry("450x450")
        ventana_sus.transient(self.root)
        ventana_sus.grab_set()
        
        frame = tk.Frame(ventana_sus, bg="white")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        tk.Label(frame, text="Renovar Suscripción", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
        tk.Label(frame, text=f"Cliente: {nombre_cliente}", font=("Helvetica", 11, "italic"), bg="white", fg="#4a90e2").pack(pady=5)
        
        tk.Label(frame, text="Selecciona Plan:", bg="white", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        
        # Combobox para seleccionar tipo de suscripción
        tipos_suscripcion = ["Mensual", "Trimestral", "Semestral", "Anual"]
        combo_tipo = ttk.Combobox(frame, values=tipos_suscripcion, state="readonly", width=20)
        combo_tipo.set("Mensual")
        combo_tipo.pack(fill="x", pady=5)
        
        # Precios (puedes personalizarlos)
        precios = {
            "Mensual": 50.00,
            "Trimestral": 140.00,
            "Semestral": 270.00,
            "Anual": 500.00
        }
        
        # ✅ NUEVO: Información de duración
        tk.Label(frame, text="Duración del Plan:", bg="white", font=("Helvetica", 10, "italic"), fg="#666").pack(anchor="w", pady=(10, 0))
        label_duracion = tk.Label(frame, text="30 días", bg="white", font=("Helvetica", 10))
        label_duracion.pack(anchor="w", pady=0)
        
        duraciones = {
            "Mensual": "30 días",
            "Trimestral": "90 días (3 meses)",
            "Semestral": "180 días (6 meses)",
            "Anual": "365 días (12 meses)"
        }
        
        tk.Label(frame, text="Monto (CLP):", bg="white").pack(anchor="w", pady=(15, 0))
        entry_monto = ttk.Entry(frame, width=20)
        entry_monto.insert(0, "50.00")
        entry_monto.pack(fill="x", pady=5)
        
        def actualizar_monto(event=None):
            """Actualiza el monto según el tipo seleccionado."""
            tipo = combo_tipo.get()
            if tipo in precios:
                entry_monto.delete(0, tk.END)
                entry_monto.insert(0, str(precios[tipo]))
                label_duracion.config(text=duraciones.get(tipo, ""))
        
        combo_tipo.bind("<<ComboboxSelected>>", actualizar_monto)
        
        def guardar_suscripcion():
            try:
                tipo = combo_tipo.get().lower()
                monto = float(entry_monto.get().strip())
                
                if not tipo:
                    messagebox.showerror("Error", "Selecciona un tipo de suscripción")
                    return
                
                if monto <= 0:
                    messagebox.showerror("Error", "El monto debe ser positivo")
                    return
                
                # Llamar método de renovación
                exito, msg = self.controlador.gym.renovar_suscripcion(rut, tipo, monto)
                
                if exito:
                    messagebox.showinfo("Éxito", f"Suscripción renovada:\n{msg}")
                    self.cargar_tabla_clientes()
                    self.cargar_tabla_suscripciones()
                    ventana_sus.destroy()
                else:
                    messagebox.showerror("Error", msg)
            
            except ValueError:
                messagebox.showerror("Error", "El monto debe ser un número válido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al renovar: {str(e)}")
        
        # ✅ MODIFICADO: Aumentado padding vertical
        ttk.Button(frame, text="Confirmar Renovación", command=guardar_suscripcion).pack(pady=25, ipadx=10, ipady=8)

    def eliminar_cliente(self):
        """Elimina cliente seleccionado."""
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Selecciona un cliente de la lista")
            return
        
        item = self.tree_clientes.item(selected)
        rut = item['values'][0]
        
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar cliente {rut}?")
        if confirm:
            try:
                exito, msg = self.controlador.eliminar_cliente(str(rut))
                if exito:
                    messagebox.showinfo("Éxito", msg)
                    self.cargar_tabla_clientes()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def hacer_backup(self):
        """Crea backup de todos los datos."""
        try:
            exito, msg = self.controlador.hacer_backup()
            if exito:
                messagebox.showinfo("Backup", msg)
            else:
                messagebox.showerror("Error", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Error en backup: {str(e)}")

    # ==================== PESTAÑA ENTRENADORES ====================
    def init_tab_entrenadores(self):
        frame_top = ttk.Frame(self.frame_entrenadores)
        frame_top.pack(side="top", fill="x", padx=10, pady=10)
        
        ttk.Label(frame_top, text="Gestión de Entrenadores:").pack(side="left")
        ttk.Button(frame_top, text="Abrir Registro", command=self.abrir_registro_ent).pack(side="left", padx=5)
        
        frame_table = ttk.Frame(self.frame_entrenadores)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_entrenadores = ttk.Treeview(frame_table, columns=("RUT", "Nombre", "Especialidad"), show='headings', height=20)
        self.tree_entrenadores.heading("RUT", text="RUT")
        self.tree_entrenadores.heading("Nombre", text="Nombre")
        self.tree_entrenadores.heading("Especialidad", text="Especialidad")
        
        self.tree_entrenadores.column("RUT", width=120)
        self.tree_entrenadores.column("Nombre", width=200)
        self.tree_entrenadores.column("Especialidad", width=250)
        
        self.tree_entrenadores.pack(fill="both", expand=True)
        
        self.cargar_tabla_entrenadores()
    
    def abrir_registro_ent(self):
        """Abre registro de entrenadores."""
        try:
            subprocess.Popen([sys.executable, "registro.py"])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir registro: {e}")

    def cargar_tabla_entrenadores(self):
        """Carga entrenadores desde controlador."""
        try:
            for i in self.tree_entrenadores.get_children():
                self.tree_entrenadores.delete(i)
            
            entrenadores = self.controlador.obtener_entrenadores()
            
            for e in entrenadores:
                esp = ", ".join(e.get("especialidades", ["General"]))[:40]
                self.tree_entrenadores.insert("", "end", values=(
                    e.get("rut", ""), 
                    e.get("nombre", ""), 
                    esp
                ))
        except Exception as e:
            messagebox.showerror("Error al cargar", f"Error: {str(e)}")

    # ==================== PESTAÑA SUSCRIPCIONES ====================
    def init_tab_suscripciones(self):
        """Inicializa la pestaña de suscripciones."""
        frame_top = ttk.Frame(self.frame_suscripciones)
        frame_top.pack(side="top", fill="x", padx=10, pady=10)
        
        ttk.Label(frame_top, text="Gestión de Suscripciones:").pack(side="left")
        ttk.Button(frame_top, text="Actualizar", command=self.cargar_tabla_suscripciones).pack(side="left", padx=5)
        
        frame_table = ttk.Frame(self.frame_suscripciones)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        cols = ("RUT Cliente", "Tipo", "Fecha Inicio", "Fecha Fin", "Días Restantes", "Activa")
        self.tree_suscripciones = ttk.Treeview(frame_table, columns=cols, show='headings', height=20)
        
        for col in cols:
            self.tree_suscripciones.heading(col, text=col)
        
        self.tree_suscripciones.column("RUT Cliente", width=120)
        self.tree_suscripciones.column("Tipo", width=100)
        self.tree_suscripciones.column("Fecha Inicio", width=120)
        self.tree_suscripciones.column("Fecha Fin", width=120)
        self.tree_suscripciones.column("Días Restantes", width=130)
        self.tree_suscripciones.column("Activa", width=80)
        
        self.tree_suscripciones.pack(fill="both", expand=True)
        
        self.cargar_tabla_suscripciones()
    
    def cargar_tabla_suscripciones(self):
        """Carga suscripciones desde el backend."""
        try:
            for i in self.tree_suscripciones.get_children():
                self.tree_suscripciones.delete(i)
            
            # Recargar datos
            self.controlador.gym.cargar_datos()
            suscripciones = self.controlador.gym.suscripciones
            
            if not suscripciones:
                print("📭 No hay suscripciones registradas")
                return
            
            for sus in suscripciones:
                estado = "✅ Activa" if sus.get("activa", False) else "❌ Vencida"
                self.tree_suscripciones.insert("", "end", values=(
                    sus.get("rut_cliente", ""),
                    sus.get("tipo_suscripcion", "").capitalize(),
                    sus.get("fecha_inicio", ""),
                    sus.get("fecha_fin", ""),
                    sus.get("dias_restantes", "0"),
                    estado
                ))
            
            print(f"✅ {len(suscripciones)} suscripciones cargadas")
        
        except Exception as e:
            messagebox.showerror("Error al cargar", f"Error: {str(e)}")

    # ==================== PESTAÑA EJERCICIOS ====================
    def init_tab_ejercicios(self):
        """Inicializa la pestaña de ejercicios (vacía por ahora)."""
        frame_top = ttk.Frame(self.frame_ejercicios)
        frame_top.pack(side="top", fill="x", padx=10, pady=10)
        
        ttk.Label(frame_top, text="Gestión de Ejercicios").pack(side="left")
        
        ttk.Button(frame_top, text="Actualizar", command=self.cargar_tabla_ejercicios).pack(side="left", padx=5)
        
        frame_table = ttk.Frame(self.frame_ejercicios)
        frame_table.pack(fill="both", expand=True, padx=10, pady=10)
        
        cols = ("Ejercicio", "Tipo", "Entrenador", "Duración (min)", "Fecha")
        self.tree_ejercicios = ttk.Treeview(frame_table, columns=cols, show='headings', height=20)
        
        for col in cols:
            self.tree_ejercicios.heading(col, text=col)
        
        self.tree_ejercicios.column("Ejercicio", width=150)
        self.tree_ejercicios.column("Tipo", width=120)
        self.tree_ejercicios.column("Entrenador", width=150)
        self.tree_ejercicios.column("Duración (min)", width=130)
        self.tree_ejercicios.column("Fecha", width=120)
        
        self.tree_ejercicios.pack(fill="both", expand=True)
        
        self.cargar_tabla_ejercicios()
    
    def cargar_tabla_ejercicios(self):
        """Carga ejercicios desde el backend."""
        try:
            for i in self.tree_ejercicios.get_children():
                self.tree_ejercicios.delete(i)
            
            self.controlador.gym.cargar_datos()
            ejercicios = self.controlador.gym.ejercicios
            
            if not ejercicios:
                print("📭 No hay ejercicios registrados")
                return
            
            for ej in ejercicios:
                self.tree_ejercicios.insert("", "end", values=(
                    ej.get("nombre_ejercicio", ""),
                    ej.get("tipo_ejercicio", "").capitalize(),
                    ej.get("nombre_entrenador", ""),
                    ej.get("duracion_minutos", ""),
                    ej.get("fecha", "")
                ))
            
            print(f"✅ {len(ejercicios)} ejercicios cargados")
        
        except Exception as e:
            messagebox.showerror("Error al cargar", f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GymGUI(root)
    root.mainloop()