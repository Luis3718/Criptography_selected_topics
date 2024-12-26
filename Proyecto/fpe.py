import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Crypto.Random import get_random_bytes
from ff3 import FF3Cipher

def generate_salt() -> str:
    """
    Genera un salt único de 16 bytes en formato hexadecimal.
    """
    return get_random_bytes(16).hex()

def derive_key(password: str, salt: str, key_length: int = 16) -> str:
    """
    Deriva una clave de cifrado utilizando PBKDF2-HMAC-SHA256.
    :param password: Contraseña base para la derivación de la clave.
    :param salt: Salt único en formato hexadecimal.
    :param key_length: Longitud de la clave derivada en bytes (16 para AES-128).
    :return: Clave derivada en formato hexadecimal.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=bytes.fromhex(salt),
        iterations=100000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode()).hex()

def encrypt_card_number(card_number: str, password: str, salt: str, tweak: str = None) -> str:
    """
    Cifra un número de tarjeta de crédito utilizando FF3Cipher.
    :param card_number: Número de tarjeta en texto claro.
    :param password: Contraseña base para derivar la clave.
    :param salt: Salt único para la derivación de la clave.
    :param tweak: Tweak opcional de 16 caracteres.
    :return: Número cifrado en el mismo formato.
    """
    key = derive_key(password, salt)
    tweak = tweak or os.urandom(8).hex()  # Tweak de 64 bits (8 bytes)
    cipher = FF3Cipher(key, tweak)
    return cipher.encrypt(card_number)

def decrypt_card_number(encrypted_number: str, password: str, salt: str, tweak: str) -> str:
    """
    Descifra un número de tarjeta de crédito cifrado con FF3Cipher.
    :param encrypted_number: Número cifrado.
    :param password: Contraseña base para derivar la clave.
    :param salt: Salt único para la derivación de la clave.
    :param tweak: Tweak de 16 caracteres utilizado durante el cifrado.
    :return: Número de tarjeta en texto claro.
    """
    key = derive_key(password, salt)
    cipher = FF3Cipher(key, tweak)
    return cipher.decrypt(encrypted_number)

# Ejemplo de uso
if __name__ == "__main__":
    card_number = "4526167852314596"  # Número de tarjeta (16 dígitos)
    password = "securepassword"  # Contraseña para derivar la clave
    salt = generate_salt()  # Generar un salt único
    tweak = os.urandom(8).hex()  # Tweak de 8 bytes (64 bits)

    print(f"Salt: {salt}")
    print(f"Tweak: {tweak}")

    # Cifrar
    encrypted = encrypt_card_number(card_number, password, salt, tweak)
    print(f"Encrypted Card Number: {encrypted}")

    # Descifrar
    decrypted = decrypt_card_number(encrypted, password, salt, tweak)
    print(f"Decrypted Card Number: {decrypted}")
