import sys
import unittest
from datetime import datetime
from typing import Literal

from misskeycrawler.db.MediaDB import MediaDB
from misskeycrawler.db.Model import Media


class TestMediaDB(unittest.TestCase):
    def get_instance(self) -> MediaDB:
        controller = MediaDB(db_path=":memory:")
        return controller

    def get_record(
        self, id_num: int, type_kind: Literal["record", "list", "dict"] = "record"
    ) -> Media | list[Media] | list[dict]:
        now_date = datetime.now().isoformat()
        arg_dict = {
            "note_id": f"note_id_{id_num}",
            "media_id": f"media_id_{id_num}",
            "name": "name",
            "type": "text/jpeg",
            "md5": "md5",
            "size": 123,
            "url": "url",
            "created_at": now_date,
            "registered_at": now_date,
        }
        if type_kind == "dict":
            return arg_dict
        record = Media.create(arg_dict)
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

    def test_upsert(self):
        controller = self.get_instance()
        record1 = self.get_record(1)
        actual = controller.upsert(record1)
        self.assertEqual([0], actual)

        record1 = self.get_record(1)
        record1.name = "new_name"
        actual = controller.upsert(record1)
        self.assertEqual([1], actual)

        record2 = self.get_record(2)
        actual = controller.upsert([record2])
        self.assertEqual([0], actual)

        record2 = self.get_record(2)
        record2.name = "new_name"
        actual = controller.upsert([record2])
        self.assertEqual([1], actual)

        record3 = self.get_record(3, "dict")
        actual = controller.upsert([record3])
        self.assertEqual([0], actual)

        record3 = self.get_record(3, "dict")
        record3["name"] = "new_name"
        actual = controller.upsert([record3])
        self.assertEqual([1], actual)
        record3 = Media.create(record3)

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
