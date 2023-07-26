from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.exceptions import MessageToEditNotFound
from aiogram.utils.exceptions import BadRequest
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
    except BadRequest:
        await message.delete()
        await message.answer(
            MESS,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    except MessageToEditNotFound:
        await message.answer(
            MESS,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    try:
        await message.edit_reply_markup(keyboard)
    except MessageToEditNotFound:
        pass
