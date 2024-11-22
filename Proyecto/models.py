from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

class RoleEnum(enum.Enum):
    Employee = "Employee"
    Admin = "Admin"

class CustomerUsers(Base):
    __tablename__ = "customerusers"
    UserID = Column(Integer, primary_key=True, index=True)
    CustomerID = Column(Integer, nullable=False)
    Username = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)

class EmployeeUsers(Base):
    __tablename__ = "employeeusers"
    UserID = Column(Integer, primary_key=True, index=True)
    EmployeeID = Column(Integer, nullable=False)
    Username = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    Role = Column(Enum(RoleEnum), nullable=False)
