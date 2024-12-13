from aiogram import Router

from . import products


router = Router(name=__name__)
for i in [
    products.router,
]:
    router.include_router(i)
