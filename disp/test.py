from .dispetcher import dp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from clas import User, PersonStatus
from func import update_message


@dp.message_handler(commands='test')
async def test_func(message: types.Message):
    "команда для того чтобы тестово что-то отправлять"

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    PERS, STAT = await PersonStatus.get_all(message['from']['id'])
    res = STAT.dice_roll(2)

    # добавить предмет
    #await using_item(PERS, STAT, 1, True)
    #EVENT = await Event.get(0)
    #L = EVENT.get_check()

    kb_test = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )

    DICT = {
        'вперед!': 'dialog_1_1',
            }

    for key, value in DICT.items():
        kb_test.add(InlineKeyboardButton(
            text=key,
            callback_data=value
            ))

    MESS = "пробуем поговорить с продавцом хотдогов"

    return await message.answer(MESS, parse_mode='html',  reply_markup=kb_test)
