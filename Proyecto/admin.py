import os
from PyPDF2 import PdfReader
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.exceptions import InvalidSignature
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

def read_metadata(file_path):
    try:
        reader = PdfReader(file_path)
        metadata = reader.metadata
        print(f"Metadatos encontrados: {metadata}")  # Depuración
        return metadata
    except Exception as e:
        print(f"Error leyendo los metadatos: {e}")
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
        print(f"Hash calculado: {file_hash.hex()}")

        # Verify the signature (no need to decode DER here)
        public_key.verify(
            signature,
            file_hash,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        print("La firma no es válida.")
        return False
    except Exception as e:
        print(f"Error en la verificación: {e}")
        return False

if __name__ == "__main__":
    # Request file name from the user
    file_to_check = input("Enter the name of the file to verify: ").strip()

    # Define the path within the "Proyecto/reports" directory
    project_reports_path = os.path.join(os.getcwd(), "reports", file_to_check)
    
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
        if not metadata:
            print("Failed to retrieve metadata from the PDF.")
            exit(1)

        # Use the correct key for the signature
        signature_hex = metadata.get("/empleado")
        if signature_hex:
            try:
                signature = bytes.fromhex(signature_hex.strip())
                print(signature)
                # Decode the signature from DER format
                r, s = decode_dss_signature(signature)
                print(f"Decoded signature values: r={r}, s={s}")
            except ValueError:
                print(f"Formato de firma inválido: {signature_hex}")
                exit(1)
        else:
            print("No se encontró la firma en los metadatos.")
            exit(1)

        # Verify the signature
        if verify_signature(project_reports_path, public_key_pem, signature):
            print("The file's signature is valid.")
        else:
            print("The file's signature is invalid.")
