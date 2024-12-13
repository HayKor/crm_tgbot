from aiogram.filters.callback_data import CallbackData


class ProductCallBack(CallbackData, prefix="product"):
    id: int
