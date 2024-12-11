from aiogram import Router

from .commands import router as commands

router = Router(name="main_router")
for i in [
    commands.router,
]:
    router.include_router(i)
