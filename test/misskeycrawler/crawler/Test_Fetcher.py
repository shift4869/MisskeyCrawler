import sys
import unittest
from contextlib import ExitStack
from datetime import datetime
from logging import getLogger
from pathlib import Path

import freezegun
import orjson
from mock import patch

from misskeycrawler.crawler.Fetcher import Fetcher

logger = getLogger("misskeycrawler.crawler.Fetcher")


class TestFetcher(unittest.TestCase):
    config_path: Path = Path("./config/test_config.json")

    def setUp(self) -> None:
        config_dict = {
            "misskey": {
                "instance": "misskey.io",
                "token": "misskey_token",
            }
        }
        self.config_path.write_bytes(
            orjson.dumps(config_dict)
        )

    def tearDown(self) -> None:
        self.config_path.unlink(missing_ok=True)

    def test_init(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_misskey = stack.enter_context(patch("misskeycrawler.crawler.Fetcher.Misskey"))
            fetcher = Fetcher(self.config_path)
            mock_misskey.assert_called_once_with("misskey.io", "misskey_token")
            self.assertEqual(False, fetcher.is_debug)

    def test_fetch(self):
        with ExitStack() as stack:
            freeze_gun = stack.enter_context(freezegun.freeze_time("2023/09/11 00:00:00"))
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_misskey = stack.enter_context(patch("misskeycrawler.crawler.Fetcher.Misskey"))
            mock_fetched_info = stack.enter_context(patch("misskeycrawler.crawler.Fetcher.FetchedInfo"))

            mock_misskey().notes_with_reactions.side_effect = lambda limit, last_since_id: ["fetched_entry"]
            mock_misskey().instance_name = "misskey.io"
            mock_fetched_info.create.side_effect = lambda fetched_dict, instance_name: fetched_dict

            fetcher = Fetcher(self.config_path, False)
            fetcher.cache_path = Path("./test/misskeycrawler/cache")
            last_since_id = "last_since_id"
            actual = fetcher.fetch(last_since_id)
            self.assertEqual(["fetched_entry"], actual)
            mock_misskey().notes_with_reactions.assert_called_once_with(
                limit=100, last_since_id=last_since_id
            )
            mock_misskey().notes_with_reactions.reset_mock()
            mock_fetched_info.create.assert_called()
            mock_fetched_info.create.reset_mock()

            date_str = datetime.now().strftime("%Y%m%d%H%M%S")  # YYYYMMDDhhmmss
            cache_filename = f"{date_str}_notes_with_reactions.json"
            expect_cachepath = fetcher.cache_path / cache_filename
            self.assertEqual(True, expect_cachepath.exists())
            expect_cachepath.unlink(missing_ok=True)

            fetcher = Fetcher(self.config_path, True)
            fetcher.cache_path = Path("./test/misskeycrawler/cache")
            actual = fetcher.fetch(last_since_id)

            expect: list[dict] = orjson.loads(
                Path("./test/misskeycrawler/cache/test_notes_with_reactions.json").read_bytes()
            ).get("result")
            expect.reverse()
            self.assertEqual(expect, actual)
            mock_misskey().notes_with_reactions.assert_not_called()
            mock_fetched_info.create.assert_called()


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
