from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
import database, models, schemas
from custom_hashing import hash_password, verify_password  # Importar tu función personalizada
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Configuración JWT
SECRET_KEY = "your_secret_key"  # Cambia esto por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Crear un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("id")
        if username is None or role is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username, "role": role, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Endpoint de login
router = APIRouter()

@router.post("/login")
def login(login_request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    # Buscar en empleados
    employee = db.query(models.Employee).filter(models.Employee.Username == login_request.username).first()
    if employee and verify_password(login_request.password, employee.PasswordHash):
        access_token = create_access_token(data={
            "sub": employee.Username,
            "role": "employee",
            "id": employee.EmployeeID
        })
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "employee",
            "id": employee.EmployeeID  # Incluye explícitamente el ID
        }

    # Buscar en compradores
    customer = db.query(models.Customer).filter(models.Customer.Username == login_request.username).first()
    if customer and verify_password(login_request.password, customer.PasswordHash):
        access_token = create_access_token(data={
            "sub": customer.Username,
            "role": "customer",
            "id": customer.CustomerID
        })
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "customer",
            "id": customer.CustomerID  # Incluye explícitamente el ID
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")