import bcrypt

def hash_password(password: str) -> str:
    pw = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    pw = password.encode("utf-8")[:72]
    return bcrypt.checkpw(pw, hashed.encode("utf-8"))