from functools import wraps

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Прошу ввести ім'я та телефон."
        except KeyError:
            return "Введіть ім'я користувача або контакт не знайдено."
        except IndexError:
            return "Прошу ввести ім'я."
    return inner