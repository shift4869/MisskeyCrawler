import pprint
from datetime import datetime
from logging import INFO, getLogger
from pathlib import Path

import orjson

from misskeycrawler.crawler.valueobject.fetched_info import FetchedInfo
from misskeycrawler.misskey_manager.misskey_manager import MisskeyManager

logger = getLogger(__name__)
logger.setLevel(INFO)


class Fetcher:
    misskey: MisskeyManager
    is_debug: bool
    cache_path = Path("./misskeycrawler/cache/")

    def __init__(self, config_path: Path, is_debug: bool = False) -> None:
        logger.info("Fetcher init -> start")
        config_dict = orjson.loads(config_path.read_bytes())
        instance_name = config_dict["misskey"]["instance"]
        token = config_dict["misskey"]["token"]
        self.misskey = MisskeyManager(instance_name, token)
        self.is_debug = is_debug

        self.cache_path.mkdir(parents=True, exist_ok=True)
        logger.info("Fetcher init -> done")

    def fetch(self, last_since_id: str = "") -> list[FetchedInfo]:
        logger.info("Fetcher fetch -> start")
        fetched_entry_list: list[dict] = []
        if not self.is_debug:
            logger.info("Fetch from misskey API -> start")
            fetched_entry_list = self.misskey.notes_with_reactions(limit=100, last_since_id=last_since_id)
            logger.info("Fetch from misskey API -> done")

            if len(fetched_entry_list) > 0:
                logger.info("Saving Cache -> start")
                date_str = datetime.now().strftime("%Y%m%d%H%M%S")  # YYYYMMDDhhmmss
                cache_filename = f"{date_str}_notes_with_reactions.json"
                save_path = self.cache_path / cache_filename
                save_path.write_bytes(orjson.dumps({"result": fetched_entry_list}, option=orjson.OPT_INDENT_2))
                logger.info(f"Saved for {str(save_path)}.")
                logger.info("Saving Cache -> done")
        else:
            logger.info("Fetch from cache file -> start")
            load_paths: list[Path] = [p for p in self.cache_path.glob("*notes_with_reactions.json*")]
            if len(load_paths) == 0:
                raise ValueError("Cache file is not exist.")
            load_path: Path = load_paths[-1]
            fetched_entry_list: list[dict] = orjson.loads(load_path.read_bytes()).get("result")
            logger.info(f"Loaded from {str(load_path)}.")
            logger.info("Fetch from cache file -> done")
        fetched_entry_list.reverse()

        logger.info("Create FetchedInfo -> start")
        fetched_info_list = []
        for entry in fetched_entry_list:
            try:
                fetched_info = FetchedInfo.create(entry, self.misskey.instance_name)
            except Exception as e:
                logger.error(e)
                continue
            fetched_info_list.append(fetched_info)
        logger.info("Create FetchedInfo -> done")
        logger.info("Fetcher fetch -> done")
        return fetched_info_list


if __name__ == "__main__":
    import logging.config

    logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)
    config_path: Path = Path("./config/config.json")
    cache_path = Path("./misskeycrawler/cache/")

    fetcher = Fetcher(config_path, is_debug=True)
    response = fetcher.fetch()
    (cache_path / "notes_with_reactions.json").write_bytes(
        orjson.dumps({"result": response}, option=orjson.OPT_INDENT_2)
    )
    pprint.pprint(response)
