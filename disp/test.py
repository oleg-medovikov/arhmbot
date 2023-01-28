from .dispetcher import dp
from aiogram import types

from clas import User,  PersonStatus
from func import delete_message, using_item


@dp.message_handler(commands='test')
async def test_func(message: types.Message):
    "команда для того чтобы тестово что-то отправлять"
    await delete_message(message)

    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    PERS, STAT = await PersonStatus.get_all(message['from']['id'])

    # добавить обувь
    # MESS = await using_item(PERS, STAT, 7, True)

    MESS = str(STAT)

    await message.answer(MESS)
