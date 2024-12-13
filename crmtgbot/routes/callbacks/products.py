from aiogram import Router, types
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from dishka.integrations.aiogram import FromDishka
from lib.api.product import get_product, get_products
from lib.callback.product import ProductCallBack
from lib.callback.product_group import ProductGroupCallBack
from lib.keyboards.inline_markup.products import build_product_kb, build_products_kb
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


@router.callback_query(ProductCallBack.filter())
async def handle_product_cb(
    callback: types.CallbackQuery,
    client: FromDishka[RetailClient],
):
    cb_data = ProductCallBack.unpack(callback.data)
    product = get_product(client, cb_data.id)
    print(product)
    text = (
        f"{markdown.hide_link(url=product.imageUrl)}<b>Описание товара:</b> \n"
        f"<b>Наименование:</b> {product.name}\n"
        f"<b>Цена:</b> {product.offers[0]["price"]}\n"
        f"<b>Доставка:</b>: {product.offers[0]["prices"][0]["ordering"]}\n"
    )

    if callback.message:
        await callback.message.reply(
            text=text,
            reply_markup=build_product_kb(),
            parse_mode=ParseMode.HTML,
        )
    await callback.answer()
