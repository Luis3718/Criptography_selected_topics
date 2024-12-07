from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import create_customer_user, create_employee_user
from database import get_db
from schemas import CustomerCreate, EmployeeCreate

router = APIRouter()

@router.post("/customer")
def register_customer(request: RegisterCustomerRequest, db: Session = Depends(get_db)):
    new_user = create_customer_user(db, request.username, request.password, request.customer_id)
    return {"message": "Customer registered successfully", "user_id": new_user.UserID}

@router.post("/register/employee")
def register_employee(request: RegisterEmployeeRequest, db: Session = Depends(get_db)):
    new_user = create_employee_user(db, request.username, request.password, request.employee_id, request.role)
    return {"message": "Employee registered successfully", "user_id": new_user.UserID}
