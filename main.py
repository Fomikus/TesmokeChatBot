import asyncio
import logging
import sys
import time

from handlers import *
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from middlewares import *
from datetime import datetime
import config


async def periodic(bot):
    while True:
        await asyncio.sleep(5)
        now = datetime.utcnow()
        # await bot.send_message(chat_id=727685002, text=f"{now}")


async def main():
    dp = Dispatcher()
    dp.include_routers(
        dev_route,
        moder_route,
        missed_route
    )
    dp.message.outer_middleware(AutoRegister())

    bot = Bot(config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))

    asyncio.run_coroutine_threadsafe(periodic(bot), asyncio.get_event_loop())
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
