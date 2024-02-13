from collections import UserDict
from datetime import datetime
import pickle 

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.value = value

    def is_valid(self, value):
        return isinstance(value, str) and value.isdigit() and len(value) == 10

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid phone number format")
        self.__value = new_value

class Birthday(Field):
    def __init__(self, value):
        self._set_value(value)

    def is_valid(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")
        self.__value = new_value

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_phone_number, new_phone_number):
        if not (isinstance(new_phone_number, str) and new_phone_number.isdigit() and len(new_phone_number) == 10):
            raise ValueError("Invalid new phone number format")

        found = False
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                found = True
                break

        if not found:
            raise ValueError(f"Phone number {old_phone_number} not found")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, *map(int, self.birthday.value.split('-'))).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split('-'))).date()
            days_left = (next_birthday - today).days
            return days_left
        return None

class AddressBook(UserDict):
    def __init__(self, file_path='address_book.pkl'):
        super().__init__()
        self.file_path = file_path
        self.data = self.load_address_book()

    def load_address_book(self):
        try:
            with open(self.file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

    def save_address_book(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, chunk_size=5):
        all_records = list(self.data.values())
        for i in range(0, len(all_records), chunk_size):
            yield all_records[i:i + chunk_size]

class ContactBook:
    def __init__(self, address_book):
        self.address_book = address_book

    def add_contact(self, name, phone):
        if name not in self.address_book.data:
            record = Record(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
            return f"Added {name} with phone number {phone}"
        else:
            return f"Contact {name} already exists. Use 'change' command to update the phone number."

    def change_phone(self, name, new_phone):
        record = self.address_book.find(name)
        if record:
            record.add_phone(new_phone)
            return f"Changed phone number for {name} to {new_phone}"
        else:
            return f"Contact {name} not found"

    def find_phone(self, name):
        record = self.address_book.find(name)
        if record:
            phones_str = '; '.join(str(phone) for phone in record.phones)
            return f"Phone number for {name} is {phones_str}"
        else:
            return f"Contact {name} not found"

    def show_all(self):
        return "\n".join([str(record) for record in self.address_book.data.values()])

    def close(self):
        self.address_book.save_address_book()  # Зберегти дані перед виходом
        return "Good bye!"

# Решта коду незмінна

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)
    return wrapper

def parse_command(command):
    # Решта коду незмінна

def handle_command(contact_book, command):
    # Решта коду незмінна

def main():
    address_book = AddressBook()
    contact_book = ContactBook(address_book)

    while True:
        command = input("Enter command: ")
        parsed_command = parse_command(command)
        
        if parsed_command == "close":
            print(contact_book.close())
            break

        response = handle_command(contact_book, parsed_command)
        print(response)

if __name__ == "__main__":
    main()
