from dotenv import dotenv_values

INIT_TABLES = False
DEBUG = True
ACCESS_TOKEN_EXPIRE_MINUTES = 240
ALGORITHM = "HS256"

config_env = {
    **dotenv_values(".env"),
}
