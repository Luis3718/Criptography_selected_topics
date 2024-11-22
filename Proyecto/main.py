from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth, register, customer, employee

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(register.router, prefix="/register", tags=["Registration"])
#app.include_router(customer.router, prefix="/customer", tags=["Customer Operations"])
#app.include_router(employee.router, prefix="/employee", tags=["Employee Operations"])
