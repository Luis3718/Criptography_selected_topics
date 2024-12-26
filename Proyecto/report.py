from fpdf import FPDF
from datetime import datetime
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def save_report_to_pdf(report, file_name="monthly_report.pdf"):
    """
    Guarda el informe en un archivo PDF.
    """
    if not report:
        print("No hay transacciones para el mes especificado.")
        return

    # Inicializar el objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado del reporte
    employee_name = report[0]['EmployeeName']
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Informe Mensual de Ventas", ln=True, align="C")
    pdf.ln(10)  # Salto de línea

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Empleado: {employee_name}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Fecha del Reporte: {report_date}", ln=True, align="L")
    pdf.ln(10)  # Salto de línea

    # Columnas del reporte
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(40, 10, "Fecha", 1, 0, "C")
    pdf.cell(40, 10, "Cliente", 1, 0, "C")
    pdf.cell(40, 10, "Tarjeta", 1, 0, "C")
    pdf.cell(30, 10, "Monto", 1, 0, "C")
    pdf.cell(0, 10, "Productos", 1, 1, "C")

    # Detalles del reporte
    pdf.set_font("Arial", size=10)
    for item in report:
        pdf.cell(40, 10, item['DateOfSale'], 1, 0, "C")
        pdf.cell(40, 10, item['CustomerName'], 1, 0, "C")
        pdf.cell(40, 10, item['CreditCardUsed'], 1, 0, "C")
        pdf.cell(30, 10, f"${item['TotalAmount']:.2f}", 1, 0, "C")
        pdf.cell(0, 10, item['ProductsSold'], 1, 1, "C")

    # Guardar el archivo PDF
    pdf.output(file_name)
    print(f"Informe guardado como {file_name}")

def print_report(report):
    """
    Imprime el informe en un formato legible con encabezado.
    """
    if not report:
        print("No hay transacciones para el mes especificado.")
        return

    # Encabezado con nombre del empleado y fecha del reporte
    employee_name = report[0]['EmployeeName']
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Informe Mensual de Ventas")
    print(f"Empleado: {employee_name}")
    print(f"Fecha del Reporte: {report_date}")
    print("=" * 100)

    # Columnas de la tabla
    print(f"{'Fecha':<20}{'Cliente':<20}{'Tarjeta':<20}{'Monto':<10}{'Productos'}")
    print("=" * 100)

    # Detalles del reporte
    for item in report:
        print(
            f"{item['DateOfSale']:<20}"
            f"{item['CustomerName']:<20}"
            f"{item['CreditCardUsed']:<20}"
            f"{item['TotalAmount']:<10.2f}"
            f"{item['ProductsSold']}"
        )

# Funcion que calcula el Hash de un archivo con SHA-256
def calcular_hash(ruta_archivo):
    contenido = leer_archivo(ruta_archivo)

    hash_sha256 = hashlib.sha256()
    hash_sha256.update(contenido.encode('utf-8'))
    hash_hex256 = hash_sha256.hexdigest()

    print("Hash SHA-256:", hash_hex256)

    hash_bytes = hash_hex256.encode('utf-8')
    return hash_bytes

# Funcion que crea una firma con la llave privada de nuestro destinatario 
# y el hash de un archivo
def sign_hash(private_key_path, hash_data):
    with open(private_key_path, 'rb') as f:
        private_key = load_pem_private_key(
            f.read(),
            password=None
        )
    
    signature = private_key.sign(
        hash_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Funcion que guarda una firma dentro de los metadatos de un archivo
# Con el rol de quien lo firma
def guardar_firma(input_pdf, output_pdf, signature, remitente):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
        
    info_dict = reader.metadata
    new_info_dict = {**info_dict, remitente: signature.hex()}

    writer.add_metadata(new_info_dict)

    with open(output_pdf, 'wb') as f:
        writer.write(f)

# Funcion que verifica una firma de con la llave publica de las llaves RSA
def verify_signature(public_key_path, file_path, signature):
    with open(public_key_path, 'rb') as f:
        public_key = load_pem_public_key(f.read())
    
    file_hash = calcular_hash(file_path)
    print("Hash calculado con exito")
    try:
        public_key.verify(
            signature,
            file_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False

# Funcion que extrae la firma de los metadatos de un archivo
def extract_signature_from_pdf(signed_pdf, remitente):
    reader = PdfReader(signed_pdf)
    metadata = reader.metadata
    print(f"Metadatos del archivo: {metadata}")
    signature_hex = metadata.get(remitente)
    return bytes.fromhex(signature_hex) if signature_hex else None