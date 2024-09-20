import tkinter as tk
from tkinter import ttk, messagebox
from model.jubilados_dao import crear_tabla, borrar_tabla, jubilado, guardar, listar, editar, eliminar
import sqlite3

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=800, height=600)
        self.root = root
        self.pack()
        self.config(bg='white')
        self.id_jubilados = None

        self.Datos_persona()
        self.desabilitar_button()
        self.tabla_control()

        # Menú
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu_inicio = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Inicio", menu=self.menu_inicio)
        self.menu_inicio.add_command(label="Crear un Registro en BD", command=crear_tabla)
        self.menu_inicio.add_command(label="Eliminar un Registro en BD", command=borrar_tabla)
        self.menu_inicio.add_command(label="Salir", command=self.root.destroy)

        self.menu_ventanas = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ventanas", menu=self.menu_ventanas)
        self.menu_ventanas.add_command(label="Abrir Ventana de Consultas", command=self.abrir_ventana_consultas)

    def Datos_persona(self):
        # Labels de los datos
        labels = ["Ficha: ", "Nombre: ", "Fecha Jubilado: ", "Correo Elec.: ", "Dirección: ", "Num. Celular: ", "Fecha Certificación: ", "Lugar: ", "Status: "]
        for i, text in enumerate(labels):
            tk.Label(self, text=text, font=("Arial", 11, "bold")).grid(row=i, column=0, padx=10, pady=10)

        # Entrys de los datos
        self.entries = {}
        for i, label in enumerate(labels):
            self.entries[label] = tk.Entry(self, width=50, font=("Arial", 11))
            self.entries[label].grid(row=i, column=1, padx=10, pady=10, columnspan=2)

        # Botones
        self.boton_nuevo = tk.Button(self, text="Nuevo", command=self.habilitar_button, width=50, font=("Arial", 11, "bold"), fg="#DAD5D6", bg="#158645", cursor="hand2", activebackground="#35BD6F")
        self.boton_nuevo.grid(row=9, column=0, padx=5, pady=5)

        self.boton_guardar = tk.Button(self, text="Guardar", command=self.guardar_datos, width=50, font=("Arial", 11, "bold"), fg="#DAD5D6", bg="#1658A2", cursor="hand2", activebackground="#3586DF")
        self.boton_guardar.grid(row=9, column=1, padx=5, pady=5)

        self.boton_cancelar = tk.Button(self, text="Cancelar", command=self.desabilitar_button, width=50, font=("Arial", 11, "bold"), fg="#DAD5D6", bg="#BD152E", cursor="hand2", activebackground="#E15370")
        self.boton_cancelar.grid(row=9, column=2, padx=5, pady=5)

    def habilitar_button(self):
        for entry in self.entries.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)

        self.boton_guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

    def desabilitar_button(self):
        self.id_jubilados = None
        for entry in self.entries.values():
            entry.config(state="disabled")

        self.boton_guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")

    def guardar_datos(self):
        jubilados = jubilado(
            self.entries["Ficha: "].get(),
            self.entries["Nombre: "].get(),
            self.entries["Fecha Jubilado: "].get(),
            self.entries["Correo Elec.: "].get(),
            self.entries["Dirección: "].get(),
            self.entries["Num. Celular: "].get(),
            self.entries["Fecha Certificación: "].get(),
            self.entries["Lugar: "].get(),
            self.entries["Status: "].get(),
        )

        if self.id_jubilados is None:
            guardar(jubilados)
        else:
            editar(jubilados, self.id_jubilados)

        self.tabla_control()
        self.desabilitar_button()

    def tabla_control(self):
        # Mostrar lista en tabla
        self.lista_jubilados = listar()
        self.lista_jubilados.reverse()

        self.tabla = ttk.Treeview(self, columns=("Ficha", "Nombre", "fj", "ce", "direc", "tel", "fc", "lug", "status"), height=8)
        self.tabla.grid(row=12, column=0, columnspan=5, sticky="nsew")

        self.scrollv = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.scrollv.grid(row=12, column=11, sticky="nse")
        self.tabla.configure(yscrollcommand=self.scrollv.set)

        self.tabla.heading("#0", text="ID")
        self.tabla.heading("#1", text="Ficha")
        self.tabla.heading("#2", text="Nombre")
        self.tabla.heading("#3", text="Fecha Jubilacion")
        self.tabla.heading("#4", text="Correo Electronico")
        self.tabla.heading("#5", text="Dirección")
        self.tabla.heading("#6", text="Telefono")
        self.tabla.heading("#7", text="Fecha Certificado")
        self.tabla.heading("#8", text="Lugar")
        self.tabla.heading("#9", text="status")

        for p in self.lista_jubilados:
            self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9]))

        # Botón de editar
        self.boton_editar = tk.Button(self, text="Editar", command=self.editar_datos, width=50, font=("Arial", 11, "bold"), fg="#DAD5D6", bg="#158645", cursor="hand2", activebackground="#35BD6F")
        self.boton_editar.grid(row=14, column=0, padx=5, pady=5)

        # Botón de eliminar
        self.boton_eliminar = tk.Button(self, text="Eliminar", command=self.eliminar_datos, width=50, font=("Arial", 11, "bold"), fg="#DAD5D6", bg="#BD152E", cursor="hand2", activebackground="#E15370")
        self.boton_eliminar.grid(row=14, column=1, padx=5, pady=5)

    def editar_datos(self):
        try:
            self.id_jubilados = self.tabla.item(self.tabla.selection())["text"]
            values = self.tabla.item(self.tabla.selection())['values']
            for i, key in enumerate(self.entries.keys()):
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, values[i])
            self.habilitar_button()
        except:
            titulo = 'Edición de datos'
            mensaje = 'No ha seleccionado ningún registro'
            messagebox.showerror(titulo, mensaje)

    def eliminar_datos(self):
        try:
            self.id_jubilados = self.tabla.item(self.tabla.selection())["text"]
            eliminar(self.id_jubilados)
            self.tabla_control()
            self.id_jubilados = None
        except:
            titulo = 'Eliminar un registro'
            mensaje = 'No ha seleccionado ningún registro'
            messagebox.showerror(titulo, mensaje)

    def abrir_ventana_consultas(self):
        """Abre una nueva ventana para consultas."""
        ventana = tk.Toplevel(self.root)
        ventana.title("Ventana de Consultas")
        VentanaConsultas(ventana)

class ConexionDB:
    def __init__(self):
        self.base_datos = 'control_de_Jubilados/database/jubilados.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

class VentanaConsultas:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Jubilados")

        # Menú principal
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ventanas", menu=self.menu)
        self.menu.add_command(label="Abrir Ventana de Consultas", command=self.abrir_ventana_consultas)

        # Crear las pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Pestañas
        self.tab_consulta = ttk.Frame(self.notebook)
        self.tab_reporte = ttk.Frame(self.notebook)

        # Añadir pestañas al notebook
        self.notebook.add(self.tab_consulta, text="Consultas")
        self.notebook.add(self.tab_reporte, text="Reporte General")

        # Crear el contenido de las pestañas
        self.create_consulta_tab()
        self.create_reporte_tab()

        # Tabla para mostrar los resultados
        self.create_treeview()

    def create_treeview(self):
        """Crea un Treeview para mostrar los resultados."""
        self.tree = ttk.Treeview(self.root, columns=("ficha", "nombre", "fecha_jubilacion", "correo", "direccion", "telefono", "fecha_certificacion", "lugar", "status"), show="headings")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

        # Definir los encabezados de las columnas
        self.tree.heading("ficha", text="Ficha")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("fecha_jubilacion", text="Fecha Jubilación")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("direccion", text="Dirección")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("fecha_certificacion", text="Fecha Certificación")
        self.tree.heading("lugar", text="Lugar")
        self.tree.heading("status", text="Status")

        # Definir el ancho de las columnas
        for col in self.tree["columns"]:
            self.tree.column(col, width=120)

    def create_consulta_tab(self):
        """Pestaña para consultas por fecha de certificación y status general."""
        # Etiqueta y campo para ingresar fecha de certificación
        ttk.Label(self.tab_consulta, text="Fecha de Certificación (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_fecha = ttk.Entry(self.tab_consulta)
        self.entry_fecha.grid(row=0, column=1, padx=10, pady=10)

        # Botón de consulta por fecha de certificación
        ttk.Button(self.tab_consulta, text="Buscar por Fecha", command=self.buscar_por_fecha).grid(row=1, column=0, columnspan=2, pady=10)

        # Etiqueta y campo para status
        ttk.Label(self.tab_consulta, text="Status:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_status = ttk.Entry(self.tab_consulta)
        self.entry_status.grid(row=2, column=1, padx=10, pady=10)

        # Botón de consulta por status
        ttk.Button(self.tab_consulta, text="Buscar por Status", command=self.buscar_por_status).grid(row=3, column=0, columnspan=2, pady=10)

    def create_reporte_tab(self):
        """Pestaña para reporte general de status."""
        ttk.Button(self.tab_reporte, text="Generar Reporte General", command=self.generar_reporte_general).pack(pady=20)

    def limpiar_tabla(self):
        """Limpia los datos actuales de la tabla antes de mostrar nuevos resultados."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insertar_en_tabla(self, filas):
        """Inserta los datos obtenidos de la consulta en la tabla."""
        for fila in filas:
            self.tree.insert("", tk.END, values=fila)

    def buscar_por_fecha(self):
        """Consulta por fecha de certificación."""
        fecha_cert = self.entry_fecha.get()

        if fecha_cert:
            try:
                db = ConexionDB()
                db.cursor.execute("SELECT * FROM jubilados WHERE fc_jubilados = ?", (fecha_cert,))
                resultados = db.cursor.fetchall()
                
                if resultados:
                    self.limpiar_tabla()
                    self.insertar_en_tabla(resultados)
                else:
                    messagebox.showinfo("Sin resultados", "No se encontraron resultados para esa fecha.")
                    
                db.cerrar()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al consultar la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese una fecha válida.")

    def buscar_por_status(self):
        """Consulta por status."""
        status = self.entry_status.get()

        if status:
            try:
                db = ConexionDB()
                db.cursor.execute("SELECT * FROM jubilados WHERE status_jubilados = ?", (status,))
                resultados = db.cursor.fetchall()
                
                if resultados:
                    self.limpiar_tabla()
                    self.insertar_en_tabla(resultados)
                else:
                    messagebox.showinfo("Sin resultados", "No se encontraron resultados para ese status.")
                    
                db.cerrar()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al consultar la base de datos: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un status válido.")

    def generar_reporte_general(self):
        """Genera un reporte general del status de todos los jubilados."""
        try:
            db = ConexionDB()
            db.cursor.execute("SELECT * FROM jubilados")
            resultados = db.cursor.fetchall()
            
            if resultados:
                self.limpiar_tabla()
                self.insertar_en_tabla(resultados)
            else:
                messagebox.showinfo("Sin resultados", "No se encontraron registros.")
                
            db.cerrar()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al consultar la base de datos: {e}")

    def abrir_ventana_consultas(self):
        messagebox.showinfo("Consulta", "Ventana de Consultas Abierta")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Jubilados")
    app = Frame(root)
    root.mainloop()
