import re
import pickle  # Для серіалізації/десеріалізації об'єктів

class ContactBook:
    def __init__(self, file_path):
        self.contacts = {}
        self.file_path = file_path
        self.load_contacts()

    def add_contact(self, name, phone):
        if name not in self.contacts:
            self.contacts[name] = phone
            self.save_contacts()
            return f"Added {name} with phone number {phone}"
        else:
            return f"Contact {name} already exists. Use 'change' command to update the phone number."

    def change_phone(self, name, new_phone):
        if name in self.contacts:
            self.contacts[name] = new_phone
            self.save_contacts()
            return f"Changed phone number for {name} to {new_phone}"
        else:
            return f"Contact {name} not found"

    def find_phone(self, query):
        results = []
        for name, phone in self.contacts.items():
            if query.lower() in name.lower() or query in phone:
                results.append(f"{name}: {phone}")
        if results:
            return "\n".join(results)
        else:
            return f"No matching contacts for '{query}'"

    def show_all(self):
        return "\n".join([f"{name}: {phone}" for name, phone in self.contacts.items()])

    def close(self):
        self.save_contacts()
        return "Good bye!"

    def load_contacts(self):
        try:
            with open(self.file_path, 'rb') as file:
                self.contacts = pickle.load(file)
        except (FileNotFoundError, EOFError):
            # Ignore if the file doesn't exist or is empty
            pass

    def save_contacts(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.contacts, file)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return wrapper

def parse_command(command):
    # Залиште цю функцію без змін

def handle_command(contact_book, command):
    # Залиште цю функцію без змін

def main():
    contact_book = ContactBook("contacts.pkl")  # Зазначте свій шлях та ім'я файлу
    while True:
        command = input("Enter command: ")
        parsed_command = parse_command(command)
        if parsed_command == "close":
            print("Good bye!")
            break
        response = handle_command(contact_book, parsed_command)
        print(response)

if __name__ == "__main__":
    main()
