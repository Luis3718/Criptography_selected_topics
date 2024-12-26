import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from report import print_report, save_report_to_pdf
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
    private_key_url = f"/employee/download_private_key/{db_employee.EmployeeID}"
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

@router.get("/monthly_report", response_model=list[dict])
def get_monthly_report(
    month: str,  # Formato esperado: YYYY-MM
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
):
    # Extraer EmployeeID desde el token
    user_data = crud.get_employee_id_from_token(token)

    if not user_data or user_data.get("role") != "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    employee_id = user_data.get("id")

    # Query para obtener el reporte mensual
    query = text(f"""
        SELECT 
            e.FullName AS EmployeeName,
            t.DateOfSale,
            c.FullName AS CustomerName,
            CONCAT('**** **** **** ', RIGHT(t.CreditCardNumber, 4)) AS CreditCardUsed,
            t.TotalAmount,
            GROUP_CONCAT(CONCAT(p.ProductName, ' (x', td.Quantity, ')') SEPARATOR ', ') AS ProductsSold
        FROM 
            Transactions t
        JOIN 
            Employees e ON t.EmployeeID = e.EmployeeID
        JOIN 
            Customers c ON t.CustomerID = c.CustomerID
        JOIN 
            TransactionDetails td ON t.TransactionID = td.TransactionID
        JOIN 
            Products p ON td.ProductID = p.ProductID
        WHERE 
            DATE_FORMAT(t.DateOfSale, '%Y-%m') = :month
            AND e.EmployeeID = :employee_id
        GROUP BY 
            t.TransactionID
        ORDER BY 
            t.DateOfSale
    """)

    results = db.execute(query, {"month": month, "employee_id": employee_id}).fetchall()

    # Convertir resultados en un formato legible
    report = [
        {
            "EmployeeName": row.EmployeeName,
            "DateOfSale": row.DateOfSale.strftime("%Y-%m-%d %H:%M:%S"),
            "CustomerName": row.CustomerName,
            "CreditCardUsed": row.CreditCardUsed,
            "TotalAmount": float(row.TotalAmount),
            "ProductsSold": row.ProductsSold,
        }
        for row in results
    ]

    if not report:
        raise HTTPException(status_code=404, detail="No transactions found for the specified month")
    
    # Guardar el informe en PDF
    #save_report_to_pdf(report, file_name=f"monthly_report_{employee_id}.pdf")

    return report