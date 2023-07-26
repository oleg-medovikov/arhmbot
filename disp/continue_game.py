from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text

from conf import MAX_HUNGER, MAX_WEARY
from clas import EventHistory, PersonStatus, Shop
from func import death_message, person_status_card, update_message, \
    demand, create_keyboard

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

    DICT = {}
    # если есть незаконченное событие, предложить его закончить
    try:
        await EventHistory.get(PERS.p_id)
    except ValueError:
        pass
    else:
        DICT['понимаю'] = 'get_event'

        return await update_message(
            query.message,
            'У вас незаконченное событие!',
            create_keyboard(DICT)
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
        DICT['попробовать ещё раз'] = 'start_new_game'

        # пишем эпитафию
        return await update_message(
            query.message,
            death_message(PERS, STAT),
            create_keyboard(DICT)
            )

    """
    если с персонажем все нормально,
    предложить меню дальнейших действий в городе
    """
    DICT = {
        'разветка':       'look_around',
        'подготовка':     'prepare_main',
        'действие':       'get_event',
        'переход':        'leave',
        }

    for SHOP in await Shop.get(STAT.location, STAT.stage):
        # тут нужно проверить, если персонаж не проходит проверку
        # маназина и нет сообщения, чтобы не показывать магазин
        if SHOP.mess_not_pass == 'None':
            if not await demand(PERS, STAT, SHOP.get_demand()):
                continue
        DICT[SHOP.shop_name] = f'go_to_the_shop_{SHOP.s_id}'

    return await update_message(
            query.message,
            person_status_card(PERS, STAT),
            create_keyboard(DICT)
            )
