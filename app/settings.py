from dotenv import dotenv_values
from passlib.context import CryptContext

INIT_TABLES = False
DEBUG = True
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

config_env = {
    **dotenv_values('.env'),
}
