from aiogram.utils.exceptions import MessageNotModified
from aiogram import types


async def update_message(
        message: types.Message,
        MESS,
        keyboard: types.InlineKeyboardMarkup
        ) -> None:
    "удаление сообщения с обработкой исключения"

    try:
        await message.edit_text(MESS, parse_mode='Markdown')
    except MessageNotModified:
        pass

    await message.edit_reply_markup(keyboard)
