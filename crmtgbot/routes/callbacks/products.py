from aiogram import Router, types
from lib.callback.product_group import ProductGroupCallBack


router = Router(name=__name__)


@router.callback_query(ProductGroupCallBack.filter())
async def handle_product_group_cb(callback: types.CallbackQuery, cb_data: ProductGroupCallBack):
    await callback.answer()
