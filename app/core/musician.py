# -*- coding: utf-8 -*-
from __future__ import annotations

from bs4 import BeautifulSoup as BS

import aiogram.types as types

from typing import List, Union

import aiohttp

import random
import json
import os


class _Musician(object):
    _TARGET_DATA = {
        'site_url': 'https://eu.hitmotop.com',
        'tag': 'li',
        'class': 'tracks__item track mustoggler',
        'meta': 'data-musmeta'
    }

    _TEMP_PATH = './storage/temp/audio'

    _MAX_ATTEMPT_NUMBER = 5
    _MIN_BYTE_LENGTH = 9999

    def __init__(self: _Musician) -> None:
        self._http = aiohttp.ClientSession()

    def _create_temp_path(self, file_name: str) -> str:
        return f'{_Musician._TEMP_PATH}/' \
            f"{file_name.replace(' ', '_')}_" \
            f'{random.randint(100000, 999999)}.mp3'
    
    def _delete_file(self, file_path: str) -> None:
        try:
            os.remove(file_path)
        except (PermissionError, FileNotFoundError):
            pass

    async def _get_music_list(self) -> Union[List[str, str], None]: # [title, url] | None
        music_data = []

        target_data = _Musician._TARGET_DATA

        r = await self._http.get(target_data['site_url'])
        text_content = await r.text()

        soup = BS(text_content, features='lxml')
        
        tag_list = soup.find_all(target_data['tag'], {
            'class': target_data['class']
        })

        for tag in tag_list:
            music_meta = tag.get(target_data['meta'])

            json_list = json.loads(music_meta)
            music_data.append([json_list['title'], json_list['url']])
        
        return music_data

    async def _get_music_context(self) -> Union[List[str, bytes], None]: # [title, bytes] | None
        music_list = await self._get_music_list()

        if not music_list:
            return
        
        music_context = None
        for _ in range(0, _Musician._MAX_ATTEMPT_NUMBER):
            ml = random.choice(music_list)

            r = await self._http.get(ml[1])
            b = await r.read()

            if len(b) >= _Musician._MIN_BYTE_LENGTH:
                music_context = [ml[0], b]
                break

        return music_context

    def _save_music(self, music_context: List[str, bytes]) -> str:
        file_path = self._create_temp_path(music_context[0])
        with open(file_path, 'wb') as f:
            f.write(music_context[1])
        
        return file_path

    async def _send_music(self, msg: types.Message, file_path: str) -> None:
        file = open(file_path, 'rb')
        await msg.reply_audio(file)
        file.close()

        self._delete_file(file_path)

    async def send_random_music(self, msg: types.Message) -> None:
        music_context = await self._get_music_context()

        if not music_context:
            site_url = _Musician._TARGET_DATA['site_url']

            await msg.reply('Не удалось получить музыку...\n\n' \
                f"Сайт: <a href='{site_url}'>{site_url}</a>"
            )
            return

        file_path = self._save_music(music_context)
        await self._send_music(msg, file_path)


musician = _Musician()
