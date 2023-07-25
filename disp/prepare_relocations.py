from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from aiogram.utils.markdown import link

from clas import PersonStatus, Journal
from func import update_message, button_key_add_space
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
        START + 5
    )

    kb_prepare = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )
    DICT = {}

    for JOUR in SPISOK:
        TIME = (
            datetime.strptime('09:00', '%H:%M')
            + timedelta(minutes=15*JOUR.gametime)
        ).strftime('%H:%M')

        KEY = emoji('clock') + ' ' + TIME \
            + JOUR.name.replace('Переход:', ' ')
        DICT[KEY] = f'r\\_m\\_{JOUR.date_create.microsecond}'
    if len(SPISOK) == 0:
        MESS += 'больше нет перемещений'

    # DICT = button_key_add_space(DICT)

    for KEY, VALUE in DICT.items():
        MESS += f'\n ``` {KEY} ``` '
    MESS += '\n'

    if START != 0:
        kb_prepare.add(InlineKeyboardButton(
                text='позднее',
                callback_data=f'prepare_relocations_{START - 5}',
            ))
    if len(SPISOK) > 0:
        kb_prepare.add(InlineKeyboardButton(
            text='раньше',
            callback_data=f'prepare_relocations_{START + 5}',
        ))

    kb_prepare.add(InlineKeyboardButton(
            text='назад',
            callback_data='prepare_main',
        ))
    # MESS = f'``` {MESS} ```'
    return await update_message(
            query.message,
            MESS,
            kb_prepare)

"""
@dp.callback_query_handler(Text(startswith=['r_m_']))
async def prepare_relocation(query: types.CallbackQuery):
    MICRO = int(query.data.split('_')[-1])

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    MESS = await Journal.get_relocation(STAT.p_id, MICRO)

    kb_prepare = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    kb_prepare.add(InlineKeyboardButton(
            text='назад',
            callback_data='prepare_main',
        ))

    return await update_message(
            query.message,
            MESS,
            kb_prepare)
"""
