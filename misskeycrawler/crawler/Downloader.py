
import logging.config
import pprint
from logging import INFO, getLogger
from pathlib import Path

import orjson

from misskeycrawler.crawler.valueobject.FetchedInfo import FetchedInfo
from misskeycrawler.misskey.Misskey import Misskey

logger = getLogger(__name__)
logger.setLevel(INFO)


class Downloader():
    def __init__(self) -> None:
        pass

    def download(self, urls: list[str]) -> None:
        pass


if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)

    downloader = Downloader()
    response = downloader.download([
        "https://s3.arkjp.net/misskey/937f6abf-be32-4601-84dc-4fae22637b72.jpg"
    ])
    pprint.pprint(response)
