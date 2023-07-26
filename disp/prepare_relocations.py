from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from datetime import datetime, timedelta

from clas import PersonStatus, Journal
from func import update_message, create_keyboard
from conf import emoji


@dp.callback_query_handler(Text(startswith=['prepare_relocations_']))
async def prepare_relocations(query: types.CallbackQuery):
    """показать игроку основной квест"""
    START = int(query.data.split('_')[-1])

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    MESS = 'История ваших странствий по городу: \n\n'
    SPISOK = await Journal.get_relocations(
        STAT.p_id,
        START,
        START + 4
    )
    # формируем сообщение со списком
    if len(SPISOK) == 0:
        MESS += 'больше нет перемещений'

    for JOUR in SPISOK:
        TIME = (
            datetime.strptime('09:00', '%H:%M')
            + timedelta(minutes=15*JOUR.gametime)
        ).strftime('%H:%M')

        KEY = emoji('clock') + ' ' + TIME \
            + JOUR.name.replace('Переход:', ' ')

        MESS += f'\n ``` {KEY} ``` '

    MESS += '\n'
    # формируем клавиатуру
    DICT = {}

    if START != 0:
        DICT['позднее'] = f'prepare_relocations_{START - 5}'

    if len(SPISOK) > 0:
        DICT['раньше'] = f'prepare_relocations_{START + 5}'

    DICT['назад'] = 'prepare_main'
    return await update_message(
            query.message,
            MESS,
            create_keyboard(DICT)
    )
