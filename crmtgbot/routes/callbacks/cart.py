from aiogram import F, Router, types
from dishka.integrations.aiogram import FromDishka
from lib.callback.cart import CartCallBack
from lib.callback.enums.cart import CartActions
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
