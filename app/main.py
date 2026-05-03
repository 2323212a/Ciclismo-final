from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.schemas.usuario import Usuario
from app.models import queries

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/frontend"), name="static")


# -----------------------
# CONFIGURACIÓN SEGURIDAD
# -----------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password[:72])

def verify_password(plain, hashed):
    return pwd_context.verify(plain[:72], hashed)

# -----------------------
# CORS
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restringe en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# RUTA BASE
# -----------------------
@app.get("/")
def mostrar_index():
    return FileResponse("app/frontend/index.html")


# -----------------------
# REGISTER (CREATE)
# -----------------------
@app.post("/usuarios")
def crear(usuario: Usuario):
    try:
        print("📩 Datos recibidos:", usuario)

        password_hash = hash_password(usuario.password)

        queries.crear_usuario(
            usuario.nombre,
            usuario.email,
            password_hash,
            usuario.categoria,
            usuario.rol
        )

        print("✅ Usuario insertado correctamente")

        return {"mensaje": "Usuario creado"}

    except Exception as e:
        print("🔥 ERROR REAL:", e)
        raise HTTPException(status_code=400, detail=str(e))
# -----------------------
# LOGIN
# -----------------------
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    usuario = queries.obtener_usuario_por_email(email)

    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    if not verify_password(password, usuario["password"]):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    return {
        "mensaje": "Login exitoso",
        "usuario": {
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "rol": usuario["rol"]
        }
    }

# -----------------------
# READ ALL
# -----------------------
@app.get("/usuarios")
def listar():
    return queries.obtener_usuarios()

# -----------------------
# READ ONE
# -----------------------
@app.get("/usuarios/{id}")
def obtener(id: int):
    usuario = queries.obtener_usuario(id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

# -----------------------
# UPDATE
# -----------------------
@app.put("/usuarios/{id}")
def actualizar(id: int, usuario: Usuario):
    if not queries.obtener_usuario(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        password_hash = hash_password(usuario.password)

        queries.actualizar_usuario(
            id,
            usuario.nombre,
            usuario.email,
            password_hash,
            usuario.categoria,
            usuario.rol
        )
        return {"mensaje": "Usuario actualizado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------
# DELETE
# -----------------------
@app.delete("/usuarios/{id}")
def eliminar(id: int):
    if not queries.obtener_usuario(id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        queries.eliminar_usuario(id)
        return {"mensaje": "Usuario eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------
# ADMIN (PROTEGIDO BÁSICO)
# -----------------------
@app.get("/admin/usuarios")
def ver_todos(rol: str):
    if rol != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    return queries.obtener_usuarios()