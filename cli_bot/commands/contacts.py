"""Команди роботи з контактами для CLI-асистента.

Містить обробники команд:
- add, change, phone, all, add-birthday, show-birthday,
  add-address, add-email, delete, email, name, birthdays.
"""

from .decorator import input_error
from .address_book import Record


def add_contact(args, book):
    """Додає новий контакт або оновлює існуючий, додаючи до нього номер телефону.

    Формат команди:
        add <ім'я> <телефон>

    Логіка:
    - якщо контакту з таким ім'ям немає — створюється новий запис Record;
    - номер телефону попередньо перевіряється через Record.add_phone;
    - якщо номер уже використовується іншим контактом — повертається повідомлення про конфлікт.

    Args:
        args (list[str]): Список аргументів командного рядка (ім'я та телефон).
        book: Екземпляр AddressBook, у якому зберігаються контакти.

    Returns:
        str: Текстове повідомлення про результат операції.
    """
    if len(args) < 2:
        return "Помилка: команда 'add' очікує 2 аргументи: add <ім'я> <телефон>."
    
    name, phone = args[0], args[1]
    record = book.find(name)
    existing_owner = book.find_record_by_phone(phone)

    if existing_owner and (record is None or existing_owner.name.value != record.name.value):
        return f"Номер {phone} вже використовується контактом '{existing_owner.name.value}'."

    if not record:
        temp_record = Record(name)
        phone_result = temp_record.add_phone(phone)
        if "Невірний номер" in phone_result:
            return phone_result
        book.add_record(temp_record)
        return f"Контакт додано. {phone_result}"

    phone_result = record.add_phone(phone)
    if "Невірний номер" in phone_result:
        return phone_result

    return f"Контакт оновлено. {phone_result}"


@input_error
def change_contact(args, book):
    """Змінює окремі поля контакту: ім'я, телефон, адресу, день народження або email.

    Формат:
        change <ім'я> name <нове_ім'я>
        change <ім'я> phone <старий_номер> <новий_номер>
        change <ім'я> address <нова_адреса>
        change <ім'я> birthday <DD.MM.YYYY>
        change <ім'я> email <старий_email> <новий_email>

    Args:
        args (list[str]): Аргументи командного рядка (ім'я, підкоманда, параметри).
        book: Екземпляр AddressBook.

    Returns:
        str: Повідомлення про успіх або опис помилки.
    """
    if len(args) < 3:
        return ("Помилка: команда 'change' очікує формат "
                "change <ім'я> name|phone|address|birthday|email [старе_значення] <нове_значення>.")
    name = args[0]
    subcommand = args[1].lower()
    params = args[2:]
    record = book.find(name)
    if not record:
        return 'Контакту не було знайдено.'

    if subcommand == "name":
        if not params:
            return "Формат: change <ім'я> name <нове_ім'я>."
        return record.change_name(book, params[0])

    if subcommand == "phone":
        if len(params) < 2:
            return "Формат: change <ім'я> phone <старий_номер> <новий_номер>."
        old_phone, new_phone = params[0], params[1]
        owner = book.find_record_by_phone(new_phone)
        if owner and owner.name.value != record.name.value:
            return f"Номер {new_phone} вже використовується контактом '{owner.name.value}'."
        return record.edit_phone(old_phone, new_phone)

    if subcommand == "email":
        if len(params) < 2:
            return "Формат: change <ім'я> email <старий_email> <новий_email>."
        old_email, new_email = params[0], params[1]
        owner = book.find_record_by_email(new_email)
        if owner and owner.name.value != record.name.value:
            return f"Email {new_email} вже використовується контактом '{owner.name.value}'."
        return record.edit_email(old_email, new_email)

    if subcommand == "address":
        if not params:
            return "Будь ласка, введіть нову адресу."
        return record.change_address(" ".join(params))

    if subcommand == "birthday":
        if not params:
            return "Формат: change <ім'я> birthday <DD.MM.YYYY>."
        return record.change_birthday(params[0])

    else:
        return "Невідома підкоманда. Доступні: name, phone, address, birthday, email."


@input_error
def show_phone(args, book):
    """Показує всі номери телефону контакту за його ім'ям.

    Формат:
        phone <ім'я>

    Args:
        args (list[str]): Список аргументів; args[0] — ім’я контакту.
        book (AddressBook): Колекція контактів.

    Returns:
        str: Список телефонів або повідомлення про відсутність даних.
    """
    if len(args) < 1:
        return "Помилка: команда 'phone' очікує 1 аргумент: phone <ім'я>."

    name = args[0]
    record = book.find(name)

    if not record:
        return f"Контакт з ім'ям {name} не знайдено."

    if not record.phones:
        return f"У контакту {name} немає збережених телефонів."

    phones_str = "; ".join(p.value for p in record.phones)
    return f"Телефони контакту {name}: {phones_str}"



@input_error
def show_all(book):
    """Повертає всі контакти у вигляді списку рядків.

    Використовує метод __str__ кожного Record.

    Args:
        book: Екземпляр AddressBook.

    Returns:
        str: Усі контакти, розділені переносами рядків, або повідомлення про відсутність записів.
    """
    if not book.data:
        return "Немає збережених контактів."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    """Додає або встановлює дату народження для існуючого контакту.

    Формат:
        add-birthday <ім'я> <DD.MM.YYYY>

    Args:
        args (list[str]): Ім'я та дата народження.
        book: Екземпляр AddressBook.

    Returns:
        str: Повідомлення про результат (успіх або помилку/відсутність контакту).
    """
    if len(args) < 2:
        return "Помилка: команда 'add-birthday' очікує 2 аргументи: add_birthday <ім'я> <дата_народження>."
    name, birth_date = args[0], args[1]
    record = book.find(name)
    if not record:
        return 'Контакт не було знайдено.'
    return record.add_birthday(birth_date)


@input_error
def show_birthday(args, book):
    """Показує збережену дату народження контакту.

    Формат:
        show-birthday <ім'я>

    Args:
        args (list[str]): Єдиний аргумент — ім'я контакту.
        book: Екземпляр AddressBook.

    Returns:
        str: Дата народження або повідомлення про відсутність даних/контакту.
    """
    if len(args) < 1:
        return "Помилка: команда 'show-birthday' очікує 1 аргумент: show <ім'я>"
    name = args[0]
    record = book.find(name)
    if not record:
        return 'Контакту не існує.'
    if not record.birthday:
        return 'Для цього контакту не вказано день народження.'
    return f"{name}: {record.birthday}"


@input_error
def add_address(args, book):
    """Додає або оновлює адресу контакту.

    Формат:
        add-address <ім'я> <адреса>

    Args:
        args (list[str]): Ім'я та адреса (може складатися з кількох слів).
        book: Екземпляр AddressBook.

    Returns:
        str: Повідомлення про результат.
    """
    if len(args) < 2:
        return "Помилка: команда 'add-address' очікує 2 аргументи: add-address <ім'я> <адреса>."
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        return 'Контакту не було знайдено.'
    return record.add_address(address)


@input_error
def add_email(args, book):
    """Додає email до контакту з перевіркою на дублікати в межах книги.

    Формат:
        add-email <ім'я> <email>

    Args:
        args (list[str]): Ім'я контакту та email.
        book: Екземпляр AddressBook.

    Returns:
        str: Повідомлення про результат операції.
    """
    if len(args) < 2:
        return "Помилка: команда 'add-email' очікує 2 аргументи: add-email <ім'я> <email>."
    name, email = args[0], args[1]
    record = book.find(name)
    if not record:
        return 'Контакту не було знайдено.'
    owner = book.find_record_by_email(email)
    if owner and owner.name.value != record.name.value:
        return f"Email {email} вже використовується контактом '{owner.name.value}'."
    return record.add_email(email)


@input_error
def delete_contact(args, book):
    """Видаляє контакт з адресної книги за ім'ям.

    Формат:
        delete <ім'я>

    Args:
        args (list[str]): Список аргументів; args[0] — ім'я.
        book: Екземпляр AddressBook.

    Returns:
        str: Повідомлення про результат видалення.
    """
    if len(args) < 1:
        return "Помилка: команда 'delete' очікує 1 аргумент: delete <ім'я>."
    name = args[0]
    return book.delete(name)


@input_error
def find_by_email(args, book):
    """Пошук контакту за email-адресою.

    Формат:
        email <адреса>

    Args:
        args (list[str]): Список аргументів; args[0] — email.
        book: Екземпляр AddressBook.

    Returns:
        str: Текстове представлення контакту або повідомлення, що його не знайдено.
    """
    if len(args) < 1:
        return "Помилка: команда 'email' очікує 1 аргумент: email <адреса>."
    email = args[0]
    record = book.find_record_by_email(email)
    if not record:
        return f"Контакт з email {email} не знайдено."
    return f'Контакт знайдено {record}.'


@input_error
def find_by_name(args, book):
    """Пошук контакту за ім'ям.

    Формат:
        name <ім'я>

    Args:
        args (list[str]): Список аргументів; args[0] — ім'я.
        book: Екземпляр AddressBook.

    Returns:
        str: Текстове представлення контакту або повідомлення про відсутність.
    """
    if len(args) < 1:
        return "Помилка: команда 'name' очікує 1 аргумент: name <ім'я>."
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Контакт з ім'ям {name} не знайдено."
    return f'Контакт знайдено {record}.'


@input_error
@input_error
def birthdays(book):
    """Показує список найближчих днів народження на 7 днів уперед.

    Дані беруться з методу AddressBook.get_upcomming_birthdays(), який
    повертає структуру з іменем, реальною датою народження та датою привітання.

    Args:
        book: Екземпляр AddressBook.

    Returns:
        str: Кожен рядок містить дату привітання, ім'я та реальну дату народження,
             або повідомлення про відсутність найближчих днів народження.
    """
    upcoming = book.get_upcomming_birthdays()
    if not upcoming:
        return "Немає днів народження впродовж наступних 7 днів."
    lines = []
    for item in upcoming:
        congrats_date_str = item["congrats_date"].strftime("%d.%m.%Y")
        birthday_str = item["birthday"].strftime("%d.%m.%Y")
        name = item["name"]
        lines.append(f"{congrats_date_str} привітати {name} ({birthday_str})")
    return "\n".join(lines)
