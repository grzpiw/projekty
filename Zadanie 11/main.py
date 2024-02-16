from collections import UserDict
import re
import pickle

class Field:
    """Base class for entry fields."""
    def __init__(self, value):
        self.value = value

class Name(Field):
    """Class for first and last name."""
    pass

class Phone(Field):
    """Class for phone number with validation."""
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Niepoprawny numer telefonu")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        """Checks if the phone number is valid (9 digits, format 123456789)."""
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None

class Email(Field):
    """Class for email address with validation."""
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Niepoprawny adres email")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        """Checks if the email is valid."""
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None

class Record:
    """Class for an entry in the address book."""
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.emails = []

    def add_phone(self, phone: Phone):
        """Adds a phone number."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Removes a phone number."""
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Changes a phone number."""
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        """Adds an email address."""
        self.emails.append(email)

    def remove_email(self, email: Email):
        """Removes an email address."""
        self.emails.remove(email)

    def edit_email(self, old_email: Email, new_email: Email):
        """Changes an email address."""
        self.remove_email(old_email)
        self.add_email(new_email)

    def edit_name(self, new_name: Name):
        """Changes the first and last name."""
        self.name = new_name

    def __str__(self):
        """Returns a string representation of the entry."""
        phones = ', '.join(phone.value for phone in self.phones)
        emails = ', '.join(email.value for email in self.emails)
        return f"Imię i nazwisko: {self.name.value}, Telefony: {phones}, Email: {emails}"

class AddressBook(UserDict):
    """Class for the address book."""
    def add_record(self, record: Record):
        """Adds an entry to the address book."""
        self.data[record.name.value] = record
        print("Dodano wpis.")

    def find_record(self, search_term):
        """Finds entries containing the exact phrase provided."""
        found_records = []
        for record in self.data.values():
            if search_term.lower() in record.name.value.lower():
                found_records.append(record)
                continue
            for phone in record.phones:
                if search_term in phone.value:
                    found_records.append(record)
                    break
            for email in record.emails:
                if search_term in email.value:
                    found_records.append(record)
                    break
        return found_records

    def delete_record(self, name):
        """Deletes a record by name."""
        if name in self.data:
            del self.data[name]
            print(f"Usunięto wpis: {name}.")
        else:
            print(f"Wpis o nazwie {name} nie istnieje.")

    def show_all_records(self):
        """Displays all entries in the address book."""
        if not self.data:
            print("Książka adresowa jest pusta.")
            return
        for name, record in self.data.items():
            print(record)


def edit_record(book):
    """Edits an existing record in the address book."""
    name_to_edit = input("Wprowadź imię i nazwisko które chcesz edytować: ")
    if name_to_edit in book.data:
        record = book.data[name_to_edit]
        print(f"Edytowanie: {name_to_edit}.")

        new_name_input = input("Podaj imię i nazwisko (wciśnij Enter żeby zachować obecne): ")
        if new_name_input.strip():
            record.edit_name(Name(new_name_input))
            print("Zaktualizowano imię i nazwisko.")

        if record.phones:
            print("Obecne numery telefonów: ")
            for idx, phone in enumerate(record.phones, start=1):
                print(f"{idx}. {phone.value}")
            phone_to_edit = input("Wprowadź indeks numeru telefonu który chcesz edytować "
                                  "(wciśnij Enter żeby zachować obecny): ")
            if phone_to_edit.isdigit():
                idx = int(phone_to_edit) - 1
                if 0 <= idx < len(record.phones):
                    new_phone_number = input("Podaj nowy numer telefonu: ")
                    if new_phone_number.strip():
                        record.edit_phone(record.phones[idx], Phone(new_phone_number))
                        print("Numer telefonu zaktualizowany.")
                    else:
                        print("Nie dokonano zmian.")
                else:
                    print("Niepoprawny indeks numeru.")
            else:
                print("Pomięto edycję numeru.")
        else:
            print("Brak numerów telefonu.")

        print("Wpis zaktualizowany.")
    else:
        print("Wpisu nie znaleziono.")

def save_address_book(book, filename='address_book.pkl'):
    """Saves the address book to a file."""
    with open(filename, 'wb') as file:
        pickle.dump(book.data, file)
    print("Zapisano książkę adresową.")

def load_address_book(filename='address_book.pkl'):
    """Restores the address book from a file."""
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            book = AddressBook()
            book.data = data
            print("Przywrócono książkę adresową.")
            return book
    except FileNotFoundError:
        print("Plik nie istnieje, tworzenie nowej książki adresowej.")
        return AddressBook()

def input_phone():
    """Asks the user to enter a phone number."""
    while True:
        try:
            number = input("Podaj numer telefonu w formacie '123456789' (naciśnij Enter, aby pominąć): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)

def input_email():
    """Asks the user to enter an email address."""
    while True:
        try:
            address = input("Podaj adres email (naciśnij Enter, aby pominąć): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)

def create_record():
    """Creates an entry in the address book based on user input."""
    while True:
        name_input = input("Podaj imię i nazwisko: ")
        if name_input.strip():
            name = Name(name_input)
            break
        else:
            print("Pole imię i nazwisko jest wymagane.")
    record = Record(name)
    while True:
        phone = input_phone()
        if phone:
            record.add_phone(phone)
            decision = input("Dodać kolejny numer? (tak/nie) ").lower()
            if decision not in ["tak", "t"]:
                break
        else:
            break
    while True:
        email = input_email()
        if email:
            record.add_email(email)
            decision = input("Dodać kolejny email? (tak/nie) ").lower()
            if decision not in ["tak", "t"]:
                break
        else:
            break
    return record

def main():
    """The main app function"""
    book = load_address_book()
    while True:
        action = input("Wybierz akcję: dodaj (d), znajdź (z), usuń (u), edytuj (e), pokaż wszystkie (p) koniec (q): ")
        if action == "dodaj" or action == "d":
            record = create_record()
            book.add_record(record)
        elif action == 'znajdź' or action == "z":
            search = input("Wpisz szukaną frazę: ")
            found = book.find_record(search)
            for record in found:
                print(record)
        elif action == 'usuń' or action == "u":
            name = input("Podaj imię i nazwisko do usunięcia: ")
            book.delete_record(name)
        elif action in ["edytuj", "edycja", "e"]:
            edit_record(book)
        elif action in ["pokaż wszystkie", "pokaż", "pokaz", "p"]:
            book.show_all_records()
        elif action in ["koniec", "q"]:
            save_address_book(book)
            break

if __name__ == "__main__":
    main()