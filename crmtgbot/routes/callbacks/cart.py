import logging
from typing import Any

from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from core.config import AppConfig
from dishka.integrations.aiogram import FromDishka
from lib.api.order import create_order
from lib.api.product import get_products_by_ids
from lib.callback.cart import CartCallBack
from lib.callback.enums.cart import CartActions
from lib.keyboards.inline_markup.cart import build_cart_kb
from lib.keyboards.reply_markup.menu import build_main_kb
from lib.keyboards.reply_markup.order import build_choice_kb
from lib.schemas.enums.redis import CartRedisKeyType
from lib.states.order import OrderStates
from redis.asyncio import Redis
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.callback_query(CartCallBack.filter(F.action == CartActions.add))
async def handle_cart_add_cb(
    callback: types.CallbackQuery,
    redis: FromDishka[Redis],
):
    cb_data = CartCallBack.unpack(callback.data)
    if cb_data.product_amount:
        client_cart = CartRedisKeyType.cart.format(callback.from_user.id)
        await redis.sadd(client_cart, str(cb_data.product_id))
        await callback.answer("Товар добавлен в корзину. Можете продолжить покупки.")
    else:
        await callback.answer("Сейчас нету этого товара в наличии.")


@router.callback_query(F.data == CartActions.clean)
async def handle_cart_clean_cb(
    callback: types.CallbackQuery,
    redis: FromDishka[Redis],
):
    client_cart = CartRedisKeyType.cart.format(callback.from_user.id)
    await redis.delete(client_cart)
    await callback.answer("Корзина очищена.")
    if callback.message:
        await callback.message.edit_text(
            text="Ваша корзина: \n\nВ сумме: 0 руб.",
            reply_markup=build_cart_kb(),
        )


@router.callback_query(F.data == CartActions.order)
async def handle_cart_order_cb(
    callback: types.CallbackQuery,
    state: FSMContext,
    redis: FromDishka[Redis],
):
    client_cart = CartRedisKeyType.cart.format(callback.from_user.id)
    if await redis.smembers(client_cart):  # type: ignore
        await state.set_state(OrderStates.shipping)
        await callback.answer()
        if callback.message:
            await callback.message.reply(
                text="Пожалуйста, выберете, нужна ли вам доставка?",
                reply_markup=build_choice_kb(),
            )
    else:
        await callback.answer("Ваша корзина пуста.")


@router.message(OrderStates.shipping)
async def handle_shipping_order(
    message: types.Message,
    state: FSMContext,
):
    text = message.text
    if text in ["✅ Да", "❌ Нет"]:
        choice = text == "✅ Да"
        await state.update_data(shipping=choice)
        await state.set_state(OrderStates.fullname)
        await message.reply(
            text="Пожалуйста, напишите свои имя и фамилию через пробел.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            text="Пожалуйста, выберете, нужна ли вам доставка?",
            reply_markup=build_choice_kb(),
        )


@router.message(OrderStates.fullname)
async def handle_fullname_order(
    message: types.Message,
    state: FSMContext,
):
    fullname = message.text
    if fullname is not None and len(fullname.split()) == 2:
        await state.update_data(fullname=message.text)
        await state.set_state(OrderStates.phone)
        await message.reply(
            text="Пожалуйста, напишите свой номер телефона.",
        )
    else:
        await message.reply(
            text="Пожалуйста, введите имя и фамилию.",
        )


@router.message(OrderStates.phone)
async def handle_phone_number_order(
    message: types.Message,
    state: FSMContext,
    config: FromDishka[AppConfig],
    redis: FromDishka[Redis],
    client: FromDishka[RetailClient],
):
    data = await state.update_data(
        phone=message.text,
    )
    await create_crm_order(
        message=message,
        data=data,
        manager_id=config.management.manager_id,
        user=message.from_user,
        redis=redis,
        client=client,
    )

    await message.answer(
        text="Спасибо! Ваш заказ отправлен, скоро его обработают наши менеджеры.",
        reply_markup=build_main_kb(),
    )
    await state.clear()


async def create_crm_order(
    message: types.Message,
    data: dict[str, Any],
    manager_id: int,
    user: types.User,
    redis: Redis,
    client: RetailClient,
) -> None:
    client_cart = CartRedisKeyType.cart.format(user.id)
    product_ids = await redis.smembers(client_cart)
    products = await get_products_by_ids(client, redis, list(product_ids))
    if not create_order(
        client=client,
        products=products,
        phone=data["phone"],
        nickname=user.username,
        fullname=data["fullname"],
    ):
        await message.answer("Что-то пошло не так...")
        logger.error("Couldn't create order with data: %s", data)
        return
    text = (
        "Новый заказ!\n"
        f"<b>Никнейм</b>: {"@" + user.username if user.username else "нету"}\n"
        f"<b>Имя и фамилия</b>: {data["fullname"]}\n"
        f"<b>Ссылка на аккаунт</b>: {user.url}\n"
        f"<b>Номер телефона</b>: <code>{data["phone"]}</code>\n\n"
        f"<b>Доставка</b>: <b>{"✅ Да" if data["shipping"] else "❌ Нет"}</b>\n\n"
    )
    text += "<b>Состав</b>\n"
    for product in products:
        text += f"{product.name}\n"
    if message.bot:
        await message.bot.send_message(
            chat_id=manager_id,
            text=text,
            parse_mode=ParseMode.HTML,
        )
    await redis.delete(client_cart)
