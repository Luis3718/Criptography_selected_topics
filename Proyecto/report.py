from fpdf import FPDF
from datetime import datetime

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
