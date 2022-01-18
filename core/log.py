import os
import sys
import time
import traceback

from typing import Union, List, Any, Callable, Coroutine
from contextlib import asynccontextmanager

INFO_TYPE = Union[str, int, float, bool]
MESSAGE_TYPE = Union[INFO_TYPE, List[INFO_TYPE]]
ERROR_TYPE = Union[Exception, MESSAGE_TYPE]


class ServerLog:
    @classmethod
    def write(cls, text: str):
        info(text.strip('\n'))


def info(message: MESSAGE_TYPE, level: str = 'info') -> str:
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    if type(message) is list:
        indent = (len(date) + len(level) + 5) * ' '
        text = message[0] + '\n' + '\n'.join([indent + row for row in message[1:]])
    else:
        text = str(message)

    data = {
        'time': date,
        'level': level.upper(),
        'message': text[0].upper() + text[1:]
    }

    msg = '[{time}][{level}] {message}'.format(**data)

    writer(msg)

    return msg


def error(message: ERROR_TYPE, desc: str = None) -> str:
    text = message

    if isinstance(message, Exception):
        text = traceback.format_exc()

    if desc:
        text = f'{desc} {text}'

    return info(text, level='error')


def writer(text: str, out=True):
    now = time.localtime()
    path = f'fileStorage/log/{now.tm_year}{now.tm_mon}{now.tm_mday}'
    file = f'{path}/{now.tm_hour}.txt'

    try:
        if not os.path.exists(path):
            os.makedirs(path)

        with open(file, mode='a+', encoding='utf-8') as f:
            f.write(text + '\r\n')
    finally:
        if out:
            print(text)


def progress_bar(data: Union[dict, list], desc: str = ''):
    data = data.keys() if type(data) is dict else data
    desc = f'{desc}: ' if desc else ''
    msg = ''

    def print_bar(i):
        nonlocal msg

        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        curr = int(i / len(data) * 100)
        block = int(curr / 4)
        bar = '=' * block + ' ' * (25 - block)
        msg = f'[{date}][INFO] {desc}[{bar}] {curr}% {i}/{len(data)}'

        print('\r', end='')
        print(msg, end='')

        sys.stdout.flush()

    print_bar(0)
    for index, item in enumerate(data):
        yield item
        print_bar(index + 1)

    print()
    writer(msg, out=False)


@asynccontextmanager
async def catch(desc: str = None, handler: Callable[[str], Coroutine] = None, ignore: List[Any] = None):
    try:
        yield
    except Exception as err:
        if ignore and type(err) in ignore:
            return

        error_message = error(err, desc)

        if handler and error_message:
            await handler(error_message)
