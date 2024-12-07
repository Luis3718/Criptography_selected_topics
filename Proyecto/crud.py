from sqlalchemy.orm import Session
import models, schemas
from custom_hashing import hash_password
from ECDSA import generate_ecdsa_keys  # Importar la función para generar llaves ECDSA

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Hashear la contraseña
    employee.PasswordHash = hash_password(employee.PasswordHash)

    # Generar las llaves ECDSA
    private_key, public_key = generate_ecdsa_keys()
    employee.PublicKeyECDSA = public_key  # Guardar la llave pública en la base de datos

    # Crear la entrada en la base de datos
    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    # Guardar la llave privada en un archivo
    file_path = f"private_keys/private_key_{db_employee.EmployeeID}.pem"
    with open(file_path, "w") as key_file:
        key_file.write(private_key)

    return db_employee, file_path  # Retornar el archivo generado


def create_customer(db: Session, customer: schemas.CustomerCreate):
    # Hashear la contraseña
    customer.PasswordHash = hash_password(customer.PasswordHash)
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer