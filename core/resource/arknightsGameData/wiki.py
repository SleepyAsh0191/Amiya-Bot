import os

from typing import Dict, List
from core.network.download import download_async
from core.resource import resource_config
from core.util import create_dir
from core import log
from requests_html import HTMLSession, HTML

voices_source = 'resource/voice'


class Wiki:

    real_name_dist: Dict[str, List[str]] = dict()

    @classmethod
    async def download_operator_voices(cls, code, operator, voice, cn=False):
        async with log.catch('voices download error:'):
            filename = f'{operator}_{voice}%s.wav' % ('_cn' if cn else '')
            filepath = f'{voices_source}/{operator}/{filename}'
            url = f'{resource_config.remote.wiki}/voice%s/{code}/{operator}_{voice}.wav' % ('_cn' if cn else '')

            res = await download_async(url)
            if res:
                create_dir(f'{voices_source}/{operator}')
                with open(filepath, mode='wb+') as src:
                    src.write(res)
                return filepath

    @classmethod
    async def get_real_name(cls, operator: str = None):
        if not cls.real_name_dist:
            async with log.catch('wiki error:'):
                url = 'https://prts.wiki/w/%E8%A7%92%E8%89%B2%E7%9C%9F%E5%90%8D'
                html: HTML = HTMLSession().get(url).html

                data = {}
                for table in html.find('.wikitable'):
                    trs = table.find('tr')[2:]
                    for tr in trs:
                        tds = tr.find('td')
                        name = tds[1].text
                        reel_name = tds[2].text.split('\n')

                        data[name] = reel_name

                cls.real_name_dist = data

        if operator:
            if operator in cls.real_name_dist:
                return cls.real_name_dist[operator]
            else:
                return []

        return cls.real_name_dist

    @classmethod
    async def check_exists(cls, operator, voice, cn=False):
        file = f'{voices_source}/{operator}/{operator}_{voice}%s.wav' % ('_cn' if cn else '')
        if os.path.exists(file):
            return file
