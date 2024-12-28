from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_choice_kb() -> ReplyKeyboardMarkup:
    yes_btn = KeyboardButton(text="✅ Да")
    no_btn = KeyboardButton(text="❌ Нет")
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [yes_btn, no_btn],
        ],
        resize_keyboard=True,
    )
    return markup
