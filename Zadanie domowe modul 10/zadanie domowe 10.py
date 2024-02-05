from collections import UserDict
import re

class Field:
    """Base class for entry fields."""
    def __init__(self, value):
        self.value = value

class Name(Field):
    """Class for name field."""
    pass

class Phone(Field):
    """Class for phone number field with validation."""
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        """Check if the phone number is valid (9 digits, format 123456789)."""
        pattern = re.compile(r"^\d{9}$")
        return pattern.match(value) is not None

class Email(Field):
    """Class for email address field with validation."""
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email address")
        super().__init__(value)

    @staticmethod
    def validate_email(value):
        """Check if the email address is valid."""
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return pattern.match(value) is not None

class Record:
    """Class for an entry in the address book."""
    def __init__(self, name: Name):
        self.name = name
        self.phones = []
        self.emails = []

    def add_phone(self, phone: Phone):
        """Add a phone number."""
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        """Remove a phone number."""
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        """Change a phone number."""
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_email(self, email: Email):
        """Add an email address."""
        self.emails.append(email)

    def remove_email(self, email: Email):
        """Remove an email address."""
        self.emails.remove(email)

    def edit_email(self, old_email: Email, new_email: Email):
        """Change an email address."""
        self.remove_email(old_email)
        self.add_email(new_email)

    def edit_name(self, new_name: Name):
        """Change the name."""
        self.name = new_name

    def __str__(self):
        """Return a string representation of the entry."""
        phones = ', '.join(phone.value for phone in self.phones)
        emails = ', '.join(email.value for email in self.emails)
        return f"Name: {self.name.value}, Phones: {phones}, Email: {emails}"

class AddressBook(UserDict):
    """Class for the address book."""
    def add_record(self, record: Record):
        """Add a record to the address book."""
        self.data[record.name.value] = record
        print(f"Record added.")

    def find_record(self, search_term):
        """Find entries containing the exact given phrase."""
        found_records = []
        for record in self.data.values():
            if search_term.lower() == record.name.value.lower():
                found_records.append(record)
                continue
            for phone in record.phones:
                if search_term == phone.value:
                    found_records.append(record)
                    break
            for email in record.emails:
                if search_term == email.value:
                    found_records.append(record)
                    break
        return found_records

    def delete_record(self, name):
        """Delete a record with the given name."""
        if name in self.data:
            del self.data[name]
            print(f"Record deleted: {name}.")
        else:
            print(f"No record with the name {name} exists.")

# Input functions for user interaction
def input_phone():
    """Prompt the user to enter a phone number."""
    while True:
        try:
            number = input("Enter a phone number in the format '123456789' (press Enter to skip): ")
            if not number:
                return None
            return Phone(number)
        except ValueError as e:
            print(e)

def input_email():
    """Prompt the user to enter an email address."""
    while True:
        try:
            address = input("Enter an email address (press Enter to skip): ")
            if not address:
                return None
            return Email(address)
        except ValueError as e:
            print(e)

def create_record():
    """Create an entry for the address book based on user input."""
    while True:
        name_input = input("Enter a name: ")
        if name_input.strip():
            name = Name(name_input)
            break
        else:
            print("Name is required.")
    record = Record(name)
    while True:
        phone = input_phone()
        if phone:
            record.add_phone(phone)
            decision = input("Add another phone number? (yes/no) ").lower()
            if decision not in ["yes", "y"]:
                break
        else:
            break
    while True:
        email = input_email()
        if email:
            record.add_email(email)
            decision = input("Add another email? (yes/no) ").lower()
            if decision not in ["yes", "y"]:
                break
        else:
            break
    return record

def main():
    """Main program function."""
    book = AddressBook()
    while True:
        action = input("Choose an action: add (a), find (f), delete (d), quit (q): ")
        if action == "add" or action == "a":
            record = create_record()
            book.add_record(record)
        elif action == 'find' or action == "f":
            search = input("Enter the search term: ")
            found = book.find_record(search)
            for record in found:
                print(record)
        elif action == 'delete' or action == "d":
            name = input("Enter the name to delete: ")
            book.delete_record(name)
        elif action == 'quit' or action == "q":
            break

if __name__ == "__main__":
    main()
