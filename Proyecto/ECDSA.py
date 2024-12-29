from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature

def generate_ecdsa_keys():
    # Generar una nueva llave privada
    private_key = ec.generate_private_key(ec.SECP256R1())
    # Extraer la llave pública
    public_key = private_key.public_key()

    # Serializar la llave privada
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serializar la llave pública
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem.decode('utf-8'), public_key_pem.decode('utf-8')

def calcular_hash(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        contenido = f.read()
    digest = hashes.Hash(hashes.SHA256())
    digest.update(contenido)
    return digest.finalize()

def sign_data(private_key_pem, data):
    # Cargar la llave privada desde PEM
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None
    )
    # Firmar los datos
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def verify_signature(public_key_pem, data, signature):
    # Cargar la llave pública desde PEM
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8')
    )
    # Verificar la firma
    try:
        public_key.verify(
            signature,
            data,
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
