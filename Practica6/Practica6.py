"""
  ECDSA for real implementations
  Instituto Polit�cnico Nacional
  ESCOM
  Alvarado Romero Luis Manuel   
  Materia: Ciptografia
  Grupo: 7CM1
"""
import ast
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.hazmat.primitives import serialization

Ruta = "Practica6/"

# Function para generar las llaves de ECDSA
def Generate_keys(Curva):
    # Dentro de los argummentos de la funcion se pueden agregar el tipo de curva
    private_key = ec.generate_private_key(Curva)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Escribir los archivos de llave
    with open(Ruta+"Private_key.txt", "wb") as private_file:
        private_file.write(private_pem)

    with open(Ruta+"Public_key.txt", "wb") as public_file:
        public_file.write(public_pem)

    print("Las llaves han sido generadas y guardadas en los archivos Private_key.txt y Public_key.txt")

# Function para firmar el mensaje
def Sign_message(Mensaje, Private_key_file):

    with open(Private_key_file, "rb") as private_file:
        private_key_pem = private_file.read()

    # Cargamos la llave privada en formato PEM
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )

    # Firmamos el mensaje ya hasheado con sha 256
    signature = private_key.sign(
        Mensaje,
        ec.ECDSA(hashes.SHA256())
    )

    # Obtenemos los valores de r y s
    r, s = decode_dss_signature(signature)

    return (r, s)

# Funcion para verificar la firma
def Verify_signature(Mensaje, r, s, Public_key_file):
    # Leemos la llave publica
    with open(Public_key_file, "rb") as public_file:
        public_key_pem = public_file.read()

    # Load the public key from PEM
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Regresamos los valores de nuestra firma al formato DER
    signature = encode_dss_signature(r, s)
    
    # Validamos la firma
    try:
        public_key.verify(
            signature,
            Mensaje,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception:
        return False

def opcion_1():
    opciones = {
    1: ec.SECP256R1,
    2: ec.SECP384R1,
    3: ec.SECP521R1 
    }   
    opcion=int(input("Curvas: \n 1- P-256\n 2- P-348\n 3- P-521\nQue curva deseas usar: "))
    if opcion in opciones:
        curva=opciones[opcion]()
        Generate_keys(curva)
        Mensaje=input("Ingresa el mensaje: ")
        Mensaje=Mensaje.encode('utf-8')
        r, s = Sign_message(Mensaje, Ruta+"private_key.txt")
        Signature=(r,s)
        with open(Ruta+"Firma.txt", 'w+') as archivo:
            archivo.write(str(Signature))
        print(f"Signature (r, s): (r={r}, s={s})")
    else:
        print("Esa curva no se encuentra en las opciones")

def opcion_2():
    Mensaje=input("Ingresa el mensaje: ")
    Mensaje=Mensaje.encode('utf-8')
    with open(Ruta+"Firma.txt", "r") as file:
      firma = file.read()
    firma = ast.literal_eval(firma)
    if Verify_signature(Mensaje,firma[0],firma[1],Ruta+"Public_key.txt")==True:
        print("Firma valida")
    else: 
        print("Firma no valida")

def salir():
    print("Saliendo del programa...")
    exit()

def main():
    
  opciones = {
    '1': opcion_1,
    '2': opcion_2,
    '3': salir
}

  while True:
    print("\n Menú:")
    print("1. Generacion de llaves y firma ECDSA")
    print("2. Verificacion de firma ECDSA")
    print("3. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
