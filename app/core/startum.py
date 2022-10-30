# -*- coding: utf-8 -*-
from aiogram import types

from .kernel import BotanistDispatcher

from .docxer import ReportData, docxer
from .musician import musician


# front-controller:
def init_handlers(dispatcher: BotanistDispatcher) -> None:
    @dispatcher.message_handler(commands=['start'])
    async def _(msg: types.Message) -> None:
        await msg.answer('Started')


    @dispatcher.message_handler(commands=['report'])
    async def _(msg: types.Message) -> None:
        msg_report_args = msg.get_args().split(',')
        report_context = list(map(str.strip, msg_report_args))

        try:
            report_data = ReportData(
                discipline=report_context[0],
                topic=report_context[1],
                student=report_context[2],
                teacher=report_context[3],
            )

            await docxer.report(msg, report_data)
        except IndexError:
            await msg.reply(
                '<b>🛀🏽 Недостаточно аргументов</b>\n\n' \
                '🦧 Используйте следующий формат:\n' \
                '<code>/report дисциплина, тема, студент, учитель</code>'
            )
        except Exception as unhandled_error:
            print(f'[unhandled_error][report]: {unhandled_error}')
            await msg.reply('Ошибка на сервере...')


    @dispatcher.message_handler(commands=['music'])
    async def _(msg: types.Message) -> None:
        try:
            await musician.send_random_music(msg)
        except Exception as unhandled_error:
            print(f'[unhandled_error][music]: {unhandled_error}')
            await msg.reply('Музыки не будет...')
