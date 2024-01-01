import sys
import unittest

from mock import call, patch

from misskeycrawler.misskey_crawler import main


class TestMisskeyCrawler(unittest.TestCase):
    def test_main(self):
        self.enterContext(patch("misskeycrawler.misskey_crawler.logger.info"))
        mock_crawler = self.enterContext(patch("misskeycrawler.misskey_crawler.Crawler"))
        main()
        self.assertEqual([call(), call().run()], mock_crawler.mock_calls)


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
