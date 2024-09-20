from .conexion_db import ConexionDB
from tkinter import messagebox

def crear_tabla():
    conexion = ConexionDB()

    sql = '''
    CREATE TABLE jubilados(
        id_jubilados INTEGER PRIMARY KEY AUTOINCREMENT,
        ficha_jubilados INTEGER(1000),
        nombre_jubilados VARCHAR(100),
        fj_jubilados VARCHAR(20),
        ce_jubilados VARCHAR(100),
        direc_jubilados VARCHAR(100),
        tel_jubilados VARCHAR(20),
        fc_jubilados VARCHAR(20),
        lug_jubilados VARCHAR(100),
        status_jubilados VARCHAR(50)
    )'''
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        
        titulo = 'Crear Registro'
        mensaje = 'Se creo la tabla en la base datos'
        messagebox.showinfo(titulo,mensaje)

    except:
        titulo = 'Crear Registro'
        mensaje = 'Ya se creo la tabla en la base datos'
        messagebox.showwarning(titulo,mensaje)

def borrar_tabla():
    conexion = ConexionDB()

    sql = 'DROP TABLE jubilados'
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()

        titulo = 'Borrando Registro'
        mensaje = 'Se a borrado la tabla en la base datos'
        messagebox.showinfo(titulo,mensaje)

    except:
        titulo = 'Borrando Registro'
        mensaje = 'No hay tabla en la base datos'
        messagebox.showwarning(titulo,mensaje)

class jubilado:
    def __init__(self, ficha, nombre, fj, ce, direc, tel, fc, lug, status):
        self.id_jubilados = None
        self.ficha = ficha
        self.nombre = nombre
        self.fj = fj
        self.ce = ce
        self.direc = direc
        self.tel = tel
        self.fc = fc
        self.lug = lug
        self.status = status

    def __str__(self):
        return f'jubilados[{self.ficha},{self.nombre},{self.fj},{self.ce},{self.direc},{self.tel},{self.fc},{self.lug},{self.status}]'

def guardar(jubilado):
    conexion = ConexionDB()

    sql = f"""INSERT INTO jubilados (ficha_jubilados, nombre_jubilados, fj_jubilados, ce_jubilados, direc_jubilados, tel_jubilados, fc_jubilados, lug_jubilados, status_jubilados)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    try:
        conexion.cursor.execute(sql, (jubilado.ficha, jubilado.nombre, jubilado.fj, jubilado.ce, jubilado.direc, jubilado.tel, jubilado.fc, jubilado.lug, jubilado.status))
        conexion.cerrar()
    except Exception as e:
        conexion.cerrar()
        titulo = 'Conexión al Registro'
        mensaje = f'Error al guardar los datos: {e}'
        messagebox.showerror(titulo, mensaje)

def listar():

    conexion = ConexionDB()

    lista_jubilados = []
    sql = 'SELECT * FROM jubilados'

    try:
        conexion.cursor.execute(sql)
        lista_jubilados = conexion.cursor.fetchall()
        conexion.cerrar()

    except:
        titulo = 'Conexion al Registro'
        mensaje = 'Crea la tabla en la Base de datos'
        messagebox.showwarning(titulo, mensaje)

    return lista_jubilados

def editar(jubilado, id_jubilados):
    conexion = ConexionDB()

    sql = """UPDATE jubilados
    SET ficha_jubilados = ?, nombre_jubilados = ?, fj_jubilados = ?, 
    ce_jubilados = ?, direc_jubilados = ?, tel_jubilados = ?, 
    fc_jubilados = ?, lug_jubilados = ?, status_jubilados = ?
    WHERE id_jubilados = ?"""

    try:
        conexion.cursor.execute(sql, (
            jubilado.ficha, jubilado.nombre, jubilado.fj,
            jubilado.ce, jubilado.direc, jubilado.tel,
            jubilado.fc, jubilado.lug, jubilado.status,
            id_jubilados
        ))
        conexion.cerrar()

    except Exception as e:
        conexion.cerrar()
        titulo = 'Edición de datos'
        mensaje = f'No se pudo actualizar el registro: {e}'
        messagebox.showerror(titulo, mensaje)

        
def eliminar(id_jubilados):
    conexion = ConexionDB()
    sql = f'DELETE FROM jubilados WHERE id_jubilados = {id_jubilados}'

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Eilinar datos'
        mensaje = 'Se han eliminado los datos'
        messagebox.showerror(titulo,mensaje)

