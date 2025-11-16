from datetime import date, timedelta
from .decorator import input_error


def _days_word(n: int) -> str:
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

    matches = []

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
