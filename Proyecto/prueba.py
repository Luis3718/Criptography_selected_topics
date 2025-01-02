import ECDSA 
import report
from admin import calcular_hash

file1 = "Proyecto/reports/Reporte_2024-09_7_signed.pdf"
file2 = "Proyecto/reports/Reporte_2024-09_7_signed copy.pdf"

# Asegúrate de que ambos archivos tengan el mismo contenido binario
hash1 = calcular_hash(file1)
hash2 = calcular_hash(file2)

print(f"Hash de {file1}: {hash1.hex()}")
print(f"Hash de {file2}: {hash2.hex()}")

if hash1 == hash2:
    print("El nombre del archivo NO afecta el hash.")
else:
    print("El nombre del archivo afecta el hash.")
