import asyncio
import pprint
from logging import INFO, getLogger
from pathlib import Path

import httpx
import orjson

from misskeycrawler.db.Model import Media

logger = getLogger(__name__)
logger.setLevel(INFO)


class Downloader():
    save_base_path: Path
    save_num: int

    def __init__(self, config_path: Path) -> None:
        logger.info("Downloader init -> start")
        config_dict = orjson.loads(config_path.read_bytes())
        self.save_base_path = Path(config_dict["misskey"]["save_base_path"])
        self.save_num = int(config_dict["misskey"]["save_num"])

        self.save_base_path.mkdir(parents=True, exist_ok=True)
        logger.info("Downloader init -> done")

    async def worker(self, media: Media) -> None:
        async with httpx.AsyncClient(timeout=httpx.Timeout(5, read=60)) as client:
            url = media.url
            filename = media.get_filename()
            filepath = self.save_base_path / filename
            if filepath.exists():
                return

            response = await client.get(url)
            response.raise_for_status()

            filepath.write_bytes(
                response.content
            )

    async def excute(self, media_list: list[Media]) -> None:
        task_list = [self.worker(media) for media in media_list]
        await asyncio.gather(*task_list)

    def download(self, media_list: list[Media]) -> None:
        logger.info("Downloader download -> start")
        logger.info(f"Save base path : {str(self.save_base_path)} -> start")
        asyncio.run(self.excute(media_list))
        logger.info("Downloader download -> done")


if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)
    config_path = Path("./config/config.json")

    downloader = Downloader(config_path)
    media_dict1 = {
        "note_id": "9h7oxl4ilh",
        "media_id": "9h7ophtbg1",
        "name": "test1.jpg",
        "type": "image/jpeg",
        "md5": "",
        "size": -1,
        "url": "https://s3.arkjp.net/misskey/937f6abf-be32-4601-84dc-4fae22637b72.jpg",
        "created_at": "",
        "registered_at": "",
    }
    media1 = Media.create(media_dict1)
    media_dict2 = {
        "note_id": "9h7oxl4ilh",
        "media_id": "9h7opvugcz",
        "name": "test2.jpg",
        "type": "image/jpeg",
        "md5": "",
        "size": -1,
        "url": "https://s3.arkjp.net/misskey/50f2bf8e-e0ec-4906-a232-15266031cd44.jpg",
        "created_at": "",
        "registered_at": "",
    }
    media2 = Media.create(media_dict2)
    response = downloader.download([media1, media2])
    pprint.pprint(response)
