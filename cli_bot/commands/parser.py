def parse_input(user_input: str):
    """Розбирає введений рядок на команду та аргументи.

    Args:
        user_input (str): Повний рядок, введений користувачем у CLI.

    Returns:
        tuple[str, list[str]]: 
            - назва команди у нижньому регістрі;
            - список аргументів (може бути порожнім).
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args
