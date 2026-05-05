from random import choices
from string import ascii_letters, digits


def generate_password(length: int = 8) -> str:
    return ''.join(choices(ascii_letters + digits, k=length))