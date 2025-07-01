import sqlite3

DB_FILE = 'db.sqlite3'

#Funcion que crea la tabla de sensores si es que no existe
def init_db():

    #Conecta con la base de datos, si no existe, crea una
    conn = sqlite3.connect(DB_FILE)

    #Crea un cursor que permite ejecutar sentencias SQL
    c = conn.cursor()

    #Ejecuta una sentencia SQL para crear la tabla de los sensores si es que aun no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS sensores (
            id INTEGER,
            fecha_hora TEXT,
            temperatura REAL,
            presion REAL,
            humedad REAL
        )
    ''')

    #Guarda los cambios y cierra la conexion con la base de datos
    conn.commit()
    conn.close()

#Funcion para insertar un nuevo dato en la DB
#Recibe un diccionario "dato"
def insertar_dato(dato):

    #Conecta con la base de datos y crea un cursor
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #Ejecuta una sentencia SQL para insertar los datos
    c.execute('''
        INSERT INTO sensores (id, fecha_hora, temperatura, presion, humedad)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        dato['id'],
        dato['fecha_hora'],
        dato['temperatura'],
        dato['presion'],
        dato['humedad']
    ))

    #Guarda y cierra la conexion
    conn.commit()
    conn.close()


#Funcion que recupera los ultimos "limit" datos insertados
def obtener_ultimos_datos(limit=10):

    #Conecta a la BD y configura "row_factory" para poder acceder a los resultados como diccionarios
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    #Consulta los últimos "limit" registros de la tabla "sensores", ordenados por "fecha_hora" en orden descendente.
    c = conn.cursor()
    c.execute('SELECT * FROM sensores ORDER BY fecha_hora DESC LIMIT ?', (limit,))

    #Guarda los resultados y cierra la conexion
    filas = c.fetchall()
    conn.close()

    #Convierte cada fila a un diccionario para que sea facil de convertir a JSON en la API
    return [dict(fila) for fila in filas]
