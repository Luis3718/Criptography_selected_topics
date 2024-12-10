from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

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

class Transaction(BaseModel):
    TransactionID: int
    CustomerID: int
    EmployeeID: int
    DateOfSale: datetime  # Sigue siendo un datetime aquí
    TotalAmount: float

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convierte datetime a string en formato ISO 8601
        }
