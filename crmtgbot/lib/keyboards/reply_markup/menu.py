from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def build_main_kb() -> ReplyKeyboardMarkup:
    buy_btn = KeyboardButton(text="💰 Корзина")
    products_btn = KeyboardButton(text="🎁 Наличие товара")
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [buy_btn, products_btn],
        ],
        resize_keyboard=True,
    )
    return markup
