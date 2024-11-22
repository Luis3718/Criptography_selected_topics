import hashlib
import os

def hash_password(password: str) -> str:
    # Generate a random salt
    salt = os.urandom(16).hex()  # Convert binary salt to hex
    # Hash the password combined with the salt
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed_password}"

def verify_password(password: str, stored_hash: str) -> bool:
    # Split the stored hash into salt and hashed password
    salt, hashed_password = stored_hash.split("$")
    # Hash the provided password with the stored salt
    test_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return test_hash == hashed_password
