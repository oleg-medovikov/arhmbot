from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(DICT: dict) -> InlineKeyboardMarkup:
    "создаем клавиатуру"
    kb = InlineKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True
            )
    for key, value in DICT.items():
        kb.add(InlineKeyboardButton(
            text=key,
            callback_data=value,
        ))

    return kb
