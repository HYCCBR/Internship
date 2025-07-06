import os
import sys
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

class Encryptor:
    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, message: str) -> str:
        return self.fernet.encrypt(message.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.fernet.decrypt(token.encode()).decode()

def write_note(file_path, note, encryptor):
    encrypted_note = encryptor.encrypt(note)
    with open(file_path, 'a') as file:
        file.write(encrypted_note + '\n')

def read_notes(file_path, encryptor):
    decrypted_notes = []
    try:
        with open(file_path, 'r') as file:
            encrypted_notes = file.readlines()
            for encrypted_note in encrypted_notes:
                decrypted_note = encryptor.decrypt(encrypted_note.strip())
                decrypted_notes.append(decrypted_note)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading notes: {e}")
    return decrypted_notes

def main():
    key = load_key()
    encryptor = Encryptor(key)
    notes_file = 'notes.txt'

    while True:
        print("Welcome to the Notes CLI App!")
        print("1. Write a note")
        print("2. Read notes")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            note = input("Enter your note: ")
            write_note(notes_file, note, encryptor)
            print("Note saved successfully!")

        elif choice == '2':
            if os.path.exists(notes_file):
                decrypted_notes = read_notes(notes_file, encryptor)
                print("Your notes:")
                for note in decrypted_notes:
                    print(f"- {note}")
            else:
                print("No notes found.")

        elif choice == '3':
            print("Exiting the application. Goodbye!")
            sys.exit()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()