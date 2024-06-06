import sys
import unittest
from datetime import datetime
from typing import Literal

from misskey_crawler.db.model import Reaction
from misskey_crawler.db.reaction_db import ReactionDB


class TestReactionDB(unittest.TestCase):
    def get_instance(self) -> ReactionDB:
        controller = ReactionDB(db_path=":memory:")
        return controller

    def get_record(
        self, id_num: int, type_kind: Literal["record", "list", "dict"] = "record"
    ) -> Reaction | list[Reaction] | list[dict]:
        now_date = datetime.now().isoformat()
        arg_dict = {
            "note_id": f"note_id_{id_num}",
            "reaction_id": f"reaction_id_{id_num}",
            "type": "❤",
            "created_at": now_date,
            "registered_at": now_date,
        }
        if type_kind == "dict":
            return arg_dict
        record = Reaction.create(arg_dict)
        if type_kind == "list":
            return [record]
        return record

    def test_select(self):
        controller = self.get_instance()
        actual = controller.select()
        self.assertEqual([], actual)

        record = self.get_record(1)
        controller.upsert(record)
        actual = controller.select()
        record = self.get_record(1)
        self.assertEqual([record], actual)

    def test_select_last_record(self):
        controller = self.get_instance()
        actual = controller.select_last_record()
        self.assertEqual(None, actual)

        record = self.get_record(2)
        controller.upsert(record)
        record = self.get_record(3)
        controller.upsert(record)
        record = self.get_record(1)
        controller.upsert(record)
        actual = controller.select_last_record()
        expect = self.get_record(3)
        self.assertEqual(expect, actual)

    def test_upsert(self):
        controller = self.get_instance()
        record1 = self.get_record(1)
        actual = controller.upsert(record1)
        self.assertEqual([0], actual)

        record1 = self.get_record(1)
        record1.type = "new_type"
        actual = controller.upsert(record1)
        self.assertEqual([1], actual)

        record2 = self.get_record(2)
        actual = controller.upsert([record2])
        self.assertEqual([0], actual)

        record2 = self.get_record(2)
        record2.type = "new_type"
        actual = controller.upsert([record2])
        self.assertEqual([1], actual)

        record3 = self.get_record(3, "dict")
        actual = controller.upsert([record3])
        self.assertEqual([0], actual)

        record3 = self.get_record(3, "dict")
        record3["type"] = "new_type"
        actual = controller.upsert([record3])
        self.assertEqual([1], actual)
        record3 = Reaction.create(record3)

        actual = controller.select()
        self.assertEqual([record1, record2, record3], actual)

        record1 = self.get_record(1)
        record2 = self.get_record(2)
        actual = controller.upsert([record1, record2])
        self.assertEqual([1, 1], actual)

        with self.assertRaises(TypeError):
            record1 = self.get_record(1)
            actual = controller.upsert([record1, 1])
        with self.assertRaises(TypeError):
            actual = controller.upsert([])
        with self.assertRaises(TypeError):
            actual = controller.upsert("invalid_element")
        with self.assertRaises(TypeError):
            actual = controller.upsert(["invalid_element"])


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
