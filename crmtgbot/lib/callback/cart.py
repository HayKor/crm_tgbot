from aiogram.filters.callback_data import CallbackData

from .enums.cart import CartActions


class CartCallBack(CallbackData, prefix="cart"):
    product_id: int
    product_amount: int
    action: CartActions
