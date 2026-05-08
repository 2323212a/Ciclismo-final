from app.db.database import get_connection


# ==================================================
# CREAR USUARIO
# ==================================================
def crear_usuario(
    nombre,
    email,
    password,
    categoria_id,
    evento_id,
    rol="usuario"
):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)

    try:
        # ------------------------------------------
        # OBTENER ROL
        # ------------------------------------------
        cursor.execute(
            "SELECT id FROM roles WHERE nombre = %s",
            (rol,)
        )

        rol_data = cursor.fetchone()

        if not rol_data:
            raise Exception("Rol no existe")

        rol_id = rol_data[0]

        # ------------------------------------------
        # CREAR USUARIO
        # ------------------------------------------
        query_usuario = """
        INSERT INTO usuarios
        (nombre, email, password, rol_id)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query_usuario,
            (nombre, email, password, rol_id)
        )

        usuario_id = cursor.lastrowid

        # ------------------------------------------
        # CREAR INSCRIPCIÓN
        # ------------------------------------------
        query_inscripcion = """
        INSERT INTO inscripciones
        (usuario_id, evento_id, categoria_id)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query_inscripcion,
            (usuario_id, evento_id, categoria_id)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()


# ==================================================
# OBTENER TODOS LOS USUARIOS
# ==================================================
def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        u.id,
        u.nombre,
        u.email,
        r.nombre AS rol,
        c.nombre AS categoria,
        e.nombre AS evento,
        e.fecha,
        e.ubicacion

    FROM usuarios u

    JOIN roles r
    ON u.rol_id = r.id

    LEFT JOIN inscripciones i
    ON u.id = i.usuario_id

    LEFT JOIN categorias c
    ON i.categoria_id = c.id

    LEFT JOIN eventos e
    ON i.evento_id = e.id
    """

    cursor.execute(query)

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados


# ==================================================
# OBTENER UN USUARIO
# ==================================================
def obtener_usuario(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        u.id,
        u.nombre,
        u.email,
        r.nombre AS rol,
        c.nombre AS categoria,
        e.nombre AS evento,
        e.fecha,
        e.ubicacion

    FROM usuarios u

    JOIN roles r
    ON u.rol_id = r.id

    LEFT JOIN inscripciones i
    ON u.id = i.usuario_id

    LEFT JOIN categorias c
    ON i.categoria_id = c.id

    LEFT JOIN eventos e
    ON i.evento_id = e.id

    WHERE u.id = %s
    """

    cursor.execute(query, (id,))

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado


# ==================================================
# ACTUALIZAR USUARIO
# ==================================================
def actualizar_usuario(
    id,
    nombre,
    email,
    password,
    categoria_id,
    evento_id,
    rol
):
    conn = get_connection()
    cursor = conn.cursor(buffered=True)

    try:
        # ------------------------------------------
        # VALIDAR USUARIO
        # ------------------------------------------
        cursor.execute(
            "SELECT id FROM usuarios WHERE id = %s",
            (id,)
        )

        if not cursor.fetchone():
            raise Exception("Usuario no existe")

        # ------------------------------------------
        # OBTENER ROL
        # ------------------------------------------
        cursor.execute(
            "SELECT id FROM roles WHERE nombre = %s",
            (rol,)
        )

        rol_data = cursor.fetchone()

        if not rol_data:
            raise Exception("Rol inválido")

        rol_id = rol_data[0]

        # ------------------------------------------
        # ACTUALIZAR USUARIO
        # ------------------------------------------
        query_usuario = """
        UPDATE usuarios
        SET
            nombre = %s,
            email = %s,
            password = %s,
            rol_id = %s
        WHERE id = %s
        """

        cursor.execute(
            query_usuario,
            (
                nombre,
                email,
                password,
                rol_id,
                id
            )
        )

        # ------------------------------------------
        # ACTUALIZAR INSCRIPCIÓN
        # ------------------------------------------
        query_inscripcion = """
        UPDATE inscripciones
        SET
            categoria_id = %s,
            evento_id = %s
        WHERE usuario_id = %s
        """

        cursor.execute(
            query_inscripcion,
            (
                categoria_id,
                evento_id,
                id
            )
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()


# ==================================================
# ELIMINAR USUARIO
# ==================================================
def eliminar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM usuarios WHERE id = %s",
            (id,)
        )

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()


# ==================================================
# LOGIN
# ==================================================
def obtener_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        u.id,
        u.nombre,
        u.email,
        u.password,
        r.nombre AS rol,
        c.nombre AS categoria,
        e.nombre AS evento

    FROM usuarios u

    JOIN roles r
    ON u.rol_id = r.id

    LEFT JOIN inscripciones i
    ON u.id = i.usuario_id

    LEFT JOIN categorias c
    ON i.categoria_id = c.id

    LEFT JOIN eventos e
    ON i.evento_id = e.id

    WHERE u.email = %s
    """

    cursor.execute(query, (email,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario


# ==================================================
# OBTENER EVENTOS
# ==================================================
def obtener_eventos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM eventos")

    eventos = cursor.fetchall()

    cursor.close()
    conn.close()

    return eventos


# ==================================================
# OBTENER CATEGORÍAS
# ==================================================
def obtener_categorias():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categorias")

    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return categorias