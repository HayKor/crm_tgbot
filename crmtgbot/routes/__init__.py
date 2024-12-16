from aiogram import Router

from .callbacks import router as callbacks
from .commands import router as commands


router = Router(name="main_router")
for i in [
    commands.router,
    callbacks.router,
]:
    router.include_router(i)
