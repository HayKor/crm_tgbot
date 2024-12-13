from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lib.callback.product_group import ProductGroupCallBack
from lib.schemas.product_group import ProductGroupSchema


def build_product_groups_kb(groups: list[ProductGroupSchema]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for group in groups:
        cb_data = ProductGroupCallBack(id=group.id)
        builder.button(
            text=group.name.title(),
            callback_data=cb_data.pack(),
        )

    builder.adjust(2)
    return builder.as_markup()
