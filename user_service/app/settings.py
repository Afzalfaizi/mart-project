from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()
    
SECRET_KEY: str = config("SECRET_KEY", cast=str)
ALGORITHM: str = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)
DATABASE_URL = config("DATABASE_URL", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Adjust the expiration time as needed




# TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)