import logging

from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from dishka.integrations.aiogram import FromDishka
from lib.api.product import get_products
from lib.api.product_group import get_product_groups
from lib.middlewares.error import ErrorHandlingMiddleware
from retailcrm import v5 as RetailClient


router = Router(name=__name__)
router.message.middleware(ErrorHandlingMiddleware())

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def handle_products(message: types.Message, client: FromDishka[RetailClient]):
    groups = get_product_groups(client)
    text = "Группы товаров: \n"
    for group in groups:
        if not group.active:
            continue
        text += group.name.title() + "\n"

    await message.reply(
        text=text,
    )


@router.message(Command("test"))
async def handle_product(message: types.Message, client: FromDishka[RetailClient]):
    groups = get_products(client, group_id=80)
    text = str(groups)

    await message.reply(
        text=text,
    )
