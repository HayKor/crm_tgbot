from aiogram import Router

from . import cart, products


router = Router(name=__name__)
for i in [
    products.router,
    cart.router,
]:
    router.include_router(i)
