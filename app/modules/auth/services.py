from passlib.context import CryptContext
import secrets
import string

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(password:str,hashed:str) -> bool:
    return pwd_context.verify(password,hashed)

def generate_random_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password