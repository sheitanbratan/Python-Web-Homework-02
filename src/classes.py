import re
from collections import UserDict
from datetime import datetime
from exceptions import *
# from .exceptions import *


class Field:

    def __init__(self, value):

        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError

    def __str__(self):
        return str(self.value)

    @staticmethod
    def is_valid(value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):

        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError


class Name(Field):
    pass


class Address(Field):
    pass


class Phone(Field):

    @staticmethod
    def is_valid(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    @staticmethod
    def is_valid(value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except:
            raise BadBirthdayFormat


class Email(Field):

    @staticmethod
    def is_valid(value):
        if bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value)):
            return True

        raise BadEmailFormat


class Record:
    def __init__(self, name, phone=None, birthday=None, address=None, email=None):
        self.name = Name(name)

        self.phones = []
        self.addresses = []
        self.emails = []

        if phone:
            self.phones.append(Phone(phone))

        if address:
            self.addresses.append(Address(address))

        self.birthday = Birthday(birthday) if birthday else None

        if email:
            self.emails.append(Email(email))

    def add_phone(self, phone):
        phone = Phone(phone)
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)

        return phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return self.birthday

    def add_address(self, address):
        address = Address(address)
        if address.value not in [a.value for a in self.addresses]:
            self.addresses.append(address)
            return self.address
        else:
            raise AddressIsExist

    def add_email(self, email):
        email = Email(email)
        if email.value not in [a.value for a in self.emails]:
            self.emails.append(email)
            return self.emails
        else:
            raise ValueError("Email already exists")

    def remove_address(self, address):
        len_before = len(self.addresses)
        self.addresses = [a for a in self.addresses if a.value != address]
        if len_before == len(self.addresses):
            raise AddressIsNotExist
        else:
            return self

    def days_to_birthday(self):

        if self.birthday:
            day_of_birthday = datetime.strptime(
                self.birthday.value, '%d.%m.%Y')
            today = datetime.today()
            data = day_of_birthday.replace(year=today.year)

            delta = data - today
            if delta.days < 0:
                data = data.replace(year=today.year + 1)
                delta = data - today

            return delta.days

        return None

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def edit_phone(self, old_phone, new_phone):
        Phone(new_phone)
        if self.remove_phone(old_phone) is not None:
            return self.add_phone(new_phone)
        return

    def edit_email(self, old_email, new_email):
        Email(new_email)

        if self.remove_email(old_email):
            return self.add_email(new_email)

    def find_phone(self, search):

        for phone in self.phones:
            if phone.value == search:
                return phone

        raise ValueError

    def remove_phone(self, phone):
        len_before = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone]
        if len_before == len(self.phones):
            return None
        return self

    def remove_email(self, email):
        len_before = len(self.emails)
        self.emails = [e for e in self.emails if e.value != email]
        if len_before == len(self.emails):
            return None
        return self

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {str(self.birthday)}, addresses: {'; '.join(str(a) for a in self.addresses)}, email: {'; '.join(str(a) for a in self.emails)}"

    def __repr__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):

        if str(record.name.value) not in self.data:
            self.data[str(record.name.value)] = record
            return record

        raise ContactAlreadyExists

    def find(self, name: str):  # -> Record:
        # inner method. not for user's search
        for key in self.data.keys():
            if name == key:
                return self.data[key]

    def iterator(self, n=2):
        values = list(self.data.values())
        for i in range(0, len(values), n):
            yield values[i:i+n]

    def delete(self, name) -> str:
        for person in self.data:

            if isinstance(person, Name):
                if str(person.value) == name:
                    self.data.pop(person)
                    return
            else:
                if person == name:
                    self.data.pop(person)
                    return
        return

    def search(self, text):
        searched_text = text.strip().lower()
        result = []
        if not searched_text:
            return result
        for record in self.data.values():
            if searched_text in str(record.name.value).lower()\
                    + ' '.join([phone.value for phone in record.phones])\
                    + ' '.join([address.value for address in record.addresses]):
                result.append(record)
        return result

    def edit_record(self, old_name, new_name: str):
        slot = self.find(new_name)
        if slot:
            return f'This name {slot} already exists!'
        record = self.find(old_name)
        if record:

            self.delete(str(record.name.value))
            record.edit_name(new_name)
            record = self.add_record(record)

        else:
            raise KeyError

        return record
