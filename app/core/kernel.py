# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

from aiogram import Bot, enums
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.dispatcher import Dispatcher
import aiogram.exceptions
import aiogram.utils as utils

from .exceptions import TelegramTokenError

from datetime import datetime
from time import sleep

import gc


class Botanist(Bot):
    _PARSE_MODE = enums.ParseMode.HTML

    _DELAY_FOR_RESTART = 5 # sec

    def __init__(self: Botanist, telegram_token: str) -> None:
        Bot.__init__(
            self,
            telegram_token,
            default=DefaultBotProperties(
                parse_mode=Botanist._PARSE_MODE
            )
        )
        self._dispatcher = BotanistDispatcher()

    def _print_start_report(self) -> None:
        print(f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]: Botanist started ~")

    def get_instance(self) -> Tuple[Botanist, BotanistDispatcher]:
        return (self, self._dispatcher)

    async def run(self) -> None:
        self._print_start_report()
        try:
            await self._dispatcher.start_polling(self)

        except aiogram.exceptions.TelegramUnauthorizedError:
            raise TelegramTokenError('inactive TELEGRAM_TOKEN', False)

        except Exception as unhandled_error:
            print(f'[unhandled_error][botanist]: {unhandled_error}')
            sleep(Botanist._DELAY_FOR_RESTART)

            gc.collect()
            self.run()


class BotanistDispatcher(Dispatcher):
    pass
