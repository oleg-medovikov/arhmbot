from aiogram import types
from .dispetcher import dp
from func import make_admin

@dp.message_handler(commands='cthulhu_fhtagn')
async def cthulhu_fhtagn(message: types.Message):
    try:
        await message.delete()
    except:
        pass

    U_ID = message['from']['id']

    if make_admin( U_ID ):
        MESS = 'Древний услышал тебя админ'
    else:
        MESS = 'Не в этот раз'

    await message.answer(MESS)


