from colorama import Fore, Style
from .decorator import input_error


@input_error
def all_table(book):

    if not getattr(book, "data", None):
        return "Немає збережених контактів."

    headers = ["Ім'я", "Телефони", "День народження", "Адреса", "Email"]

    rows_plain: list[list[str]] = []
    rows_colored: list[list[str]] = []

    for record in book.data.values():
        name_plain = record.name.value

        if getattr(record, "phones", None):
            phones_plain = "; ".join(phone.value for phone in record.phones)
        else:
            phones_plain = ""

        if getattr(record, "birthday", None):
            birthday_plain = str(record.birthday)
        else:
            birthday_plain = ""

        if getattr(record, "address", None):
            address_plain = str(record.address)
        else:
            address_plain = ""

        if getattr(record, "emails", None):
            emails_plain = "; ".join(email.value for email in record.emails)
        else:
            emails_plain = ""

        row_plain = [name_plain, phones_plain, birthday_plain, address_plain, emails_plain]
        rows_plain.append(row_plain)

        row_colored = [
            Fore.MAGENTA + name_plain + Style.RESET_ALL if name_plain else "",
            Fore.MAGENTA + phones_plain + Style.RESET_ALL if phones_plain else "",
            Fore.MAGENTA + birthday_plain + Style.RESET_ALL if birthday_plain else "",
            Fore.MAGENTA + address_plain + Style.RESET_ALL if address_plain else "",
            Fore.MAGENTA + emails_plain + Style.RESET_ALL if emails_plain else "",
        ]
        rows_colored.append(row_colored)

    col_widths = [len(h) for h in headers]
    for row in rows_plain:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    header_line = " | ".join(
        header.ljust(col_widths[i]) for i, header in enumerate(headers)
    )
    separator = "-+-".join("-" * w for w in col_widths)

    lines = [header_line, separator]

    for row_plain, row_colored in zip(rows_plain, rows_colored):
        cells = []
        for i, (plain, colored) in enumerate(zip(row_plain, row_colored)):
            padding = col_widths[i] - len(plain)
            cells.append(colored + " " * padding)
        lines.append(" | ".join(cells))

    return "\n".join(lines)
