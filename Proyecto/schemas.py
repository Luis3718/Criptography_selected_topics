from pydantic import BaseModel
from enum import Enum

# Modelos de Pydantic para validación
class CustomerCreate(BaseModel):
    FullName: str
    PhoneNumber: str
    CreditCardNumber: str
    Username: str
    PasswordHash: str

class EmployeeCreate(BaseModel):
    FullName: str
    Username: str
    PasswordHash: str
    PublicKeyECDSA: str

