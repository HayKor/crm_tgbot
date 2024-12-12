from aiogram import Router, types
from aiogram.filters import CommandStart
from dishka.integrations.aiogram import FromDishka
from lib.schemas.product_group import ProductGroup
from retailcrm import v5 as RetailClient


router = Router(name=__name__)


@router.message(CommandStart())
async def handle_products(message: types.Message, client: FromDishka[RetailClient]):
    response = client.product_groups(filters=[]).get_response()
    groups = response["productGroup"]
    text = "Группы товаров: \n"
    for group in groups:
        group_schema = ProductGroup.model_construct(**group)
        if not group_schema.active:
            continue
        text += group_schema.name + "\n"

    await message.reply(
        text=text,
    )
