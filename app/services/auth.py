from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JNTError, jwt
from app.config import SECRET_KEY, ALGORITHM, ACCES_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=[bcrypt],derecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict, expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp" : expire})
    return jwt.enç(to_encode,SECRET_KEY,algorithm=ALGORITHM)