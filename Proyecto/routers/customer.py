from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database, models
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/")
def register_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    db_customer = crud.create_customer(db, customer)
    return {"message": "Customer created successfully", "customer_id": db_customer.CustomerID}


@router.get("/transactions", response_model=list[schemas.Transaction])
def get_customer_transactions(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    # Extraer CustomerID desde el token (esto dependerá de tu implementación de tokens)
    customer_id = crud.get_customer_id_from_token(token)

    if not customer_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    # Obtener las transacciones del cliente
    transactions = db.query(models.Transaction).filter(models.Transaction.CustomerID == customer_id).all()

    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found for this customer")

    return transactions
