import collections

from core.util import read_yaml
from core.util import create_dir


class GameData:
    version: str
    source: str
    files: list


class Remote:
    cos: str
    wiki: str
    console: str
    gameData: GameData


class Save:
    data: str
    face: str
    rank: str
    style: str
    gacha: str
    classify: str
    database: str

    @classmethod
    def values(cls) -> collections.Iterable:
        pass


class Files:
    face: list
    rank: list
    style: list
    classify: list
    gacha: list
    database: list

    @classmethod
    def items(cls):
        pass


class ResourceConfig:
    remote: Remote
    save: Save
    files: Files


resource_config: ResourceConfig = read_yaml('config/private/resource.yaml')

for item in resource_config.save.values():
    create_dir(item)
