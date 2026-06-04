from pathlib import Path
import sqlite3
import uuid
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "reservas.db"

def conectar_db():
    
    DATABASE_DIR.mkdir(exist_ok = True)
    
    conexion = sqlite3.connect(DATABASE_PATH)
    conexion.row_factory = sqlite3.Row

    return conexion

def inicializar_db():
    
    conexion = conectar_db()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_reserva TEXT UNIQUE NOT NULL,
            nombre_cliente TEXT NOT NULL,
            destino TEXT NOT NULL,
            fecha_salida TEXT NOT NULL,
            numero_personas INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'activa',
            fecha_creacion TEXT NOT NULL,
            fecha_actualizacion TEXT
        );
        """
    )
    
    conexion.commit()
    conexion.close()
    

def generar_numero_reserva():
    
    fecha = datetime.now().strftime("%Y%m%d")
    codigo = uuid.uuid4().hex[:6].upper()
    
    return f"RES-{fecha}-{codigo}"


def crear_reserva(nombre_cliente, destino, fecha_salida, numero_personas):

    numero_reserva = generar_numero_reserva()
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO reservas (
            numero_reserva,
            nombre_cliente,
            destino,
            fecha_salida,
            numero_personas,
            estado,
            fecha_creacion
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        (
            numero_reserva,
            nombre_cliente,
            destino,
            fecha_salida,
            numero_personas,
            "activa",
            fecha_creacion,
        ),
    )

    conexion.commit()
    conexion.close()

    return numero_reserva
    
    
def consultar_reserva(numero_reserva):

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT
            numero_reserva,
            nombre_cliente,
            destino,
            fecha_salida,
            numero_personas,
            estado,
            fecha_creacion,
            fecha_actualizacion
        FROM reservas
        WHERE numero_reserva = ?;
        """,
        (numero_reserva,),
    )

    reserva = cursor.fetchone()
    conexion.close()

    if reserva is None:
        return None

    return dict(reserva)



def modificar_reserva(numero_reserva, nuevo_destino, nueva_fecha_salida, nuevo_numero_personas):

    fecha_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE reservas
        SET
            destino = ?,
            fecha_salida = ?,
            numero_personas = ?,
            estado = 'modificada',
            fecha_actualizacion = ?
        WHERE numero_reserva = ?
        AND estado != 'cancelada';
        """,
        (
            nuevo_destino,
            nueva_fecha_salida,
            nuevo_numero_personas,
            fecha_actualizacion,
            numero_reserva,
        ),
    )

    conexion.commit()
    filas_modificadas = cursor.rowcount
    conexion.close()

    return filas_modificadas > 0


def cancelar_reserva(numero_reserva):

    fecha_actualizacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        """
        UPDATE reservas
        SET
            estado = 'cancelada',
            fecha_actualizacion = ?
        WHERE numero_reserva = ?
        AND estado != 'cancelada';
        """,
        (
            fecha_actualizacion,
            numero_reserva,
        ),
    )

    conexion.commit()
    filas_modificadas = cursor.rowcount
    conexion.close()

    return filas_modificadas > 0