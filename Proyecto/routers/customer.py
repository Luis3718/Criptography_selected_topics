from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, database

router = APIRouter()

@router.post("/")
def register_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    db_customer = crud.create_customer(db, customer)
    return {"message": "Customer created successfully", "customer_id": db_customer.CustomerID}
