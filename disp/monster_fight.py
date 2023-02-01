from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uuid import uuid4

from clas import PersonStatus, Event, Monster, FightHistory
from func import update_message


@dp.callback_query_handler(Text(startswith=['monster_fight_']))
async def monster_fight(query: types.CallbackQuery):
    "Заканчиваем событие, сражением с монстром"

    E_ID = int(query.data.split('_')[-1])
    EVENT = await Event.get(E_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    MONSTER = await Monster.get(EVENT.get_monster())
    kb_event = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    CHOICE = 0 if 'hide' in query.data else 1
    MESS = query.message.text
    MESS += '\n\nВы выбрали ' + EVENT.get_choice()[CHOICE]

    if not CHOICE:
        # Если персонаж пробует спрятаться от монстра
        COUNT = STAT.stealth - MONSTER.check_of_stels
        DICT = await STAT.dice_roll(COUNT)
        MESS += '\nПроходим проверку на скрытность'
        MESS += f'\nКоличество бросков {COUNT}' + \
            (
                f'из них благодаря удаче {DICT["LUCK"]}\n' if DICT["LUCK"]
                else '\n'
            )
        for num in DICT['numbers']:
            MESS += f"  {num}\ufe0f\u20e3  "

        if DICT['success']:
            MESS += '\nВы успешно прошли проверку!\n\n'
            MESS += EVENT.mess_prize
            kb_event.add(InlineKeyboardButton(
                text='закончить событие',
                callback_data='continue_game'
                        ))

            return await update_message(
                    query.message,
                    MESS,
                    kb_event
                    )
        else:
            # Персонаж не прошёл проверку - тратит время и здоровье
            MESS += '\nВам не удалось пройти проверку! Придётся драться!'
            MESS += '\nВы потратили время и нервы на попытку'
            await STAT.waste_time(1)
            STAT = await STAT.change('mind', -1)

    # начинается сражение с монстром
    # Нужно создать непосредственно объект битвы

    BATLE = FightHistory(**{
        'gametime':   STAT.gametime,
        'p_id':       STAT.p_id,
        'm_id':       MONSTER.m_id,
        'm_uid':      uuid4(),
        'p_start_hp': STAT.health,
        'p_start_md': STAT.mind,
        'm_start_hp': MONSTER.health,
        })

    while BATLE.p_alive and BATLE.p_right_mind and BATLE.m_alive is True:
        BATLE = await BATLE.new_battle_round(STAT, MONSTER)

    BATLE_HISTORY = await FightHistory.get_history(BATLE.m_uid)

    MESS += '\n\n' + str(BATLE_HISTORY)

    kb_event.add(InlineKeyboardButton(
        text='закончить событие',
        callback_data='continue_game'
                ))

    return await update_message(
            query.message,
            MESS,
            kb_event
            )
