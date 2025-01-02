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

def obtener_archivo_original(file_path_signed):
    """
    Obtiene la ruta del archivo original correspondiente al archivo firmado.
    Remueve el sufijo '_signed' del nombre del archivo.
    """
    # Remover '_signed' del nombre del archivo
    if "_signed" in file_path_signed:
        file_path_original = file_path_signed.replace("_signed", "")
        if os.path.exists(file_path_original):
            return file_path_original
        else:
            raise FileNotFoundError(f"El archivo original '{file_path_original}' no existe.")
    else:
        raise ValueError("El archivo firmado no tiene el sufijo '_signed'.")


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
    # Solicitar el archivo firmado
    file_to_check = input("Enter the name of the file to verify: ").strip()

    # Ruta del archivo firmado
    project_reports_path_signed = os.path.join(os.getcwd(), "reports", file_to_check)

    if not os.path.exists(project_reports_path_signed):
        print(f"File {file_to_check} does not exist in the 'reports' folder.")
        exit(1)

    # Determinar la ruta del archivo original
    try:
        project_reports_path_original = obtener_archivo_original(project_reports_path_signed)
        print(f"Archivo original encontrado: {project_reports_path_original}")
    except (FileNotFoundError, ValueError) as e:
        print(e)
        exit(1)

    # Solicitar el ID del empleado
    employee_id = input("Enter the employee ID: ").strip()

    # Obtener la clave pública del empleado
    with next(get_db()) as db:
        public_key_pem = get_public_key_from_db(employee_id, db)
        if not public_key_pem:
            print("Public key retrieval failed.")
            exit(1)

    # Leer los metadatos para extraer la firma
    metadata = read_metadata(project_reports_path_signed)
    if not metadata:
        print("Failed to retrieve metadata from the signed PDF.")
        exit(1)

    # Extraer la firma desde los metadatos
    signature_hex = metadata.get("/empleado")
    if signature_hex:
        try:
            signature = bytes.fromhex(signature_hex.strip())
            print(f"Firma extraída: {signature.hex()}")
        except ValueError:
            print(f"Formato de firma inválido: {signature_hex}")
            exit(1)
    else:
        print("No se encontró la firma en los metadatos.")
        exit(1)

    # Calcular el hash del archivo original
    file_hash = calcular_hash(project_reports_path_original)
    print(f"Hash calculado para verificación: {file_hash.hex()}")

    # Verificar la firma
    if verify_signature(project_reports_path_original, public_key_pem, signature):
        print("The file's signature is valid.")
    else:
        print("The file's signature is invalid.")
