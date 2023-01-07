from starlette.config import Config

config = Config('../.config/bot/bot.conf')

BOT_TOKEN = config('TELEGRAM_API', cast=str)
ARHM_PSQL = config('ARHM_PSQL',   cast=str)
