from pwdlib import PasswordHash

pwlib_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwlib_context.hash(password)
