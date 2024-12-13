from aiogram import Router, types
from dishka.integrations.aiogram import FromDishka
from lib.api.product import get_products
from lib.callback.product_group import ProductGroupCallBack
from lib.keyboards.inline_markup.products import build_products_kb
from retailcrm import v5 as RetailClient


router = Router(name=__name__)


@router.callback_query(ProductGroupCallBack.filter())
async def handle_product_group_cb(
    callback: types.CallbackQuery,
    client: FromDishka[RetailClient],
):
    cb_data = ProductGroupCallBack.unpack(callback.data)
    products = get_products(client, cb_data.id)
    if callback.message:
        await callback.message.reply(
            text=f"Товары по категории {cb_data.name}:",
            reply_markup=build_products_kb(products),
        )
    await callback.answer()
