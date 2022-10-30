# -*- coding: utf-8 -*-
from __future__ import annotations

import wikipedia

import warnings

import random
import re


class Searcher(object):
    _PAGE_LIMIT = 5

    def __init__(self: Searcher) -> None:
        self._wiki = wikipedia
        self._wiki.set_lang('ru')

    def _filter(self, content: str) -> str:
        content = f'== Введение ==\n\n{content}'
        content = re.sub('  +|\n+', '\n', content)
        content = content.replace('—', '-')

        return content

    def surf(self, topic: str) -> str: # content
        warnings.simplefilter('ignore')

        content = 'Контент не найден...'

        def _surf(pages: list) -> None:
            nonlocal content

            if pages:
                page = random.choice(pages)
                try:
                    content = self._filter(
                        self._wiki.page(page, auto_suggest=False).content
                    )
                except wikipedia.exceptions.DisambiguationError:
                    pages.remove(page)
                    _surf(pages)
        
        _surf(self._wiki.search(topic)[:Searcher._PAGE_LIMIT] or [])
        
        return content
