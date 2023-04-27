"""
autor: Медовиков О.Е.
mess:  Адоптированный для телеграмма движок настольной игры

"""

import warnings
import logging
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
