from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from conf import MAX_HUNGER, MAX_WEARY
from clas import EventHistory, PersonStatus, Shop
from func import death_message, person_status_card, update_message

"""
    1. показать игроку частичный статус
    2. предложить осмотреться
    3. предложить меню со статусом и инвентарем
    4. предложить меню с перемещением куда двигаться
"""


@dp.callback_query_handler(Text(equals=['continue_game']))
async def continue_game(query: types.CallbackQuery):
    "Непосредственно игра!"
    # удаляем предыдущую клавиатуру
    await query.message.edit_reply_markup(reply_markup=None)

    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])

    kb_game = InlineKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
        )

    # если есть незаконченное событие, предложить его закончить
    try:
        await EventHistory.get(PERS.p_id)
    except ValueError:
        pass
    else:
        kb_game.add(InlineKeyboardButton(
             text='понимаю',
             callback_data='get_event'
             ))

        return await update_message(
            query.message,
            'У вас незаконченное событие!',
            kb_game
                )

    # вытаскиваем статус персонажа, чтобы проверить его состояние, жив ли
    if STAT.death:
        reason = PERS.d_reason
    else:
        reason = {
            STAT.mind < 1:
                'Самоубийство от потери рассудка',
            STAT.mind < 1 and STAT.weary >= MAX_WEARY:
                'Смерть от нервного истощения',
            STAT.health < 1:
                'Насильственная смерть',
            STAT.health < 1 and STAT.hunger >= MAX_HUNGER:
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
        PERS = await PERS.die(reason)
        STAT = await STAT.change('death', True)
        kb_game.add(InlineKeyboardButton(
             text='попробовать ещё раз',
             callback_data='start_new_game'
             ))
        # пишем эпитафию
        return await update_message(
            query.message,
            death_message(PERS, STAT),
            kb_game
                )

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

    for SHOP in await Shop.get(STAT.location, STAT.stage):
        DICT[SHOP.shop_name] = f'go_to_the_shop_{SHOP.s_id}'

    for key, value in DICT.items():
        kb_game.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))

    return await update_message(
            query.message,
            person_status_card(PERS, STAT),
            kb_game
                )
