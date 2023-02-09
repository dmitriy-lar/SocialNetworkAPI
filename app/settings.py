from dotenv import dotenv_values

INIT_TABLES = True
DEBUG = True

config_env = {
    **dotenv_values('.env'),
}
