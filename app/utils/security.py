from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext


SECRET_KEY = "parktrack_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    password = password[:72]  # bcrypt limit
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
