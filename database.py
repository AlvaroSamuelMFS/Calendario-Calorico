import sqlite3
from contextlib import nullcontext

import bcrypt

def crear_conexion():
    conn = sqlite3.connect("usuarios.db")
    return conn

def crear_tabla():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            peso REAL,
            altura REAL,
            nacimiento DATE,
            sexo TEXT,
            actividad INTEGER,
            objetivo TEXT
        )
    """)
    conn.commit()
    conn.close()

def crear_tabla_alimentos():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            dia TEXT,
            comida TEXT,
            alimento TEXT,
            gramos REAL,
            calorias REAL,
            proteinas REAL,
            hdc REAL,
            grasas REAL
        )
    """)
    conn.commit()
    conn.close()

def crear_usuario(nombre,contrasena,peso,altura,dia,mes,año,sexo,actividad,objetivo):
    conn = crear_conexion()
    cursor = conn.cursor()
    contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())
    cursor.execute("INSERT INTO usuarios (nombre,contrasena,peso,altura,nacimiento,sexo,actividad,objetivo)VALUES(?,?,?,?,?,?,?,?)",(nombre,contrasena_hash,peso,altura,f"{año}-{mes}-{dia}",sexo,actividad,objetivo))
    conn.commit()
    cursor.close()
    conn.close()
def modificar_usuario(id,altura,peso,actividad,objetivo):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios set altura=?,peso=?, actividad=?, objetivo=? WHERE id=?",(altura,peso,actividad,objetivo,id))
    conn.commit()
    cursor.close()
    conn.close()

def verificar_usuario(nombre):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE nombre=?",(nombre,))
    resultado = cursor.fetchall()
    conn.close()
    if  not resultado:
        return True
    else:
        return False

def inicio_sesion(nombre, contrasena):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE nombre=?",(nombre,))
    resultado = cursor.fetchall()
    if resultado:
        contrasena_hash = resultado[0][0]
        if bcrypt.checkpw(contrasena.encode("utf-8"), contrasena_hash):
            cursor.execute("SELECT id FROM usuarios WHERE nombre=? AND contrasena=?", (nombre,contrasena_hash))
            resultadoId = cursor.fetchall()
            return resultadoId[0][0]
        else:
            conn.close()
            return -1
    else:
        conn.close()
        return -1
def datos_usuario(nombre):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (nombre,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def datos_usuario_id(id):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def guardar_alimento(usuario_id, dia, comida, alimento, gramos, calorias, proteinas, hdc, grasas):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comidas (usuario_id, dia, comida, alimento, gramos, calorias, proteinas, hdc, grasas)VALUES(?,?,?,?,?,?,?,?,?)",(usuario_id, dia, comida, alimento, gramos,calorias, proteinas, hdc, grasas))
    conn.commit()
    id_insertado = cursor.lastrowid
    cursor.close()
    conn.close()
    return id_insertado


def eliminar_alimento(id):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comidas WHERE id=? ",(id,))
    #cursor.execute("DELETE FROM comidas WHERE id=1 ")
    conn.commit()
    cursor.close()
    conn.close()

def cargar_comidas(id):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comidas WHERE usuario_id =?",(id,))
    comidas = cursor.fetchall()
    conn.close()
    return comidas


def obtener_resultados_semanales(id):
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT dia, ROUND(SUM(calorias),2), ROUND(SUM(proteinas),2), ROUND(SUM(hdc),2), ROUND(SUM(grasas),2)
        FROM comidas 
        WHERE usuario_id=?
        GROUP BY dia
    """,(id,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado


