from starlette.config import Config

config = Config('.conf')

BOT_API   = config('BOT_API',   cast=str)
BOT_TOKEN = config('BOT_TOKEN', cast=str)
SALT      = config('SALT',      cast=str)
API_URL   = config('API_URL',   cast=str) 

