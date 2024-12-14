from aiogram import F, Router, types
from dishka.integrations.aiogram import FromDishka
from lib.callback.cart import CartCallBack
from lib.callback.enums.cart import CartActions
from lib.keyboards.inline_markup.cart import build_cart_kb
from lib.schemas.enums.redis import CartRedisKeyType
from redis.asyncio import Redis


router = Router(name=__name__)


@router.callback_query(CartCallBack.filter(F.action == CartActions.add))
async def handle_cart_add_cb(
    callback: types.CallbackQuery,
    redis: FromDishka[Redis],
):
    cb_data = CartCallBack.unpack(callback.data)
    client_cart = CartRedisKeyType.cart.format(callback.from_user.id)
    await redis.sadd(client_cart, str(cb_data.product_id))
    await callback.answer("Товар добавлен в корзину. Можете продолжить покупки.")


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
