import jwt
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from models import Pacientes
from schemas import PacienteCreate, PacienteResponse, PacienteLogin, PacienteLoginResponse
from crud import crear_paciente, verificar_credenciales
from passlib.context import CryptContext

# Configuración JWT
SECRET_KEY = "h#jnas34_"
ALGORITHM = "HS256"

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Crear la instancia de FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para registrar un paciente
@app.post("/pacientes/", response_model=PacienteResponse)
def registrar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    try:
        return crear_paciente(db, paciente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login/")
def login_paciente(credentials: PacienteLogin, db: Session = Depends(get_db)):
    paciente = verificar_credenciales(db, credentials.Correo, credentials.Contraseña)
    if not paciente:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Crear un token JWT con expiración
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"sub": paciente.ID_Paciente, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
    
    # Crear la respuesta con el token en una cookie
    response = JSONResponse(content={"Mensaje": "Inicio de sesión exitoso"})
    response.set_cookie(key="token", value=token, httponly=True, max_age=3600)  # 1 hora de duración
    
    return response

@app.post("/logout/")
def logout(response: Response):
    response.delete_cookie(key="token")
    return {"Mensaje": "Sesión cerrada correctamente"}

@app.get("/usuario-info/")
def obtener_usuario_info(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")

    try:
        # Decodificar el token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")
        
        # Buscar la información del usuario en la base de datos
        paciente = db.query(Pacientes).filter(Pacientes.ID_Paciente == usuario_id).first()
        if not paciente:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"Nombre": paciente.Nombre}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
