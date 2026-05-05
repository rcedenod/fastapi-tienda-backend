from bcrypt import hashpw, checkpw, gensalt


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())

# hash = hash_password('12345678')
# print(hash)
