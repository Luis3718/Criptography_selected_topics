from sqlalchemy.orm import Session
import models, schemas
from custom_hashing import hash_password

def create_customer(db: Session, customer: schemas.CustomerCreate):
    # Hashear la contraseña
    customer.PasswordHash = hash_password(customer.PasswordHash)
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Hashear la contraseña
    employee.PasswordHash = hash_password(employee.PasswordHash)
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee
