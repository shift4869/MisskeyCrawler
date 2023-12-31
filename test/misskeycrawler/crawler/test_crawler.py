import sys
import unittest
from contextlib import ExitStack
from logging import getLogger

from mock import MagicMock, patch

from misskeycrawler.crawler.crawler import Crawler

logger = getLogger("misskeycrawler.crawler.crawler")


class TestCrawler(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_init(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_fetcher = stack.enter_context(patch("misskeycrawler.crawler.crawler.Fetcher"))
            mock_downloader = stack.enter_context(patch("misskeycrawler.crawler.crawler.Downloader"))
            mock_reaction_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.ReactionDB"))
            mock_note_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.NoteDB"))
            mock_user_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.UserDB"))
            mock_media_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.MediaDB"))

            self.crawler = Crawler()
            mock_fetcher.assert_called_once_with(self.crawler.config_path)
            mock_downloader.assert_called_once_with(self.crawler.config_path)
            mock_reaction_db.assert_called_once_with()
            mock_note_db.assert_called_once_with()
            mock_user_db.assert_called_once_with()
            mock_media_db.assert_called_once_with()

    def test_run(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_fetcher = stack.enter_context(patch("misskeycrawler.crawler.crawler.Fetcher"))
            mock_downloader = stack.enter_context(patch("misskeycrawler.crawler.crawler.Downloader"))
            mock_reaction_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.ReactionDB"))
            mock_note_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.NoteDB"))
            mock_user_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.UserDB"))
            mock_media_db = stack.enter_context(patch("misskeycrawler.crawler.crawler.MediaDB"))

            self.crawler = Crawler()

            def make_reaction_id_mock(reaction_id):
                r = MagicMock()
                r.reaction_id = reaction_id
                return r

            reaction_id_mock = make_reaction_id_mock(111111)
            last_reaction_id = 111111
            mock_reaction_db().select_last_record.side_effect = lambda: reaction_id_mock

            def make_fetched_list_mock(args_last_reaction_id):
                r = MagicMock()
                r1 = [MagicMock() for _ in range(4)]
                r.get_records.side_effect = lambda: [r1]
                return [r]

            mock_fetcher().fetch.side_effect = make_fetched_list_mock

            actual = self.crawler.run()
            self.assertEqual(None, actual)
            mock_reaction_db().select_last_record.assert_called_once_with()
            mock_fetcher().fetch.assert_called_once_with(last_reaction_id)
            mock_downloader().download.assert_called_once()
            mock_reaction_db().upsert.assert_called_once()
            mock_note_db().upsert.assert_called_once()
            mock_user_db().upsert.assert_called_once()
            mock_media_db().upsert.assert_called_once()

            mock_reaction_db().reset_mock()
            mock_fetcher().reset_mock()
            mock_downloader().reset_mock()
            mock_reaction_db().reset_mock()
            mock_note_db().reset_mock()
            mock_user_db().reset_mock()
            mock_media_db().reset_mock()
            mock_fetcher().fetch.side_effect = lambda args_last_reaction_id: []

            actual = self.crawler.run()
            self.assertEqual(None, actual)
            mock_reaction_db().select_last_record.assert_called_once_with()
            mock_fetcher().fetch.assert_called_once_with(last_reaction_id)
            mock_downloader().download.assert_not_called()
            mock_reaction_db().upsert.assert_not_called()
            mock_note_db().upsert.assert_not_called()
            mock_user_db().upsert.assert_not_called()
            mock_media_db().upsert.assert_not_called()
        pass


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
