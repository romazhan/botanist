# -*- coding: utf-8 -*-
from core.exceptions import TelegramTokenError

from core.kernel import Botanist

from dotenv import load_dotenv
from sys import argv
import asyncio, os


async def self_init() -> None:
    ROOT = os.path.dirname(argv[0])
    ROOT and os.chdir(ROOT)

    load_dotenv('./.env')

    TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TOKEN:
        raise TelegramTokenError('empty TELEGRAM_TOKEN in .env', True)

    bot, dispatcher = Botanist(TOKEN).get_instance()

    from core.startum import init_handlers
    init_handlers(dispatcher)

    await bot.run()

if __name__ == '__main__':
    asyncio.run(self_init())
