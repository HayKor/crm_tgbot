import logging

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka
from lib.api.product import get_products_by_ids
from lib.api.product_group import get_product_groups
from lib.callback.enums.menu import MenuStates
from lib.keyboards.inline_markup.products import build_product_groups_kb
from lib.keyboards.reply_markup.menu import build_main_kb
from lib.schemas.enums.redis import CartRedisKeyType
from redis.asyncio import Redis
from retailcrm import v5 as RetailClient


router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.reply(
        text="Приветствую в нашем магазине!",
        reply_markup=build_main_kb(),
    )


@router.message(F.text == "🎁 Наличие товара")
@router.callback_query(F.data == MenuStates.product_groups)
async def handle_products(event: types.Message | types.CallbackQuery, client: FromDishka[RetailClient]):
    groups = get_product_groups(client)
    text = "Пожалуйста, выберите категорию товаров."
    if isinstance(event, types.Message):
        await event.reply(
            text=text,
            reply_markup=build_product_groups_kb(groups),
        )
    else:
        await event.message.edit_text(
            text=text,
            reply_markup=build_product_groups_kb(groups),
        )


@router.message(F.text == "💰 Корзина")
async def handle_cart(message: types.Message, client: FromDishka[RetailClient], redis: FromDishka[Redis]):
    client_cart = CartRedisKeyType.cart.format(message.from_user.id)
    product_ids = await redis.smembers(client_cart)
    products = await get_products_by_ids(client, redis, list(product_ids))

    total_sum = 0
    text = "Ваша корзина: \n"
    for product in products:
        price = product.offers[0]["price"]
        ordering = product.offers[0]["prices"][0]["ordering"]
        text += f"{product.name} | {price} руб. | {ordering} руб.\n"
        total_sum += price + ordering

    text += f"\nВ сумме: {total_sum} руб."

    await message.reply(text=text)
