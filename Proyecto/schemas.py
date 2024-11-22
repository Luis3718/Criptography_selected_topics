from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    Employee = "Employee"
    Admin = "Admin"

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginResponse(BaseModel):
    message: str
    user_id: int

class RegisterCustomerRequest(BaseModel):
    username: str
    password: str
    customer_id: int

class RegisterEmployeeRequest(BaseModel):
    username: str
    password: str
    employee_id: int
    role: RoleEnum
