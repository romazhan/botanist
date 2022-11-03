# -*- coding: utf-8 -*-
from __future__ import annotations

import wikipedia

import warnings

import random
import re


class _Searcher(object):
    _PAGE_LIMIT = 1 # ?

    def __init__(self: _Searcher) -> None:
        self._wiki = wikipedia
        self._wiki.set_lang('ru')

    def _filter(self, content: str) -> str:
        content = f'== Введение ==\n\n{content}'
        content = re.sub('  +|\n+', '\n', content)
        content = content.replace('—', '-')
        
        return content

    def surf(self, topic: str, summary: bool = False) -> str:
        warnings.simplefilter('ignore')

        content = f'{topic}: ничего не найдено'

        def _surf(pages: list) -> None:
            nonlocal content

            if pages:
                page = random.choice(pages)
                try:
                    if summary:
                        content = self._wiki.summary(page, auto_suggest=False)
                    else:
                        content = self._filter(
                            self._wiki.page(page, auto_suggest=False).content
                        )
                except wikipedia.exceptions.DisambiguationError:
                    pages.remove(page)
                    _surf(pages)
        
        _surf(self._wiki.search(topic)[:_Searcher._PAGE_LIMIT] or [])
        
        return content


searcher = _Searcher()
