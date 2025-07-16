import hashlib
import os

# Passwort-Hashing
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return password_hash, salt

# Abbruchbestätigung
def confirm_quit():
    response = input("Sind Sie sicher, dass Sie das Spiel beenden möchten? (j/n): ")
    return response.lower() == 'j'