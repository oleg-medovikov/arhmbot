from .dispetcher import dp
from aiogram import types

from clas import User, PersonStatus, Event
from func import delete_message, using_item


@dp.message_handler(commands='test')
async def test_func(message: types.Message):
    "команда для того чтобы тестово что-то отправлять"
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    PERS, STAT = await PersonStatus.get_all(message['from']['id'])
    res = STAT.dice_roll(2)

    # добавить предмет
    #await using_item(PERS, STAT, 1, True)
    #EVENT = await Event.get(0)
    #L = EVENT.get_check()



    MESS = str(res)

    await message.answer(MESS)
