from .dispetcher import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uuid import uuid4

from clas import PersonStatus, Event, Monster, FightHistory, EventHistory
from func import update_message


@dp.callback_query_handler(Text(startswith=['monster_fight_']))
async def monster_fight(query: types.CallbackQuery):
    "Заканчиваем событие, сражением с монстром"

    E_ID = int(query.data.split('_')[-1])
    EVENT = await Event.get(E_ID)
    PERS, STAT = await PersonStatus.get_all(query.message['chat']['id'])
    EVENTHIS = await EventHistory.get(PERS.p_id)
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
        DICT = STAT.dice_roll(COUNT)
        LIST = (
                '\nПроходим проверку на скрытность',
                '\nКоличество бросков ', COUNT,
                f' из них благодаря удаче {DICT["luck"]}\n' if DICT["luck"]
                else '\n',
                *(f"  {x}\ufe0f\u20e3  " for x in DICT["numbers"]),
                )
        MESS += ''.join(str(x) for x in LIST)

        if DICT['success']:
            MESS += '\nВы успешно прошли проверку!\n\n'
            MESS += EVENT.mess_prize
            kb_event.add(InlineKeyboardButton(
                text='закончить событие',
                callback_data='continue_game'
                        ))
            EVENTHIS.result = False
            await EVENTHIS.write_result()

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

    for BATLE in await FightHistory.get_history(BATLE.m_uid):

        DICT_MD = BATLE.get_num_md()
        DICT_HP = BATLE.get_num_hp()

        LIST = (
            '\n\nРаунд боя ', BATLE.battle_round,
            '\nПроверка на рассудок, бросков: {len(DICT_MD["numbers"])}\n'
            if len(DICT_MD["numbers"]) else '',
            *(f"  {x}\ufe0f\u20e3  " for x in DICT_MD["numbers"]),

            '\nВы не испугались противника!' if DICT_MD["success"] else
            f'\nВы испугались противника, урон рассудку {BATLE.m_damage_md}',

            '\nПроверка боя, бросков: ', len(DICT_HP["numbers"]), '\n',
            *(f"  {x}\ufe0f\u20e3  " for x in DICT_HP["numbers"]),
            '\nВы нанесли ', BATLE.p_damage_hp, ' урона',
            '\nПротивник нанёс ', BATLE.m_damage_hp, ' урона',
            )

        MESS += ''.join(str(x) for x in LIST)

    MESS += '\n\n' + {
            BATLE.m_alive is False:      MONSTER.mess_win,
            BATLE.p_right_mind is False: MONSTER.mess_lose_md,
            BATLE.p_alive is False:      MONSTER.mess_lose_hp,
            }[True]

    # Заканчиваем событие
    EVENTHIS.result = True
    await EVENTHIS.write_result()

    # записываем изменения персонажа
    STAT.health = BATLE.p_end_hp
    STAT.mind = BATLE.p_end_md
    await STAT.update()
    await STAT.waste_time(BATLE.battle_round)

    kb_event.add(InlineKeyboardButton(
        text='закончить событие',
        callback_data='continue_game'
                ))

    return await update_message(
            query.message,
            MESS,
            kb_event
            )
