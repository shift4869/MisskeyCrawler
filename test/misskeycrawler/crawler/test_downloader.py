import asyncio
import sys
import unittest
from contextlib import ExitStack
from logging import getLogger
from pathlib import Path

import orjson
from mock import AsyncMock, MagicMock, patch

from misskeycrawler.crawler.Downloader import Downloader

logger = getLogger("misskeycrawler.crawler.Downloader")


class TestDownloader(unittest.TestCase):
    config_path: Path = Path("./config/test_config.json")
    save_base_path: Path = Path("./test/misskeycrawler/crawler/")

    def setUp(self) -> None:
        config_dict = {
            "misskey": {
                "save_base_path": "./test/misskeycrawler/crawler/",
                "save_num": -1,
            }
        }
        self.config_path.write_bytes(orjson.dumps(config_dict))
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self) -> None:
        self.config_path.unlink(missing_ok=True)
        self.loop.stop()
        self.loop.close()

    def test_init(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            downloader = Downloader(self.config_path)
            self.assertEqual(self.save_base_path, downloader.save_base_path)
            self.assertEqual(-1, downloader.save_num)

    def test_worker(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_client = stack.enter_context(patch("misskeycrawler.crawler.Downloader.httpx.AsyncClient.get"))

            async def get_mock(url: str):
                r = MagicMock()
                r.content = url.encode()
                return r

            mock_client.side_effect = get_mock

            downloader = Downloader(self.config_path)
            filename = "media_filename.png"
            media = MagicMock()
            media.url = "media_url"
            media.get_filename.return_value = filename
            self.loop.run_until_complete(downloader.worker(media))

            self.assertEqual(True, (self.save_base_path / filename).exists())
            (self.save_base_path / filename).unlink(missing_ok=True)

    def test_excute(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_worker = stack.enter_context(patch("misskeycrawler.crawler.Downloader.Downloader.worker"))

            async def worker(media):
                return media

            mock_worker.side_effect = worker

            downloader = Downloader(self.config_path)
            media_list = ["media_list"]
            self.loop.run_until_complete(downloader.excute(media_list))
            mock_worker.assert_called_once_with(media_list[0])

    def test_download(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_excute = stack.enter_context(patch("misskeycrawler.crawler.Downloader.Downloader.excute"))

            downloader = Downloader(self.config_path)
            media_list = ["media_list"]
            actual = downloader.download(media_list)
            mock_excute.assert_called_once_with(media_list)


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
