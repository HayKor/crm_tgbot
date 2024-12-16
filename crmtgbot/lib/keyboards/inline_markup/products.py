import logging

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lib.callback.cart import CartCallBack
from lib.callback.enums.cart import CartActions
from lib.callback.enums.menu import MenuStates
from lib.callback.product import ProductCallBack
from lib.callback.product_group import ProductGroupCallBack
from lib.schemas.product import ProductSchema
from lib.schemas.product_group import ProductGroupSchema


logger = logging.getLogger(__name__)


def build_product_groups_kb(groups: list[ProductGroupSchema]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for group in groups:
        cb_data = ProductGroupCallBack(id=group.id, name=group.name)
        builder.button(
            text=group.name.title(),
            callback_data=cb_data.pack(),
        )

    builder.adjust(2)
    return builder.as_markup()


def build_products_kb(products: list[ProductSchema]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        cb_data = ProductCallBack(id=product.id)
        builder.button(
            text=product.name.title(),
            callback_data=cb_data.pack(),
        )

    builder.button(
        text="🔙 Назад",
        callback_data=MenuStates.product_groups,
    )

    builder.adjust(1)
    return builder.as_markup()


def build_product_kb(product_id: int, product_amount: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🛒 Добавить в корзину",
        callback_data=CartCallBack(
            product_id=product_id,
            product_amount=product_amount,
            action=CartActions.add,
        ),
    )
    builder.button(
        text="🔙 Назад",
        callback_data=MenuStates.product_groups,
    )

    builder.adjust(1)
    return builder.as_markup()
