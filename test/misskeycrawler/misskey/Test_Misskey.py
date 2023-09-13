import sys
import unittest
from contextlib import ExitStack
from logging import getLogger
from unittest.mock import MagicMock

from mock import patch

from misskeycrawler.misskey.Misskey import Misskey

logger = getLogger("misskeycrawler.misskey.Misskey")


class TestMisskey(unittest.TestCase):
    def setUp(self) -> None:
        self.instance_name = "instance_name"
        self.token = "misskey_token"

    def get_instance(self) -> Misskey:
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_misskey = stack.enter_context(patch("misskeycrawler.misskey.Misskey.Mk"))
            misskey = Misskey(self.instance_name, self.token)
            return misskey

    def test_init(self):
        with ExitStack() as stack:
            mock_logger_info = stack.enter_context(patch.object(logger, "info"))
            mock_misskey = stack.enter_context(patch("misskeycrawler.misskey.Misskey.Mk"))
            misskey = Misskey(self.instance_name, self.token)
            mock_misskey.assert_called_once_with(self.instance_name, i=self.token)
            self.assertEqual(self.instance_name, misskey.instance_name)
            self.assertEqual(self.token, misskey.token)
            self.assertEqual(120, misskey.misskey.timeout)

    def test_user_dict(self):
        misskey = self.get_instance()
        misskey.misskey.i = MagicMock(return_value={"id": "user1user1"})
        actual = misskey.user_dict
        self.assertEqual({"id": "user1user1"}, actual)
        misskey.misskey.i.assert_called_once_with()
        misskey.misskey.i.reset_mock()

        actual = misskey.user_dict
        self.assertEqual({"id": "user1user1"}, actual)
        misskey.misskey.i.assert_not_called()

    def test_run(self):
        misskey = self.get_instance()
        misskey.misskey._Misskey__request_api = MagicMock(return_value="__request_api_return")
        path = "users/reactions"
        params = {
            "userId": "user1user1"
        }
        actual = misskey._run(path, params)
        self.assertEqual("__request_api_return", actual)
        misskey.misskey._Misskey__request_api.assert_called_once_with(path, **params)

    def test_notes_with_reactions(self):
        with ExitStack() as stack:
            mock_run = stack.enter_context(patch("misskeycrawler.misskey.Misskey.Misskey._run"))
            mock_run.side_effect = lambda path, params: params

            misskey = self.get_instance()
            misskey.misskey.i = MagicMock(return_value={"id": "user1user1"})
            limit = 10
            last_since_id = "last_since_id"
            actual = misskey.notes_with_reactions(limit, last_since_id)
            params = {
                "userId": "user1user1",
                "limit": int(limit),
                "sinceId": last_since_id
            }
            self.assertEqual(params, actual)


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
