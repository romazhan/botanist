# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Tuple

import googletrans


class _Translator(object):
    def __init__(self: _Translator) -> None:
        self._engine = googletrans.Translator()
    
    def _detect(self, text: str) -> Tuple[str, str]: # src, dest
        prefix = self._engine.detect(text).lang
        return ('ru', 'en') if prefix == 'ru' else (prefix, 'ru')
    
    def translate(self, text: str) -> str:
        src, dest = self._detect(text)
        return self._engine.translate(text, src=src, dest=dest).text


translator = _Translator()
