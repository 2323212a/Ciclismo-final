from app.db.database import get_connection

# CREATE
def crear_usuario(nombre, email, password, categoria, rol="usuario"):
    conn = get_connection()
    cursor = conn.cursor()

    # validar rol
    cursor.execute("SELECT id FROM roles WHERE nombre = %s", (rol,))
    rol_data = cursor.fetchone()

    if not rol_data:
        cursor.close()
        conn.close()
        raise Exception("Rol no válido")

    rol_id = rol_data[0]

    query = """
    INSERT INTO usuarios (nombre, email, password, categoria, rol_id)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (nombre, email, password, categoria, rol_id))
    conn.commit()

    cursor.close()
    conn.close()

 # READ ALL
def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT u.id, u.nombre, u.email, u.categoria, r.nombre AS rol
    FROM usuarios u
    JOIN roles r ON u.rol_id = r.id
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()
    return resultados

# READ ONE
def obtener_usuario(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT u.id, u.nombre, u.email, u.categoria, r.nombre AS rol
    FROM usuarios u
    JOIN roles r ON u.rol_id = r.id
    WHERE u.id = %s
    """

    cursor.execute(query, (id,))
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()
    return resultado

def actualizar_usuario(id, nombre, email, password, categoria, rol):
    conn = get_connection()
    cursor = conn.cursor()

    # validar usuario
    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise Exception("Usuario no existe")

    # validar rol
    cursor.execute("SELECT id FROM roles WHERE nombre = %s", (rol,))
    rol_data = cursor.fetchone()

    if not rol_data:
        cursor.close()
        conn.close()
        raise Exception("Rol no válido")

    rol_id = rol_data[0]

    query = """
    UPDATE usuarios
    SET nombre = %s, email = %s, password = %s, categoria = %s, rol_id = %s
    WHERE id = %s
    """

    cursor.execute(query, (nombre, email, password, categoria, rol_id, id))
    conn.commit()

    cursor.close()
    conn.close()

def eliminar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    # validar usuario
    cursor.execute("SELECT id FROM usuarios WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        raise Exception("Usuario no existe")

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

def obtener_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT u.id, u.nombre, u.email, u.password, r.nombre AS rol
    FROM usuarios u
    JOIN roles r ON u.rol_id = r.id
    WHERE u.email = %s
    """

    cursor.execute(query, (email,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()
    return usuario