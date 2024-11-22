from sqlalchemy.orm import Session
from models import CustomerUsers, EmployeeUsers
from custom_hashing import hash_password, verify_password

def authenticate_customer(db: Session, username: str, password: str):
    user = db.query(CustomerUsers).filter(CustomerUsers.Username == username).first()
    if user and verify_password(password, user.PasswordHash):
        return user
    return None

def authenticate_employee(db: Session, username: str, password: str):
    user = db.query(EmployeeUsers).filter(EmployeeUsers.Username == username).first()
    if user and verify_password(password, user.PasswordHash):
        return user
    return None

def create_customer_user(db: Session, username: str, password: str, customer_id: int):
    hashed_password = hash_password(password)
    new_user = CustomerUsers(CustomerID=customer_id, Username=username, PasswordHash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_employee_user(db: Session, username: str, password: str, employee_id: int, role: str):
    hashed_password = hash_password(password)
    new_user = EmployeeUsers(EmployeeID=employee_id, Username=username, PasswordHash=hashed_password, Role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
