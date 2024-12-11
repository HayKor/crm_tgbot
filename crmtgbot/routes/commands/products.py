from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router(name=__name__)


@router.message(CommandStart())
async def handle_products(message: types.Message):
    await message.reply(
        text="Hello!",
    )
