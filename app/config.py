from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL=os.getenv("POSTGRES_URL")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCES_TOKEN_EXPIRE_MINUTES"))