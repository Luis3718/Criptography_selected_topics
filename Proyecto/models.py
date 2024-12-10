from sqlalchemy import Column, Integer, String, Enum, Text
from database import Base
import enum

# Modelo de Cliente para SQLAlchemy
class Customer(Base):
    __tablename__ = "customers"
    CustomerID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String(255), nullable=False)
    PhoneNumber = Column(String(15), nullable=False)
    CreditCardNumber = Column(String(255), nullable=False)
    Username = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    Salt = Column(String(32), nullable=False)

# Modelo de Empleado para SQLAlchemy
class Employee(Base):
    __tablename__ = "employees"
    EmployeeID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String(255), nullable=False)
    Username = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    PublicKeyECDSA = Column(Text, nullable=False)
    Salt = Column(String(32), nullable=False)
