from fpdf import FPDF
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.exceptions import InvalidSignature

def save_report_to_pdf(report, file_name="monthly_report.pdf"):
    """
    Guarda el informe en un archivo PDF.
    """
    if not report:
        print("No hay transacciones para el mes especificado.")
        return

    # Inicializar el objeto PDF en formato horizontal
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado del reporte
    employee_name = report[0]['EmployeeName']
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt="Informe Mensual de Ventas", ln=True, align="C")
    pdf.ln(10)  # Salto de línea

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Empleado: {employee_name}", ln=True, align="L")
    pdf.cell(0, 10, txt=f"Fecha del Reporte: {report_date}", ln=True, align="L")
    pdf.ln(10)  # Salto de línea

    # Columnas del reporte
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(50, 10, "Fecha", 1, 0, "C")
    pdf.cell(50, 10, "Cliente", 1, 0, "C")
    pdf.cell(50, 10, "Tarjeta", 1, 0, "C")
    pdf.cell(40, 10, "Monto", 1, 0, "C")
    pdf.cell(0, 10, "Productos", 1, 1, "C")

    # Detalles del reporte
    pdf.set_font("Arial", size=10)
    for item in report:
        pdf.cell(50, 10, item['DateOfSale'], 1, 0, "C")
        pdf.cell(50, 10, item['CustomerName'], 1, 0, "C")
        pdf.cell(50, 10, item['CreditCardUsed'], 1, 0, "C")
        pdf.cell(40, 10, f"${item['TotalAmount']:.2f}", 1, 0, "C")
        pdf.cell(0, 10, item['ProductsSold'], 1, 1, "C")

    # Guardar el archivo PDF
    pdf.output(file_name)
    print(f"Informe guardado como {file_name}")

def calcular_hash(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()
    digest = hashes.Hash(hashes.SHA256())
    digest.update(contenido)
    return digest.finalize()

def sign_data(private_key_pem, hash_data):
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None
    )
    signature = private_key.sign(
        hash_data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

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

def extract_signature_from_pdf(signed_pdf, remitente):
    reader = PdfReader(signed_pdf)
    metadata = reader.metadata
    signature_hex = metadata.get(remitente)
    return bytes.fromhex(signature_hex) if signature_hex else None

def verify_signature(public_key_pem, file_path, signature):
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8')
    )
    hash_data = calcular_hash(file_path)

    try:
        public_key.verify(
            signature,
            hash_data,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
