from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from conf import MAX_HUNGER, MAX_WEARY
from clas import User, Person, EventHistory, PersonStatus
from func import death_message, person_status_card

"""
    1. показать игроку частичный статус
    2. предложить осмотреться
    3. предложить меню со статусом и инвентарем
    3. предложить меню с перемещением куда двигаться
"""


@dp.callback_query_handler(Text(equals=['continue_game']))
async def continue_game(query: types.CallbackQuery):
    "Непосредственно игра!"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)

    USER = await User.get(query.message['chat']['id'])
    PERSON = await Person.get(USER.u_id)

    kb_game = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # если есть незаконченное событие, предложить его закончить
    if await EventHistory.get(PERSON.p_id) is not None:
        kb_game.add(InlineKeyboardButton(
             text='понимаю',
             callback_data='get_event'
             ))
        return await query.message.answer(
                 'У вас незаконченное событие!',
                 reply_markup=kb_game,
                 parse_mode='Markdown'
                 )
    # вытаскиваем статус персонажа, чтобы проверить его состояние, жив ли
    MESS = ''
    PSTAT = await PersonStatus.get(PERSON)

    if PSTAT.death:
        reason = PERSON.d_reason
    else:
        reason = {
            PSTAT.mind < 1:
                'Самоубийство от потери рассудка',
            PSTAT.mind < 1 and PSTAT.weary >= MAX_WEARY:
                'Смерть от нервного истощения',
            PSTAT.health < 1:
                'Насильственная смерть',
            PSTAT.health < 1 and PSTAT.hunger >= MAX_HUNGER:
                'Смерть от голода',
            }.get(True)

    if reason is not None:
        """
        тут может произойти повторная перезапись причины смерти,
        но ничего страшного
        это произойдёт если персонаж будет умирать в какой-то ещё функции
        (например, смерть как наказание за событие)
        где будут прописаны уникальные причины смерти
        """
        await PERSON.die(reason)
        PSTAT = await PSTAT.change('death', True)
        # пишем эпитафию
        MESS = death_message(PERSON, PSTAT)
        return await query.message.answer(MESS, parse_mode='Markdown')

    """
    если с персонажем все нормально,
    предложить меню дальнейших действий в городе
    """
    DICT = {
        'осмотреться':       'look_around',
        'инвентарь':         'inventory_main',
        'действовать':       'get_event',
        'уйти куда-то ещё':  'leave',
        }

    for key, value in DICT.items():
        kb_game.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))

    return await query.message.answer(
            person_status_card(PERSON, PSTAT),
            reply_markup=kb_game,
            parse_mode='Markdown'
            )
