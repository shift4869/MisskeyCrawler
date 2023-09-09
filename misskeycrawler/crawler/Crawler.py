
import logging.config
from logging import INFO, getLogger
from pathlib import Path

from misskeycrawler.crawler.Fetcher import Fetcher
from misskeycrawler.crawler.valueobject.FetchedInfo import FetchedInfo
from misskeycrawler.db.MediaDB import MediaDB
from misskeycrawler.db.NoteDB import NoteDB
from misskeycrawler.db.ReactionDB import ReactionDB
from misskeycrawler.db.UserDB import UserDB

logging.config.fileConfig("./log/logging.ini", disable_existing_loggers=False)

logger = getLogger(__name__)
logger.setLevel(INFO)


class Crawler():
    fetcher: Fetcher
    reaction_db: ReactionDB
    note_db: NoteDB
    user_db: UserDB
    media_db: MediaDB
    config_path: Path = Path("./config/config.json")

    def __init__(self) -> None:
        self.fetcher = Fetcher(self.config_path)
        self.reaction_db = ReactionDB()
        self.note_db = NoteDB()
        self.user_db = UserDB()
        self.media_db = MediaDB()

    def run(self) -> None:
        # 最後にリアクションをつけた日付を取得
        reaction_list = self.reaction_db.select()
        last_reaction_id = max(
            [r.reaction_id for r in reaction_list]
        )

        # fetch
        fetched_list: list[FetchedInfo] = self.fetcher.fetch(last_reaction_id)
        reaction_list, note_list, user_list, media_list = [], [], [], []
        for fetched_record in fetched_list:
            records = fetched_record.get_records()
            for record in records:
                reaction, note, user, media = record
                if reaction not in reaction_list:
                    reaction_list.append(reaction)
                if note not in note_list:
                    note_list.append(note)
                if user not in user_list:
                    user_list.append(user)
                if media not in media_list:
                    media_list.append(media)

        # DB操作
        self.reaction_db.upsert(reaction_list)
        self.note_db.upsert(note_list)
        self.user_db.upsert(user_list)
        self.media_db.upsert(media_list)

        # メディア保存


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
