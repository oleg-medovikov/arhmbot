from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram import types


async def delete_message(message: types.Message) -> None:
    "удаление сообщения с обработкой исключения"
    try:
        await message.delete()
    except MessageToDeleteNotFound:
        pass
