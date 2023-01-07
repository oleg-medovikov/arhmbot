import logging
import warnings
from aiogram import executor

from disp import dp, on_startup

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    try:
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup
                )
    except KeyboardInterrupt:
        pass
