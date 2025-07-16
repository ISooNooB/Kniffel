import sqlite3
from Funktions import hash_password
from getpass import getpass

# Benutzerregistrierung
def register_user():
    username = input("Benutzername: ")
    password = getpass("Passwort: ")
    confirm_password = getpass("Passwort bestätigen: ")

    if password != confirm_password:
        print("Passwörter stimmen nicht überein!")
        return False

    conn = sqlite3.connect('kniffel.db')
    cursor = conn.cursor()

    try:
        password_hash, salt = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
            (username, password_hash, salt)
        )
        conn.commit()
        print("Registrierung erfolgreich!")
        return True
    except sqlite3.IntegrityError:
        print("Benutzername existiert bereits!")
        return False
    finally:
        conn.close()

# Benutzeranmeldung
def login_user():
    username = input("Benutzername: ")
    password = getpass("Passwort: ")

    conn = sqlite3.connect('kniffel.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        print("Ungültiger Benutzername oder Passwort!")
        return None

    stored_hash, salt = result
    input_hash, _ = hash_password(password, salt)

    if input_hash == stored_hash:
        print("Anmeldung erfolgreich!")
        return username
    else:
        print("Ungültiger Benutzername oder Passwort!")
        return None