# -*- coding: utf-8 -*-
from __future__ import annotations

from bs4 import BeautifulSoup as BS

import aiogram.types as types

from typing import List, Union

import aiohttp

import random
import json


class _Musician(object):
    _TARGET_DATA = {
        'site_url': 'https://eu.hitmotop.com',
        'tag': 'li',
        'class': 'tracks__item track mustoggler',
        'meta': 'data-musmeta'
    }

    _MAX_ATTEMPT_NUMBER = 5
    _MIN_BYTE_LENGTH = 9999

    def __init__(self: _Musician) -> None:
        self._http = aiohttp.ClientSession()

    async def _get_random_music_urls(self) -> Union[List[str], None]: # List[url] | None
        music_urls = []

        target_data = _Musician._TARGET_DATA

        r = await self._http.get(target_data['site_url'])
        text_content = await r.text()

        soup = BS(text_content, features='lxml')
        
        tag_list = soup.find_all(target_data['tag'], {
            'class': target_data['class']
        })

        for tag in tag_list:
            music_meta = tag.get(target_data['meta'])

            music_urls.append(json.loads(music_meta)['url'])
        
        return music_urls

    async def _get_random_music_bytes(self) -> Union[bytes, None]: # bytes | None
        music_urls = await self._get_random_music_urls()

        if not music_urls:
            return
        
        music_bytes = None
        for _ in range(0, _Musician._MAX_ATTEMPT_NUMBER):
            url = random.choice(music_urls)

            r = await self._http.get(url)
            b = await r.read()

            if len(b) >= _Musician._MIN_BYTE_LENGTH:
                music_bytes = b
                break

        return music_bytes

    async def send_random_music(self, msg: types.Message) -> None:
        music_bytes = await self._get_random_music_bytes()

        if not music_bytes:
            site_url = _Musician._TARGET_DATA['site_url']

            await msg.reply('Не удалось получить музыку...\n\n' \
                f"Сайт: <a href='{site_url}'>{site_url}</a>"
            )
            return

        await msg.reply_audio(music_bytes)


musician = _Musician()
