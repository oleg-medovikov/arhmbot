from .dispetcher import dp
from aiogram import types

from clas import User, Location
from func import delete_message


@dp.message_handler(commands='test')
async def test_func(message: types.Message):
    "команда для того чтобы тестово что-то отправлять"
    await delete_message(message)
    USER = await User.get(message['from']['id'])
    if USER is None or not USER.admin:
        return None

    list_ = await Location.get_districts()

    MESS = str(list_)

    await message.answer(MESS)


