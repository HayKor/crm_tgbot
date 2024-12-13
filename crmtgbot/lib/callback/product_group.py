from aiogram.filters.callback_data import CallbackData


class ProductGroupCallBack(CallbackData, prefix="group"):
    id: int
    name: str
