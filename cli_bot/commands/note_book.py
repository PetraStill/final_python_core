"""Модуль для роботи з нотатками (Note) та їхньою колекцією (NoteBook).

Забезпечує:
- створення нотаток із назвою, текстом і тегами;
- редагування та видалення нотаток;
- пошук за назвою;
- пошук за тегами;
- сортування нотаток за тегами;
- форматований кольоровий вивід нотатки у CLI.
"""

from collections import UserDict
from datetime import datetime
from colorama import Fore, Style


class Note:
    """Окрема нотатка з назвою, текстом, датою створення та тегами."""

    def __init__(self, title, text, tags=None):
        """Створює нову нотатку.

        Args:
            title (str): Назва нотатки.
            text (str): Основний текст нотатки.
            tags (iterable[str] | None): Початкові теги (необов'язково).
        """
        self.title = title
        self.text = text
        self.created_at = datetime.now()
        self.tags = set(tag.lower() for tag in tags) if tags else set()

    def add_tags(self, new_tags):
        """Додає один або кілька тегів до нотатки.

        Args:
            new_tags (iterable[str]): Список або інший ітератор тегів.
        """
        for tag in new_tags:
            self.tags.add(tag.lower())

    def __str__(self):
        """Повертає нотатку у кольоровому форматі для CLI-виводу.

        Заголовок і дата — magenta.
        Теги — світло-фіолетові.
        Текст — без кольору.
        """
        title_colored = Fore.MAGENTA + Style.BRIGHT + self.title + Style.RESET_ALL
        text = self.text
        created = Fore.MAGENTA + self.created_at.strftime('%d.%m.%Y %H:%M') + Style.RESET_ALL

        if self.tags:
            tags_colored = " ".join(
                Fore.LIGHTMAGENTA_EX + f"#{t}" + Style.RESET_ALL for t in sorted(self.tags)
            )
            tags_line = f"Теги: {tags_colored}"
        else:
            tags_line = "Теги: немає."

        return (
            f"{title_colored}\n"
            f"{text}\n"
            f"Створено: {created}\n"
            f"{tags_line}"
        )


class NoteBook(UserDict):
    """Колекція нотаток, що забезпечує пошук, редагування і зберігання."""

    def add(self, note: Note):
        """Додає нову нотатку до нотатника.

        Args:
            note (Note): Об'єкт нотатки.

        Returns:
            str: Повідомлення про успішне додавання.
        """
        self.data[note.title.lower()] = note
        return f"Нотатку '{note.title}' додано."

    def edit(self, title, new_text):
        """Редагує текст нотатки.

        Args:
            title (str): Назва нотатки (незалежно від регістру).
            new_text (str): Новий текст.

        Returns:
            str: Повідомлення про результат.
        """
        note = self.data.get(title.lower())
        if not note:
            return f"Нотатку '{title}' не знайдено."
        note.text = new_text
        return f"Нотатку '{title}' оновлено."

    def add_tags(self, title, tags):
        """Додає теги до зазначеної нотатки.

        Args:
            title (str): Назва нотатки.
            tags (list[str]): Список тегів.

        Returns:
            str: Результат виконання операції.
        """
        key = title.lower()
        note = self.data.get(key)
        if note:
            note.add_tags(tags)
            return f"До нотатки '{title}' додано теги: {', '.join(tags)}"
        return f"Помилка: Нотатка з назвою '{title}' не знайдена."

    def find_by_tags(self, tags_query):
        """Шукає нотатки за одним або кількома тегами.

        Args:
            tags_query (str): Рядок із тегами, розділеними пробілами або комами.

        Returns:
            list[Note]: Список відповідних нотаток.
        """
        search_tags = {tag.strip().lower() for tag in tags_query.replace(',', ' ').split()}
        return [note for note in self.data.values() if note.tags.intersection(search_tags)]

    def sort_by_tags(self):
        """Сортує нотатки за алфавітом першого тегу.

        Нотатки без тегів розміщуються в кінці.

        Returns:
            list[Note]: Відсортований список нотаток.
        """

        def sort_key(note):
            if note.tags:
                return sorted(note.tags)[0]
            return "zzzzz"  # гарантія, що безтеговi підуть у кінець

        return sorted(self.data.values(), key=sort_key)

    def find(self, query: str):
        """Пошук нотаток за частковим входженням назви.

        Args:
            query (str): Рядок для пошуку.

        Returns:
            list[Note]: Усі нотатки, чиї назви містять запит.
        """
        query_lower = query.lower()
        return [note for note in self.data.values() if query_lower in note.title.lower()]

    def delete(self, title):
        """Видаляє нотатку за назвою.

        Args:
            title (str): Назва нотатки.

        Returns:
            str: Повідомлення про результат.
        """
        key = title.lower()
        if key in self.data:
            del self.data[key]
            return f"Нотатка {title} видалено."
        return f"{title} не знайдено."
