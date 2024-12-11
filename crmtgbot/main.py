import asyncio
import logging

from aiogram import Bot, Dispatcher

from crmtgbot.core.config import AppConfig


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s   %(name)-25s %(levelname)-8s %(message)s",
    )

    config = AppConfig.from_env()
    bot = Bot(
        token=config.bot.token,
    )
    dp = Dispatcher()

    try:
        # THIS GOES LAST
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
