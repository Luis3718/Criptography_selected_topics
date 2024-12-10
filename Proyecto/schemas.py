from pydantic import BaseModel
from enum import Enum
from typing import Optional

# Modelos de Pydantic para validación
class CustomerCreate(BaseModel):
    FullName: str
    PhoneNumber: str
    CreditCardNumber: str
    Username: str
    PasswordHash: str
    Salt: Optional[str] = None  # Hacer opcional

class EmployeeCreate(BaseModel):
    FullName: str
    Username: str
    PasswordHash: str
    PublicKeyECDSA: Optional[str] = None  # Hacer opcional
    Salt: Optional[str] = None  # Hacer opcional

class LoginRequest(BaseModel):
    username: str
    password: str