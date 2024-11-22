from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import authenticate_customer, authenticate_employee
from database import get_db
from schemas import LoginRequest, LoginResponse

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    if request.role.lower() == "customer":
        user = authenticate_customer(db, request.username, request.password)
        if user:
            return {"message": "Customer login successful", "user_id": user.UserID}
    elif request.role.lower() in ["employee", "admin"]:
        user = authenticate_employee(db, request.username, request.password)
        if user:
            return {"message": f"{user.Role} login successful", "user_id": user.UserID}
    raise HTTPException(status_code=401, detail="Invalid username, password, or role")
