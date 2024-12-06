from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database

router = APIRouter()

@router.post("/")
def register_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    db_employee = crud.create_employee(db, employee)
    return {"message": "Employee created successfully", "employee_id": db_employee.EmployeeID}
