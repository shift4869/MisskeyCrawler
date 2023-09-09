
import pprint
from logging import INFO, getLogger
from pathlib import Path

import orjson

from misskeycrawler.crawler.valueobject.FetchedInfo import FetchedInfo
from misskeycrawler.misskey.Misskey import Misskey

logger = getLogger(__name__)
logger.setLevel(INFO)


class Fetcher():
    misskey: Misskey

    def __init__(self, config_path: Path) -> None:
        config_dict = orjson.loads(config_path.read_bytes())
        self.misskey = Misskey("misskey.io", config_dict["misskey"]["token"])
    
    def fetch(self, last_since_id: str) -> list[FetchedInfo]:
        fetched_entry_list: list[dict] = []
        if True:
            fetched_entry_list = self.misskey.notes_with_reactions(
                limit=100, last_since_id=last_since_id
            )
        else:
            cache_path = Path("./misskeycrawler/cache/")
            fetched_entry_list: list[dict] = orjson.loads(
                (cache_path / "notes_with_reactions.json").read_bytes()
            ).get("result")
        fetched_entry_list.reverse()

        fetched_info_list = []
        for entry in fetched_entry_list:
            fetched_info = FetchedInfo.create(entry)
            fetched_info_list.append(fetched_info)
        return fetched_info_list


if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)
    config_path: Path = Path("./config/config.json")
    cache_path = Path("./misskeycrawler/cache/")

    fetcher = Fetcher(config_path)
    response = fetcher.fetch()
    (cache_path / "notes_with_reactions.json").write_bytes(
        orjson.dumps({"result": response}, option=orjson.OPT_INDENT_2)
    )
    pprint.pprint(response)
