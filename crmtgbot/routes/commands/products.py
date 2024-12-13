import logging

from aiogram import F, Router, types
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka
from lib.api.product_group import get_product_groups
from lib.keyboards.inline_markup.products import build_product_groups_kb
from lib.keyboards.reply_markup.menu import build_main_kb
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
async def handle_products(message: types.Message, client: FromDishka[RetailClient]):
    groups = get_product_groups(client)
    text = "Пожалуйста, выберите категорию товаров."
    await message.reply(
        text=text,
        reply_markup=build_product_groups_kb(groups),
    )
