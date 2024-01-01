import sys
import unittest
from datetime import datetime
from pathlib import Path

import orjson

from misskeycrawler.crawler.valueobject.fetched_info import FetchedInfo
from misskeycrawler.db.model import Media, Note, Reaction, User
from misskeycrawler.util import find_values, to_jst


class TestFetchedInfo(unittest.TestCase):
    def setUp(self) -> None:
        self.cache_filepath = Path("./tests/misskeycrawler/cache/test_notes_with_reactions.json")
        self.fetched_entry_list = orjson.loads(self.cache_filepath.read_bytes()).get("result")
        return super().setUp()

    def expect_create(self, fetched_dict: dict, instance_name: str = "") -> FetchedInfo:
        def normalize_date_at(date_at_str: str) -> str:
            result = to_jst(datetime.fromisoformat(date_at_str)).isoformat()
            if result.endswith("+00:00"):
                result = result[:-6]
            return result

        registered_at = datetime.now().isoformat()
        note_dict = find_values(fetched_dict, "note", True, [""])
        note_id = find_values(note_dict, "id", True, [""])

        media_dicts = []
        media_dicts = find_values(note_dict, "files", True, [""])

        media_list = []
        for media_dict in media_dicts:
            media_id = find_values(media_dict, "id", True, [""])
            media_name = find_values(media_dict, "name", True, [""])
            media_type = find_values(media_dict, "type", True, [""])
            media_md5 = find_values(media_dict, "md5", True, [""])
            media_size = find_values(media_dict, "size", True, [""])
            media_url = find_values(media_dict, "url", True, [""])
            media_created_at = normalize_date_at(find_values(media_dict, "createdAt", True, [""]))
            media = Media.create({
                "note_id": note_id,
                "media_id": media_id,
                "name": media_name,
                "type": media_type,
                "md5": media_md5,
                "size": media_size,
                "url": media_url,
                "created_at": media_created_at,
                "registered_at": registered_at,
            })
            media_list.append(media)

        reaction_id = find_values(fetched_dict, "id", True, [""])
        reaction_type = find_values(fetched_dict, "type", True, [""])
        reaction_created_at = normalize_date_at(find_values(fetched_dict, "createdAt", True, [""]))
        reaction = Reaction.create({
            "note_id": note_id,
            "reaction_id": reaction_id,
            "type": reaction_type,
            "created_at": reaction_created_at,
            "registered_at": registered_at,
        })

        user_id = find_values(note_dict, "userId", True, [""])
        note_url = f"https://{instance_name}/notes/{note_id}"
        note_text = find_values(note_dict, "text", True, [""])
        note_created_at = normalize_date_at(find_values(note_dict, "createdAt", True, [""]))
        note = Note.create({
            "note_id": note_id,
            "user_id": user_id,
            "url": note_url,
            "text": note_text,
            "created_at": note_created_at,
            "registered_at": registered_at,
        })

        user_dict = find_values(note_dict, "user", True, [""])
        user_username = find_values(user_dict, "username", True, [""])
        user_name = find_values(user_dict, "name", True, [""]) or user_username
        user_avatar_url = find_values(user_dict, "avatarUrl", True, [""])
        user_is_bot = find_values(user_dict, "isBot", True, [""])
        user_is_cat = find_values(user_dict, "isCat", True, [""])
        user = User.create({
            "user_id": user_id,
            "name": user_name,
            "username": user_username,
            "avatar_url": user_avatar_url,
            "is_bot": user_is_bot,
            "is_cat": user_is_cat,
            "registered_at": registered_at,
        })
        return FetchedInfo(reaction, note, user, media_list)

    def test_create(self):
        instance_name = "test.misskey.io"
        for entry in self.fetched_entry_list[:-1]:
            expect = self.expect_create(entry, instance_name)
            actual = FetchedInfo.create(entry, instance_name)
            self.assertEqual(expect, actual)

        entry = self.fetched_entry_list[-1]
        with self.assertRaises(ValueError):
            actual = FetchedInfo.create(entry)

    def test_get_records(self):
        instance_name = "test.misskey.io"
        for entry in self.fetched_entry_list[:-1]:
            expect = self.expect_create(entry, instance_name)
            actual = FetchedInfo.create(entry, instance_name)
            self.assertEqual(expect.get_records(), actual.get_records())


if __name__ == "__main__":
    if sys.argv:
        del sys.argv[1:]
    unittest.main(warnings="ignore")
