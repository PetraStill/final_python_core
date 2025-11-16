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
    contact_path = Path(contact_filename)
    note_path = Path(note_filename)
    try:
        if not contact_path.exists():
            print("[INFO] Файл адресної книги не знайдено, створено нову.")
            book = AddressBook()
        else:
            with contact_path.open("rb") as f:
                book = pickle.load(f)
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
