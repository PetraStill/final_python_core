"""Команди для пошуку днів народження через задану кількість днів."""

from datetime import date, timedelta
from .decorator import input_error


def _days_word(n: int) -> str:
    """Повертає коректну словоформу слова «день» для української мови.

    Використовується для узгодження кількості днів у повідомленнях:
    1 день, 2–4 дні, 5–20 днів, 21 день тощо.

    Args:
        n (int): Кількість днів (може бути від’ємною, береться модуль).

    Returns:
        str: Одна з форм рядка: «день», «дні» або «днів».
    """
    n = abs(n)
    last_two = n % 100
    last = n % 10

    if 11 <= last_two <= 19:
        return "днів"
    if last == 1:
        return "день"
    if 2 <= last <= 4:
        return "дні"
    return "днів"


@input_error
def birthdays_in(args, book):
    """Шукає контакти, у яких день народження буде через вказану кількість днів.

    Команда очікує один аргумент — кількість днів від сьогоднішньої дати.
    Підтримується тільки невід’ємне ціле число.

    Логіка:
    - для кожного контакту з днем народження обчислюється наступна дата його ДН;
    - якщо наступна дата ДН рівно через N днів від сьогодні — контакт додається до результату.

    Args:
        args (list[str]): Список аргументів командного рядка; args[0] — кількість днів.
        book: Екземпляр AddressBook з атрибутом data (dict ім'я → Record).

    Returns:
        str: Текстове повідомлення з переліком імен або повідомлення про відсутність збігів,
        а також повідомлення про помилки формату/аргументів.
    """
    if len(args) != 1:
        return (
            "Помилка: команда 'birthdays-in' очікує рівно 1 аргумент:\n"
            "birthdays-in <кількість_днів>"
        )

    days_str = args[0]

    try:
        days = int(days_str)
    except ValueError:
        return "Помилка: кількість днів має бути цілим числом."

    if days < 0:
        return "Помилка: кількість днів не може бути від'ємною."

    today = date.today()
    target_date = today + timedelta(days=days)

    matches: list[str] = []

    for record in book.data.values():
        birthday_field = getattr(record, "birthday", None)
        if not birthday_field:
            continue

        bday = birthday_field.value

        next_bday = bday.replace(year=today.year)
        if next_bday < today:
            next_bday = next_bday.replace(year=today.year + 1)

        if next_bday == target_date:
            matches.append(record.name.value)

    if not matches:
        return (
            f"Немає контактів з днем народження через {days} {_days_word(days)}."
        )

    names = ", ".join(matches)
    return f"День народження через {days} {_days_word(days)} у {names}."
