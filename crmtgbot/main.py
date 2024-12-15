import asyncio
import logging

from aiogram import Bot, Dispatcher
from core.config import AppConfig
from core.dependencies.container import container
from dishka.integrations.aiogram import setup_dishka
from lib.middlewares.error import ErrorHandlingMiddleware
from routes import router


async def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
    )

    config = await container.get(AppConfig)
    bot = Bot(
        token=config.bot.token,
    )
    dp = Dispatcher()
    dp.message.middleware(ErrorHandlingMiddleware())
    dp.callback_query.middleware(ErrorHandlingMiddleware())
    dp.include_router(router)

    setup_dishka(
        container=container,
        router=dp,
        auto_inject=True,
    )

    try:
        # THIS GOES LAST
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
