from pwdlib import PasswordHash

pwlib_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwlib_context.hash(password)


def verify_password_hash(clear_password: str, password_hash: str) -> bool:
    return pwlib_context.verify(clear_password, password_hash)
