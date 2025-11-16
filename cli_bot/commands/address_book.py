from collections import UserDict 
from datetime import datetime, timedelta, date
import re
from colorama import Fore, Style

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Address(Field):
    def __init__(self, address):
        super().__init__(address)


class Email(Field):
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def __init__(self, email: str):
        email = email.strip()
        if not self.EMAIL_PATTERN.match(email):
            raise ValueError("Некоректна адреса електронної пошти.")
        super().__init__(email)


class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        new_value = new_value.strip()
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Номер телефону має бути до 10 символів.")
        self._value = new_value

    def __str__(self):
        return self._value


class Record:
    def __init__(self, name : str):
        self.name = Name(name)
        self.phones : list[Phone] = []
        self.birthday : Birthday = None
        self.address : Address = None
        self.emails : list[Email] = []

    def add_phone(self, phone):
        try:
            if self.find_phone(phone):
                return "Такий номер вже існує у цьому контакті."
            self.phones.append(Phone(phone))
            return "Телефон додано."
        except ValueError as e:
            return f"Невірний номер: {e}"
    
    def remove(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Телефон {phone} видалено."
        return f"Телефон {phone} не знайдено."
    
    def edit_phone(self,old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                if any(existing.value == new_phone and existing.value != old_phone for existing in self.phones):
                    return f"Номер {new_phone} вже існує у цьому контакті."
                try:
                    p.value = new_phone
                    return f'Старий номер : {old_phone} був змінений на {new_phone}.'
                except ValueError as er:
                    return f"Невірний номер: {er}"
        return 'Телефон не знайдено.'
    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def find_email(self, email: str):
        target = email.strip().casefold()
        for em in self.emails:
            if em.value.casefold() == target:
                return em
        return None
    
    def add_birthday(self,birthday:str):
        if self.birthday is not None:
            return f"У контакту '{self.name.value}' вже вказано день народження: {self.birthday}"
        return self._set_birthday(birthday, "Дату народження додано.")

    def change_birthday(self, birthday: str):
        return self._set_birthday(birthday, "Дату народження оновлено.")

    def _set_birthday(self, birthday: str, success_message: str):
        try:
            self.birthday = Birthday(birthday)
            return success_message
        except ValueError as er:
            return str(er)

    def add_address(self, address: str):
        return self._set_address(address, "Адресу додано.")

    def change_address(self, address: str):
        return self._set_address(address, "Адресу оновлено.")

    def _set_address(self, address: str, success_message: str):
        normalized = " ".join(address.split())
        if not normalized:
            return "Будь ласка, введіть адресу."
        self.address = Address(normalized)
        return success_message

    def add_email(self, email: str):
        if self.find_email(email):
            return "Такий email вже існує у цьому контакті."
        try:
            email_obj = Email(email)
            self.emails.append(email_obj)
            return "Email додано."
        except ValueError as er:
            return f"Невірний email: {er}"

    def change_name(self, book, new_name: str):
        new_name = new_name.strip()
        if not new_name:
            return "Нове ім'я не може бути порожнім."
        current_name = self.name.value
        if new_name == current_name:
            return "Нове ім'я збігається з поточним."
        if book.find(new_name):
            return f"Контакт з ім'ям '{new_name}' вже існує."
        del book.data[current_name]
        self.name = Name(new_name)
        book.add_record(self)
        return f"Ім'я контакту змінено на {new_name}."

    def edit_email(self, old_email: str, new_email: str):
        normalized_old = old_email.strip().casefold()
        normalized_new = new_email.strip().casefold()
        for idx, email in enumerate(self.emails):
            if email.value.casefold() == normalized_old:
                if any(
                    existing.value.casefold() == normalized_new and i != idx
                    for i, existing in enumerate(self.emails)
                ):
                    return f"Email {new_email} вже існує у цьому контакті."
                try:
                    self.emails[idx] = Email(new_email)
                    return f"Email {old_email} змінено на {new_email}."
                except ValueError as er:
                    return f"Невірний email: {er}"
        return f"Email {old_email} не знайдено."
    
    def __str__(self):
        name_colored = Fore.MAGENTA + self.name.value + Style.RESET_ALL

        if self.phones:
            phones = Fore.MAGENTA + '; '.join(phone.value for phone in self.phones) + Style.RESET_ALL
            phones = f"\n\tтелефони: {phones}"
        else:
            phones = ""

        if self.birthday:
            birthday = Fore.MAGENTA + str(self.birthday) + Style.RESET_ALL
            birthday = f"\n\tдень народження: {birthday}"
        else:
            birthday = ""

        if self.address:
            address = Fore.MAGENTA + str(self.address) + Style.RESET_ALL
            address = f"\n\tадреса: {address}"
        else:
            address = ""

        if self.emails:
            emails = Fore.MAGENTA + '; '.join(email.value for email in self.emails) + Style.RESET_ALL
            emails = f"\n\tімейли: {emails}"
        else:
            emails = ""

        return f"Контакт: {name_colored}{phones}{birthday}{address}{emails}"
    
    
class Birthday(Field):
    def __init__(self, value:str):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(birthday_date)
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class AddressBook(UserDict): 
    def add_record(self, record):
        self.data[record.name.value] = record
        return
    
    def find(self, name):
        return self.data.get(name)

    def find_record_by_phone(self, phone: str):
        for record in self.data.values():
            if record.find_phone(phone):
                return record
        return None

    def find_record_by_email(self, email: str):
        target = email.strip().casefold()
        for record in self.data.values():
            for em in record.emails:
                if em.value.casefold() == target:
                    return record
        return None
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Запис {name} видалено."
        return f"{name} не знайдено."
    
    def get_upcomming_birthdays(self):
        today = date.today()
        horizon = today + timedelta(days=7)
        upcoming = []

        for record in self.data.values():
            if not getattr(record, "birthday", None):
                continue

            original_birthday = record.birthday.value

            birthday_this_year = original_birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            congrats_date = birthday_this_year
            if congrats_date.weekday() >= 5:
                days_to_monday = 7 - congrats_date.weekday()
                congrats_date = congrats_date + timedelta(days=days_to_monday)

            if today <= congrats_date <= horizon:
                upcoming.append({
                    "name": record.name.value,
                    "congrats_date": congrats_date,
                    "birthday": original_birthday,
                })

        upcoming.sort(key=lambda x: (x["congrats_date"], x["name"]))
        return upcoming
