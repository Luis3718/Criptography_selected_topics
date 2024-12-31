import os
from PyPDF2 import PdfReader
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
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
        return {key: str(value) for key, value in metadata.items() if value is not None}
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
    return digest.finalize()

def get_public_key_from_db(employee_id, db: Session):
    """Retrieve the public key of an employee from the database."""
    try:
        query = text("SELECT PublicKeyECDSA FROM Employees WHERE EmployeeID = :id")
        result = db.execute(query, {"id": employee_id}).fetchone()
        if result:
            return result[0]  # The stored public key is expected to be in PEM format
        else:
            print("Employee ID not found in the database.")
            return None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def verify_signature(file_path, public_key_pem, signature):
    """Verify the ECDSA signature of a file."""
    try:
        # Load the public key
        public_key = load_pem_public_key(public_key_pem.encode())

        # Calculate the hash of the file
        file_hash = calcular_hash(file_path)

        # Verify the signature
        public_key.verify(
            signature,
            file_hash,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False

if __name__ == "__main__":
    # Request file name from the user
    file_to_check = input("Enter the name of the file to verify: ").strip()

    # Define the path within the "Proyecto/reports" directory
    project_reports_path = os.path.join(os.getcwd(), "Proyecto", "reports", file_to_check)
    
    if not os.path.exists(project_reports_path):
        print(f"File {file_to_check} does not exist in the 'Proyecto/reports' folder.")
        exit(1)

    # Request employee ID
    employee_id = input("Enter the employee ID: ").strip()

    # Use the database session
    with next(get_db()) as db:
        # Retrieve the public key from the database
        public_key_pem = get_public_key_from_db(employee_id, db)
        if not public_key_pem:
            print("Public key retrieval failed.")
            exit(1)

        # Read metadata from the PDF
        metadata = read_metadata(project_reports_path)
        print(metadata)
        if not metadata:
            print("Failed to retrieve metadata from the PDF.")
            exit(1)

        # Extract the signature from metadata
        signature_hex = metadata.get('EmployeeSignature')
        if not signature_hex:
            print("No signature found in the PDF metadata under 'EmployeeSignature'.")
            exit(1)

        try:
            signature = bytes.fromhex(signature_hex)
        except ValueError:
            print("Invalid signature format in the metadata.")
            exit(1)

        # Verify the signature
        if verify_signature(project_reports_path, public_key_pem, signature):
            print("The file's signature is valid.")
        else:
            print("The file's signature is invalid.")
