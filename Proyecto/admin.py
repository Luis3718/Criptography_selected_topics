import os
from PyPDF2 import PdfReader
from cryptography.hazmat.primitives import hashes
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def read_metadata(file_path):
    """Read metadata from a PDF file."""
    try:
        if not os.path.exists(file_path):
            print(f"Error: The file {file_path} does not exist.")
            return None

        if not file_path.lower().endswith('.pdf'):
            print(f"Error: The file {file_path} is not a valid PDF.")
            return None

        reader = PdfReader(file_path)
        metadata = reader.metadata
        if metadata is None:
            print("No metadata found in the PDF file.")
            return {}
        return metadata
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading metadata: {e}")
        return None

def calcular_hash(ruta_archivo):
    """Calculate the hash of a file."""
    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()
    digest = hashes.Hash(hashes.SHA256())
    digest.update(contenido)
    return digest.finalize().hex()

def get_stored_hash_from_db(employee_id, db: Session):
    """Retrieve the stored hash of an employee's file from the database."""
    try:
        query = text("SELECT PublicKeyECDSA FROM Employees WHERE EmployeeID = :id")
        result = db.execute(query, {"id": employee_id}).fetchone()
        if result:
            return result[0]  # The stored hash is expected to be a hexadecimal string
        else:
            print("Employee ID not found in the database.")
            return None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def verify_file_hash(calculated_hash, stored_hash):
    """Compare the calculated hash with the stored hash."""
    return calculated_hash == stored_hash

if __name__ == "__main__":
    # Request file name from the user
    file_to_check = input("Enter the name of the file to verify: ").strip()

    if not os.path.exists(file_to_check):
        # Check in "Proyecto" folder
        project_path = os.path.join(os.getcwd(), "Proyecto", file_to_check)
        if not os.path.exists(project_path):
            print(f"File {file_to_check} does not exist in the current directory or 'Proyecto' folder.")
            exit(1)
        else:
            file_to_check = project_path

    # Request employee ID
    employee_id = input("Enter the employee ID: ").strip()

    # Use the database session
    with next(get_db()) as db:
        # Retrieve the stored hash from the database
        stored_hash = get_stored_hash_from_db(employee_id, db)
        if not stored_hash:
            print("Stored hash retrieval failed.")
            exit(1)

        # Calculate the hash of the file
        calculated_hash = calcular_hash(file_to_check)

        # Compare hashes
        if verify_file_hash(calculated_hash, stored_hash):
            print("File hash verified successfully.")
        else:
            print("File hash verification failed.")
