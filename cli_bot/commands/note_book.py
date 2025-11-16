from collections import UserDict
from datetime import datetime
from colorama import Fore, Style


class Note:
    
    def __init__(self, title, text, tags=None): 
        self.title = title
        self.text = text
        self.created_at = datetime.now()
        self.tags = set(tag.lower() for tag in tags) if tags else set() 

    def add_tags(self, new_tags):
        for tag in new_tags:
            self.tags.add(tag.lower())

    def __str__(self):
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
    def add(self, note : Note):
        self.data[note.title.lower()] = note
        return f"Нотатку '{note.title}' додано."
    
    def edit(self,title,new_text):
        note = self.data.get(title.lower())
        if not note:
            return f"Нотатку '{title}' не знайдено."
        note.text = new_text
        return f"Нотатку '{title}' оновлено."
    
    def add_tags(self, title, tags):
        key = title.lower()
        note = self.data.get(key)
        if note:
            note.add_tags(tags)
            return f"До нотатки '{title}' додано теги: {', '.join(tags)}"
        return f"Помилка: Нотатка з назвою '{title}' не знайдена."

    def find_by_tags(self, tags_query):
        search_tags = {tag.strip().lower() for tag in tags_query.replace(',', ' ').split()}
        
        found_notes = []
        for note in self.data.values():
            if note.tags.intersection(search_tags):
                found_notes.append(note)
                
        return found_notes

    def sort_by_tags(self):
        
        def sort_key(note):
            if note.tags:
                return sorted(list(note.tags))[0] 
            else:
                return 'zzzzz' 

        sorted_notes = sorted(self.data.values(), key=sort_key)
        return sorted_notes

    def find(self, query: str):
        results = [
            i for i in self.data.values()
            if query.lower() in i.title.lower()
        ]
        return results
    
    def delete(self,title):
        if title.lower() in self.data:
            del self.data[title.lower()]
            return f"Нотатка {title} видалено."
        return f"{title} не знайдено."



