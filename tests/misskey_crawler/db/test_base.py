import sys
import unittest
from contextlib import ExitStack

from mock import patch
from sqlalchemy.pool import StaticPool

from misskey_crawler.db.base import Base


class ConcreteBase(Base):
    def select(self):
        return []

    def upsert(self, record):
        return []


class TestBase(unittest.TestCase):
    def test_init(self):
        with ExitStack() as stack:
            mock_create_engine = stack.enter_context(patch("misskey_crawler.db.base.create_engine"))
            mock_model_base = stack.enter_context(patch("misskey_crawler.db.base.ModelBase"))

            mock_create_engine.return_value = "created_engine"

            db_path: str = "mc_db.db"
            base = ConcreteBase()
            self.assertEqual(db_path, base.db_path)
            self.assertEqual(f"sqlite:///{db_path}", base.db_url)
            mock_create_engine.assert_called_once_with(
                f"sqlite:///{db_path}",
                echo=False,
                poolclass=StaticPool,
                connect_args={
                    "timeout": 30,
                    "check_same_thread": False,
                },
            )
            mock_model_base.metadata.create_all.assert_called_once_with("created_engine")


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
