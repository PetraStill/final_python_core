"""Модуль для збереження та завантаження даних CLI-асистента.

Забезпечує:
- створення директорії збереження (~/.cli_bot або шлях, заданий CLI_BOT_DATA_DIR);
- серіалізацію об’єктів AddressBook та NoteBook у pickle-файли;
- відновлення контактів і нотаток при запуску програми.

У разі відсутності файлів створюються нові порожні об'єкти.
Усі операції супроводжуються консольними повідомленнями INFO / ERROR.
"""

import os
import pickle
from pathlib import Path

from .address_book import AddressBook
from .note_book import NoteBook

_DEFAULT_DIR = Path.home() / ".cli_bot"
DATA_DIR = Path(os.getenv("CLI_BOT_DATA_DIR", _DEFAULT_DIR)).expanduser()
DATA_CONTACT_FILE = DATA_DIR / "addressbook.pkl"
DATA_NOTE_FILE = DATA_DIR / "notes.pkl"


def save_data(book, notes, contact_filename=DATA_CONTACT_FILE, note_filename=DATA_NOTE_FILE):
    """Зберігає дані адресної книги та нотаток у pickle-файли.

    Args:
        book (AddressBook): Об’єкт адресної книги, який потрібно зберегти.
        notes (NoteBook): Об’єкт нотаток.
        contact_filename (str|Path): Шлях до файлу з контактами.
        note_filename (str|Path): Шлях до файлу з нотатками.

    Returns:
        None. Виводить інформаційні або помилкові повідомлення у консоль.
    """
    contact_path = Path(contact_filename)
    note_path = Path(note_filename)
    try:
        contact_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.parent.mkdir(parents=True, exist_ok=True)

        with contact_path.open("wb") as f:
            pickle.dump(book, f)

        with note_path.open("wb") as f:
            pickle.dump(notes, f)

        print(f"[INFO] Дані збережено у файлах: {contact_path}, {note_path}")

    except Exception as e:
        print(f"[ERROR] Помилка збереження даних: {e}")


def load_data(contact_filename=DATA_CONTACT_FILE, note_filename=DATA_NOTE_FILE):
    """Завантажує дані контактів і нотаток із pickle-файлів.

    Якщо файлів не існує, створює нові об’єкти AddressBook та NoteBook.
    У разі помилки завантаження повертає порожні структури.

    Args:
        contact_filename (str|Path): Шлях до файлу контактів.
        note_filename (str|Path): Шлях до файлу нотаток.

    Returns:
        tuple(AddressBook, NoteBook): Завантажені або новостворені об’єкти.
    """
    contact_path = Path(contact_filename)
    note_path = Path(note_filename)

    try:
        # Завантаження контактів
        if not contact_path.exists():
            print("[INFO] Файл адресної книги не знайдено, створено нову.")
            book = AddressBook()
        else:
            with contact_path.open("rb") as f:
                book = pickle.load(f)

        # Завантаження нотаток
        if not note_path.exists():
            print("[INFO] Файл нотаток не знайдено, створено новий.")
            notes = NoteBook()
        else:
            with note_path.open("rb") as f:
                notes = pickle.load(f)

        print(f"[INFO] Дані завантажено з файлів: {contact_path}, {note_path}")
        return book, notes

    except Exception as e:
        print(f"[ERROR] Помилка завантаження даних: {e}")
        return AddressBook(), NoteBook()
