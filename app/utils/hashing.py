from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================
# HASH PASSWORD
# =========================

def hash_password(password: str):
    return pwd_context.hash(password)


# alias for main.py
def get_password_hash(password: str):
    return pwd_context.hash(password)


# =========================
# VERIFY PASSWORD
# =========================

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )