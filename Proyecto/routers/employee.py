from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import crud, schemas, database
import os

router = APIRouter()

@router.post("/")
def register_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    db_employee, private_key_path = crud.create_employee(db, employee)
    private_key_url = f"/employees/download_private_key/{db_employee.EmployeeID}"
    return {
        "message": "Employee created successfully",
        "employee_id": db_employee.EmployeeID,
        "private_key_url": private_key_url
    }

@router.get("/download_private_key/{employee_id}")
def download_private_key(employee_id: int):
    file_path = f"private_keys/private_key_{employee_id}.pem"  # Ruta relativa correcta
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Private key not found")
    return FileResponse(file_path, media_type="application/x-pem-file", filename=f"private_key_{employee_id}.pem")
