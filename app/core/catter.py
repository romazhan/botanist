# -*- coding: utf-8 -*-
from __future__ import annotations

import aiogram.types as types

import requests


class _Catter(object):
    _RANDOM_IMG_URL = 'https://api.thecatapi.com/v1/images/search'

    async def send_random_cat_img(self, msg: types.Message) -> None:
        img_url = requests.get(_Catter._RANDOM_IMG_URL).json()[0]['url']
        img_content = requests.get(img_url).content

        await msg.answer_photo(img_content)


catter = _Catter()
