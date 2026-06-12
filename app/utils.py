from pwdlib import PasswordHash

def hash_password(password: str) -> str:
    ph = PasswordHash.recommended()
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    ph = PasswordHash.recommended()
    return ph.verify(plain_password, hashed_password)
