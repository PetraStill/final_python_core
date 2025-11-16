"""Модуль доменної логіки для адресної книги.

Містить класи:
- Field, Name, Address, Email, Phone — поля запису.
- Record — окремий контакт.
- Birthday — дата народження.
- AddressBook — колекція контактів та робота з ними.
"""

from collections import UserDict
from datetime import datetime, timedelta, date
import re
from colorama import Fore, Style


class Field:
    """Базовий клас для полів запису (значення, що виводиться як текст)."""

    def __init__(self, value):
        """Ініціалізує поле значенням.

        Args:
            value: Будь-яке значення, яке можна перетворити на рядок.
        """
        self.value = value

    def __str__(self):
        """Повертає рядкове представлення значення поля."""
        return str(self.value)


class Name(Field):
    """Поле для зберігання імені контакту."""

    def __init__(self, name):
        """Ініціалізує ім'я контакту.

        Args:
            name (str): Ім'я контакту.
        """
        super().__init__(name)


class Address(Field):
    """Поле для зберігання поштової адреси."""

    def __init__(self, address):
        """Ініціалізує адресу контакту.

        Args:
            address (str): Повна поштова адреса.
        """
        super().__init__(address)


class Email(Field):
    """Поле для зберігання та валідації email-адреси."""

    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def __init__(self, email: str):
        """Створює email із попередньою валідацією формату.

        Args:
            email (str): Email-адреса.

        Raises:
            ValueError: Якщо email має некоректний формат.
        """
        email = email.strip()
        if not self.EMAIL_PATTERN.match(email):
            raise ValueError("Некоректна адреса електронної пошти.")
        super().__init__(email)


class Phone(Field):
    """Поле для зберігання та валідації номера телефону."""

    def __init__(self, phone):
        """Ініціалізує номер телефону.

        Args:
            phone (str): Номер телефону.

        Raises:
            ValueError: Якщо номер не складається з 10 цифр.
        """
        self.value = phone

    @property
    def value(self):
        """Повертає збережений номер телефону."""
        return self._value

    @value.setter
    def value(self, new_value):
        """Валідує та встановлює номер телефону.

        Args:
            new_value (str): Новий номер телефону.

        Raises:
            ValueError: Якщо номер не є рядком із 10 цифр.
        """
        new_value = new_value.strip()
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Номер телефону має бути до 10 символів.")
        self._value = new_value

    def __str__(self):
        """Повертає номер телефону як рядок."""
        return self._value


class Record:
    """Окремий запис адресної книги (контакт)."""

    def __init__(self, name: str):
        """Створює новий контакт.

        Args:
            name (str): Ім'я контакту.
        """
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: "Birthday" | None = None
        self.address: Address | None = None
        self.emails: list[Email] = []

    def add_phone(self, phone: str) -> str:
        """Додає новий номер телефону до контакту.

        Args:
            phone (str): Номер телефону.

        Returns:
            str: Текстове повідомлення про результат операції.
        """
        try:
            if self.find_phone(phone):
                return "Такий номер вже існує у цьому контакті."
            self.phones.append(Phone(phone))
            return "Телефон додано."
        except ValueError as e:
            return f"Невірний номер: {e}"

    def remove(self, phone: str) -> str:
        """Видаляє номер телефону з контакту.

        Args:
            phone (str): Номер телефону для видалення.

        Returns:
            str: Повідомлення про успішне видалення або помилку.
        """
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Телефон {phone} видалено."
        return f"Телефон {phone} не знайдено."

    def edit_phone(self, old_phone: str, new_phone: str) -> str:
        """Змінює існуючий номер телефону на новий.

        Args:
            old_phone (str): Поточний номер телефону.
            new_phone (str): Новий номер телефону.

        Returns:
            str: Повідомлення про результат операції.
        """
        for p in self.phones:
            if p.value == old_phone:
                if any(
                    existing.value == new_phone and existing.value != old_phone
                    for existing in self.phones
                ):
                    return f"Номер {new_phone} вже існує у цьому контакті."
                try:
                    p.value = new_phone
                    return f"Старий номер : {old_phone} був змінений на {new_phone}."
                except ValueError as er:
                    return f"Невірний номер: {er}"
        return "Телефон не знайдено."

    def find_phone(self, phone: str) -> Phone | None:
        """Шукає номер телефону в межах одного контакту.

        Args:
            phone (str): Номер телефону.

        Returns:
            Phone | None: Об'єкт Phone, якщо знайдено, або None.
        """
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def find_email(self, email: str) -> Email | None:
        """Шукає email у межах одного контакту.

        Args:
            email (str): Email для пошуку.

        Returns:
            Email | None: Об'єкт Email, якщо знайдено, або None.
        """
        target = email.strip().casefold()
        for em in self.emails:
            if em.value.casefold() == target:
                return em
        return None

    def add_birthday(self, birthday: str) -> str:
        """Додає дату народження, якщо вона ще не вказана.

        Args:
            birthday (str): Дата у форматі DD.MM.YYYY.

        Returns:
            str: Повідомлення про результат операції.
        """
        if self.birthday is not None:
            return (
                f"У контакту '{self.name.value}' вже вказано день народження: "
                f"{self.birthday}"
            )
        return self._set_birthday(birthday, "Дату народження додано.")

    def change_birthday(self, birthday: str) -> str:
        """Оновлює дату народження контакту.

        Args:
            birthday (str): Нова дата у форматі DD.MM.YYYY.

        Returns:
            str: Повідомлення про результат операції.
        """
        return self._set_birthday(birthday, "Дату народження оновлено.")

    def _set_birthday(self, birthday: str, success_message: str) -> str:
        """Встановлює дату народження з валідацією.

        Args:
            birthday (str): Дата у форматі DD.MM.YYYY.
            success_message (str): Повідомлення у разі успіху.

        Returns:
            str: Повідомлення про успіх або текст помилки.
        """
        try:
            self.birthday = Birthday(birthday)
            return success_message
        except ValueError as er:
            return str(er)

    def add_address(self, address: str) -> str:
        """Додає адресу контакту.

        Args:
            address (str): Поштова адреса.

        Returns:
            str: Повідомлення про результат.
        """
        return self._set_address(address, "Адресу додано.")

    def change_address(self, address: str) -> str:
        """Оновлює адресу контакту.

        Args:
            address (str): Нова поштова адреса.

        Returns:
            str: Повідомлення про результат.
        """
        return self._set_address(address, "Адресу оновлено.")

    def _set_address(self, address: str, success_message: str) -> str:
        """Встановлює адресу після нормалізації пробілів.

        Args:
            address (str): Введена адреса.
            success_message (str): Повідомлення при успішному збереженні.

        Returns:
            str: Повідомлення про успіх або прохання ввести адресу.
        """
        normalized = " ".join(address.split())
        if not normalized:
            return "Будь ласка, введіть адресу."
        self.address = Address(normalized)
        return success_message

    def add_email(self, email: str) -> str:
        """Додає email до контакту з перевіркою на дублікати.

        Args:
            email (str): Email-адреса.

        Returns:
            str: Повідомлення про результат операції.
        """
        if self.find_email(email):
            return "Такий email вже існує у цьому контакті."
        try:
            email_obj = Email(email)
            self.emails.append(email_obj)
            return "Email додано."
        except ValueError as er:
            return f"Невірний email: {er}"

    def change_name(self, book: "AddressBook", new_name: str) -> str:
        """Змінює ім'я контакту та оновлює ключ у адресній книзі.

        Args:
            book (AddressBook): Адресна книга, якій належить запис.
            new_name (str): Нове ім'я контакту.

        Returns:
            str: Повідомлення про результат.
        """
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

    def edit_email(self, old_email: str, new_email: str) -> str:
        """Оновлює існуючий email контакту.

        Args:
            old_email (str): Поточний email.
            new_email (str): Новий email.

        Returns:
            str: Повідомлення про результат операції.
        """
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
        """Формує кольорове текстове представлення контакту для CLI."""
        name_colored = Fore.MAGENTA + self.name.value + Style.RESET_ALL

        if self.phones:
            phones = (
                Fore.MAGENTA
                + "; ".join(phone.value for phone in self.phones)
                + Style.RESET_ALL
            )
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
            emails = (
                Fore.MAGENTA
                + "; ".join(email.value for email in self.emails)
                + Style.RESET_ALL
            )
            emails = f"\n\tімейли: {emails}"
        else:
            emails = ""

        return f"Контакт: {name_colored}{phones}{birthday}{address}{emails}"


class Birthday(Field):
    """Поле для зберігання дати народження з валідацією формату."""

    def __init__(self, value: str):
        """Створює дату народження з рядка.

        Args:
            value (str): Дата у форматі DD.MM.YYYY.

        Raises:
            ValueError: Якщо дата не відповідає формату.
        """
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(birthday_date)
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")

    def __str__(self):
        """Повертає дату народження у форматі DD.MM.YYYY."""
        return self.value.strftime("%d.%m.%Y")


class AddressBook(UserDict):
    """Колекція записів контактів (адресна книга)."""

    def add_record(self, record: Record) -> None:
        """Додає або оновлює запис контакту в адресній книзі.

        Args:
            record (Record): Запис контакту для збереження.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Шукає контакт за ім'ям.

        Args:
            name (str): Ім'я контакту.

        Returns:
            Record | None: Запис контакту або None, якщо не знайдено.
        """
        return self.data.get(name)

    def find_record_by_phone(self, phone: str) -> Record | None:
        """Шукає контакт, у якому є вказаний номер телефону.

        Args:
            phone (str): Номер телефону для пошуку.

        Returns:
            Record | None: Перший знайдений запис або None.
        """
        for record in self.data.values():
            if record.find_phone(phone):
                return record
        return None

    def find_record_by_email(self, email: str) -> Record | None:
        """Шукає контакт за email-адресою.

        Args:
            email (str): Email для пошуку.

        Returns:
            Record | None: Запис контакту або None.
        """
        target = email.strip().casefold()
        for record in self.data.values():
            for em in record.emails:
                if em.value.casefold() == target:
                    return record
        return None

    def delete(self, name: str) -> str:
        """Видаляє запис контакту з адресної книги.

        Args:
            name (str): Ім'я контакту для видалення.

        Returns:
            str: Повідомлення про результат операції.
        """
        if name in self.data:
            del self.data[name]
            return f"Запис {name} видалено."
        return f"{name} не знайдено."

    def get_upcomming_birthdays(self) -> list[dict]:
        """Формує список контактів з днями народження на найближчий тиждень.

        При цьому:
        - якщо день народження вже минув у поточному році, він переноситься на наступний;
        - якщо дата привітання припадає на вихідний, вона переноситься на найближчий понеділок.

        Returns:
            list[dict]: Відсортований список словників з полями:
                - name (str): Ім'я контакту;
                - congrats_date (date): Дата привітання;
                - birthday (date): Реальна дата народження (без зміни року).
        """
        today = date.today()
        horizon = today + timedelta(days=7)
        upcoming: list[dict] = []

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
                upcoming.append(
                    {
                        "name": record.name.value,
                        "congrats_date": congrats_date,
                        "birthday": original_birthday,
                    }
                )

        upcoming.sort(key=lambda x: (x["congrats_date"], x["name"]))
        return upcoming
