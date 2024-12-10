import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database, models
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/transactions", response_model=list[schemas.Transaction])
def get_employee_transactions(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    # Extraer EmployeeID desde el token
    user_data = crud.get_employee_id_from_token(token)

    if not user_data or user_data.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    employee_id = user_data.get("id")

    # Obtener las transacciones del empleado
    transactions = db.query(models.Transaction).filter(models.Transaction.EmployeeID == employee_id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this employee")

    return transactions

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
