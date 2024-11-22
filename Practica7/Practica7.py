"""
  Schoolbook RSA
  Instituto Polit�cnico Nacional
  ESCOM
  Alvarado Romero Luis Manuel   
  Materia: Ciptografia
  Grupo: 7CM1
"""
import secrets
import random
from sympy import gcd, mod_inverse
from sympy import primerange
from sympy import isprime
from base64 import b64encode, b64decode

Ruta = "Practica7/"

# Función que genera un número primo de 1024 bits
def generar_primo_grande(bits):
    while True:
        numero = secrets.randbits(bits)
        if isprime(numero):
            return numero

# Funcion que calcula el inverso multiplicativo de un numero
def calcular_inverso(num1,num2):
    try:
        inverse = mod_inverse(num1, num2)
        #print("Inverso multiplicativo:", inverse)
        return inverse
    except ValueError:
        print("No existe inverso multiplicativo")

# Funcion que genera las llaves de RSA
def generar_llaves(num1,num2):
    n=num1*num2
    phi=(num1-1)*(num2-1)
    while True:
        e=random.randint(1,phi)
        gcd_value = gcd(e, phi)
        #print("GCD:", gcd_value)
        if gcd_value==1:
            break
    d=calcular_inverso(e, phi)
    public_key=(e,n)
    private_key=(d,n)

    return public_key, private_key

# Funcion que convierte la llave en base 64
def encode_key_to_base64(key):
    e_or_d, n = key
    key_bytes = f"{e_or_d},{n}".encode('utf-8')
    return b64encode(key_bytes).decode('utf-8')

# Funcion que crea un archivo de las llaves
def Crear_archivo_llave(filename, key_base64):
    with open(Ruta+filename, 'w') as file:
        file.write(key_base64)

# Funcion que lee las llaves de RSA
def cargar_llave(filename):
     with open(Ruta+filename, 'r') as file:
        key_base64 = file.read()
        key_bytes = b64decode(key_base64).decode('utf-8')
        e_or_d, n = map(int, key_bytes.split(','))
        return (e_or_d, n)

# Funcion que realiza el cifrado de un mensaje con RSA
def Cifrado_RSA(public_key, message):
    e, n = public_key
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    # RSA Cifrado = (message ^ e) % n
    ciphertext_int = pow(message_int, e, n)
    ciphertext_bytes = ciphertext_int.to_bytes((ciphertext_int.bit_length() + 7) // 8, byteorder='big')
    return b64encode(ciphertext_bytes).decode('utf-8')

# Funcion que realiza el descifrado de un mensaje cifrado con RSA
def Descifrado_RSA(private_key, ciphertext_base64):
    d, n = private_key
    ciphertext_bytes = b64decode(ciphertext_base64)
    ciphertext_int = int.from_bytes(ciphertext_bytes, byteorder='big')
    # RSA descifrado = (ciphertext ^ d) % n
    message_int = pow(ciphertext_int, d, n)
    message_bytes = message_int.to_bytes((message_int.bit_length() + 7) // 8, byteorder='big')
    return message_bytes.decode('utf-8')


def opcion_1():
    p=generar_primo_grande(512)
    q=generar_primo_grande(512)
    public_key, private_key = generar_llaves(p, q)
    print("Public Key:", public_key)
    print("Private Key:", private_key)

    public_key_base64 = encode_key_to_base64(public_key)
    private_key_base64 = encode_key_to_base64(private_key)

    print("Public Key (Base64):", public_key_base64)
    print("Private Key (Base64):", private_key_base64)

    Crear_archivo_llave('public_key.txt', public_key_base64)
    Crear_archivo_llave('private_key.txt', private_key_base64)

    Mensaje=input("Ingresa el mensaje a cifrar: ")
    Cifrado=Cifrado_RSA(public_key,Mensaje)
    with open(Ruta+"Cifrado.txt", 'w') as file:
        file.write(Cifrado)


def opcion_2():
    cargada_private_key = cargar_llave('private_key.txt')
    print("Private Key:", cargada_private_key)
    Archivo=input("Ingresa el nombre del archivo cifrado con su extencion: ")
    with open(Ruta+Archivo, "r") as file:
      Cifrado = file.read()
    Mensaje=Descifrado_RSA(cargada_private_key, Cifrado)
    print(f"Mensaje: \n{Mensaje}")

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
    print("1. Generacion de llaves y cifrado RSA")
    print("2. Descifrar mensaje RSA")
    print("3. Salir\n")
    seleccion = input("Selecciona una opción: ")

    if seleccion in opciones:
      opciones[seleccion]()
    else:
      print("Opción no válida. Por favor, selecciona una opción del menú.")

if __name__ == "__main__":
    main()
