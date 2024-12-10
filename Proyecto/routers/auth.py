from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
import database, models, schemas
from custom_hashing import hash_password, verify_password  # Importar tu función personalizada

# Configuración JWT
SECRET_KEY = "your_secret_key"  # Cambia esto por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint de login
router = APIRouter()

@router.post("/login")
def login(login_request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    # Buscar en empleados
    employee = db.query(models.Employee).filter(models.Employee.Username == login_request.username).first()
    if employee and verify_password(login_request.password, employee.PasswordHash):
        access_token = create_access_token(data={"sub": employee.Username, "role": "employee"})
        return {"access_token": access_token, "token_type": "bearer", "role": "employee"}

    # Buscar en compradores
    customer = db.query(models.Customer).filter(models.Customer.Username == login_request.username).first()
    if customer and verify_password(login_request.password, customer.PasswordHash):
        access_token = create_access_token(data={"sub": customer.Username, "role": "customer"})
        return {"access_token": access_token, "token_type": "bearer", "role": "customer"}

    # Si no se encuentra en ninguna tabla o las credenciales son incorrectas
    raise HTTPException(status_code=401, detail="Invalid username or password")
