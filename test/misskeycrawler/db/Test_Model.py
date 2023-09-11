import sys
import unittest
from datetime import datetime
from pathlib import Path
from typing import Literal

from misskeycrawler.db.Model import Media, Note, Reaction, User


class TestUserDB(unittest.TestCase):
    def get_record(self, id_num: int, type_kind: Literal["record", "list", "dict"] = "record") -> Media | list[Media] | list[dict]:
        now_date = datetime.now().isoformat()
        arg_dict = {
            "note_id": f"note_id_{id_num}",
            "media_id": f"media_id_{id_num}",
            "name": "name.png",
            "type": "text/x-m4v",
            "md5": "md5",
            "size": 123,
            "url": "url.webp",
            "created_at": now_date,
            "registered_at": now_date,
        }
        if type_kind == "dict":
            return arg_dict
        record = Media.create(arg_dict)
        if type_kind == "list":
            return [record]
        return record

    def test_get_filename(self):
        media = self.get_record(1)
        ext = Path(media.url).suffix
        name = Path(media.name).with_suffix(ext).name
        expect = f"{media.note_id}_{media.media_id}_{name}"
        self.assertEqual(expect, media.get_filename())

        media = self.get_record(2)
        media.url = "url"
        ext = "." + media.type.split("/")[1]
        if ext.startswith(".x-"):
            ext = "." + ext[3:]
        name = Path(media.name).with_suffix(ext).name
        expect = f"{media.note_id}_{media.media_id}_{name}"
        self.assertEqual(expect, media.get_filename())

        media = self.get_record(3)
        media.url = "url"
        media.type = "/"
        ext = Path(media.name).suffix
        name = Path(media.name).with_suffix(ext).name
        expect = f"{media.note_id}_{media.media_id}_{name}"
        self.assertEqual(expect, media.get_filename())

        media = self.get_record(4)
        media.name = "name"
        ext = Path(media.url).suffix
        name = Path(media.name).with_suffix(ext).name
        expect = f"{media.note_id}_{media.media_id}_{name}"
        self.assertEqual(expect, media.get_filename())

        media = self.get_record(5)
        media.url = "url"
        media.type = ""
        media.name = "name"
        with self.assertRaises(ValueError):
            media.get_filename()


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
