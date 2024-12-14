import logging

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lib.callback.enums.cart import CartActions


logger = logging.getLogger(__name__)


def build_cart_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="📦 Заказать",
        callback_data=CartActions.order,
    )

    builder.button(
        text="🗑️ Очистить",
        callback_data=CartActions.clean,
    )

    builder.adjust(1)
    return builder.as_markup()
