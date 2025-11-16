"""Головний модуль експорту команд та класів CLI-асистента.

Цей файл об’єднує всі основні компоненти застосунку та визначає __all__,
щоб забезпечити зручний імпорт функцій, класів та утиліт в інших частинах
програми.

Експортує:
- Команди для роботи з контактами (add, change, phone, all, delete тощо)
- Команди для роботи з email, адресою та днями народження
- Команди роботи з нотатками (add-note, find-note, edit-note, теги тощо)
- Допоміжні утиліти: парсер команд, декоратор обробки помилок
- Класи AddressBook, Record, NoteBook
- Модулі збереження та завантаження даних
- Табличний вивід контактів та пошук днів народження через N днів

Метою цього модуля є централізація імпорту та створення
зручного публічного інтерфейсу для всього CLI-пакета.
"""


from .contacts import add_contact,change_contact,show_phone,show_all,add_birthday,show_birthday, birthdays, add_address, add_email, delete_contact, find_by_email, find_by_name
from .parser import parse_input
from .decorator import input_error
from .address_book import AddressBook, Record
from .storage import save_data,load_data
from .note_book import NoteBook
from .notes import add_note, find_note, show_notes, edit_note, delete_note, add_tags_to_note, find_note_by_tags, sort_notes_by_tags
from .help_text import help_text
from .birthdays_in import birthdays_in
from .all_table import all_table

__all__ = ['add_contact', 'change_contact','show_phone', 'show_all', 'parse_input' , 'input_error', 'AddressBook', 'Record', 
        'add_birthday','show_birthday', 'birthdays', 'birthdays_in', 'save_data','load_data', 'NoteBook', 'add_note', 'find_note','show_notes',
        'edit_note','delete_note', 'help_text', 'add_tags_to_note','find_note_by_tags','sort_notes_by_tags','add_address','add_email', 
        'delete_contact','find_by_email','find_by_name', 'all_table']