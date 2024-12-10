from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, DECIMAL, Text
from database import Base
from sqlalchemy.orm import relationship
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
    transactions = relationship("Transaction", back_populates="customer")


# Modelo de Empleado para SQLAlchemy
class Employee(Base):
    __tablename__ = "employees"
    EmployeeID = Column(Integer, primary_key=True, index=True)
    FullName = Column(String(255), nullable=False)
    Username = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(255), nullable=False)
    PublicKeyECDSA = Column(Text, nullable=False)
    Salt = Column(String(32), nullable=False)
    transactions = relationship("Transaction", back_populates="employee")

class Product(Base):
    __tablename__ = "products"
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String(255), nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)

    # Relación con TransactionDetails
    details = relationship("TransactionDetail", back_populates="product")

class Transaction(Base):
    __tablename__ = "transactions"
    TransactionID = Column(Integer, primary_key=True, index=True)
    CustomerID = Column(Integer, ForeignKey("customers.CustomerID"), nullable=False)
    EmployeeID = Column(Integer, ForeignKey("employees.EmployeeID"), nullable=False)
    DateOfSale = Column(DateTime, nullable=False)
    TotalAmount = Column(DECIMAL(10, 2), nullable=False)
    CreditCardNumber = Column(String(255), nullable=False)

    # Relaciones
    customer = relationship("Customer", back_populates="transactions")
    employee = relationship("Employee", back_populates="transactions")
    details = relationship("TransactionDetail", back_populates="transaction")

class TransactionDetail(Base):
    __tablename__ = "transactiondetails"
    TransactionDetailID = Column(Integer, primary_key=True, index=True)
    TransactionID = Column(Integer, ForeignKey("transactions.TransactionID"), nullable=False)
    ProductID = Column(Integer, ForeignKey("products.ProductID"), nullable=False)
    Quantity = Column(Integer, nullable=False)

    # Relaciones
    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product", back_populates="details")
