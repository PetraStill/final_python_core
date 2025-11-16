"""Головний модуль запуску CLI-асистента.

Забезпечує:
- завантаження даних контактів і нотаток;
- цикл обробки команд користувача;
- виконання команд через execute_command;
- підказки для схожих команд (suggest_command);
- кольоровий вивід результатів і помилок.
"""

try:
    from commands import (
        add_contact, change_contact, show_phone, show_all,
        add_birthday, show_birthday, birthdays, birthdays_in,
        add_address, add_email, delete_contact, find_by_email, find_by_name,
        add_note, show_notes, find_note, edit_note, delete_note,
        add_tags_to_note, find_note_by_tags, sort_notes_by_tags,
        parse_input, save_data, load_data, help_text, all_table,
    )
except ImportError:  # pragma: no cover - fallback for script execution
    from commands import (  # type: ignore
        add_contact, change_contact, show_phone, show_all,
        add_birthday, show_birthday, birthdays, birthdays_in,
        add_address, add_email, delete_contact, find_by_email, find_by_name,
        add_note, show_notes, find_note, edit_note, delete_note,
        add_tags_to_note, find_note_by_tags, sort_notes_by_tags,
        parse_input, save_data, load_data, help_text, all_table,
    )

from difflib import get_close_matches

from colorama import init, Fore, Style
init(autoreset=True)

ERROR_MSG = "Команда не існує. Введіть 'help' для ознайомлення."

COMMANDS = (
    "hello",
    "add",
    "change",
    "phone",
    "all",
    "add-birthday",
    "add-address",
    "add-email",
    "show-birthday",
    "birthdays",
    "birthdays-in",
    "add-note",
    "find-note",
    "edit-note",
    "delete-note",
    "delete",
    "email",
    "name",
    "show-notes",
    "help",
    "close",
    "exit",
    "add-tags",
    "find-by-tag",
    "sort-notes-by-tag",
    "all-table",
)


def suggest_command(user_cmd: str):
    """Пропонує найбільш схожу відому команду.

    Args:
        user_cmd (str): Команда, введена користувачем.

    Returns:
        str | None: Найближчий збіг із COMMANDS або None, якщо збігу немає.
    """
    matches = get_close_matches(user_cmd, COMMANDS, n=1, cutoff=0.6)
    return matches[0] if matches else None


def execute_command(command: str, args: list[str], book, notes):
    """Виконує команду, маршрутизуючи її до відповідної функції.

    Args:
        command (str): Назва команди (у нижньому регістрі).
        args (list[str]): Аргументи команди.
        book: Екземпляр AddressBook.
        notes: Екземпляр NoteBook.

    Returns:
        Any | None: Результат виконання команди або None, якщо команда невідома.
    """
    if command == "hello":
        return "Як я можу допомогти?"
    elif command == "add":
        return add_contact(args, book)
    elif command == "change":
        return change_contact(args, book)
    elif command == "phone":
        return show_phone(args, book)
    elif command == "all":
        return show_all(book)
    elif command == "add-birthday":
        return add_birthday(args, book)
    elif command == "show-birthday":
        return show_birthday(args, book)
    elif command == "birthdays":
        return birthdays(book)
    elif command == "birthdays-in":
        return birthdays_in(args, book)
    elif command == "add-address":
        return add_address(args, book)
    elif command == "add-email":
        return add_email(args, book)
    elif command == "delete":
        return delete_contact(args, book)
    elif command == "email":
        return find_by_email(args, book)
    elif command == "name":
        return find_by_name(args, book)
    elif command == "add-note":
        return add_note(args, notes)
    elif command == "find-note":
        return find_note(args, notes)
    elif command == "edit-note":
        return edit_note(args, notes)
    elif command == "delete-note":
        return delete_note(args, notes)
    elif command == "show-notes":
        return show_notes(notes)
    elif command == "add-tags":
        return add_tags_to_note(args, notes)
    elif command == "find-by-tag":
        return find_note_by_tags(args, notes)
    elif command == "sort-notes-by-tag":
        return sort_notes_by_tags(notes)
    elif command == "help":
        return help_text()
    elif command == "all-table":
        return all_table(book)
    else:
        return None


def print_colored(message, color=Fore.GREEN):
    """Друкує повідомлення у вказаному кольорі.

    Args:
        message: Будь-який об'єкт, що перетворюється на рядок.
        color: Колір із colorama.Fore (за замовчуванням зелений).
    """
    print(color + str(message))


def main():
    """Точка входу CLI-асистента.

    - завантажує дані з диска,
    - запускає цикл введення команд,
    - виконує команди та виводить результати з кольорами,
    - пропонує виправлення при помилці в назві команди,
    - зберігає дані при завершенні або натисканні Ctrl+C.
    """
    book, notes = load_data()
    print_colored("Ласкаво просимо до асистента!", Fore.GREEN)

    try:
        while True:
            user_input = input(Fore.CYAN + "Введіть команду: " + Style.RESET_ALL)
            command, args = parse_input(user_input)

            if not command:
                continue

            if command in ("close", "exit"):
                print_colored("До побачення!", Fore.GREEN)
                save_data(book, notes)
                break

            result = execute_command(command, args, book, notes)

            if result is not None:
                error_keys = [
                    "Помилка:",
                    "Невірний номер",
                    "очікує",
                    "вже існує",
                    "не існує",
                    "не знайдено",
                    "вже вказано",
                    "help для ознайомлення",
                    "невірно",
                    "Некоректна",
                    "Невірний email",
                    "не може бути",
                    "поточним",
                    "має бути",
                ]
                if any(key in str(result) for key in error_keys):
                    print_colored(result, Fore.RED)
                else:
                    print_colored(result, Fore.YELLOW)
                continue

            suggestion = suggest_command(command)
            if suggestion:
                answer = input(
                    Fore.YELLOW
                    + f"Ви мали на увазі '{suggestion}'? (y/n): "
                    + Style.RESET_ALL
                ).strip().lower()
                if answer in ("y", "yes", "т", "так"):
                    result = execute_command(suggestion, args, book, notes)
                    if result is not None:
                        print(result)
                else:
                    print_colored(ERROR_MSG, Fore.RED)
            else:
                print_colored(ERROR_MSG, Fore.RED)
    except KeyboardInterrupt:
        save_data(book, notes)


if __name__ == "__main__":
    main()
