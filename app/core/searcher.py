# -*- coding: utf-8 -*-
from __future__ import annotations

import wikipedia
import langid

import warnings

import random
import re


class _Searcher(object):
    _PAGE_LIMIT = 1 # ?

    def __init__(self: _Searcher) -> None:
        self._wiki = wikipedia
    
    def _set_lang_by_text(self, text: str) -> None:
        prefix = langid.classify(text)[0]
        prefix = 'en' if prefix == 'en' else 'ru'

        self._wiki.set_lang(prefix)
        self._lang = prefix
    
    def _enoru(self, en: str, ru: str) -> str:
        return en if self._lang == 'en' else ru

    def _filter(self, content: str) -> str:
        content = f"{self._enoru('== Introduction ==', '== Введение ==')}\n\n{content}"
        content = re.sub('  +|\n+', '\n', content)
        content = content.replace('—', '-')
        
        return content

    def surf(self, topic: str, summary: bool = False) -> str:
        warnings.simplefilter('ignore')

        self._set_lang_by_text(topic)

        content = f"{topic}: {self._enoru('nothing found', 'ничего не найдено')}"

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
