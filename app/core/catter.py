# -*- coding: utf-8 -*-
from __future__ import annotations

import aiogram.types as types

import aiohttp


class _Catter(object):
    _RANDOM_IMG_API_URL = 'https://api.thecatapi.com/v1/images/search'

    def __init__(self: _Catter) -> None:
        self._http = aiohttp.ClientSession()
    
    async def _get_cat_img_url(self) -> str:
        r = await self._http.get(_Catter._RANDOM_IMG_API_URL)
        r_json = await r.json()

        return r_json[0]['url']
    
    async def _get_cat_img_content(self) -> bytes:
        img_url = await self._get_cat_img_url()
        r = await self._http.get(img_url)

        return await r.read()

    async def send_random_cat_img(self, msg: types.Message) -> None:
        img_content = await self._get_cat_img_content()

        await msg.answer_photo(img_content)


catter = _Catter()
