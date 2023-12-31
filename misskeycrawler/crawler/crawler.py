import time
from logging import getLogger
from pathlib import Path

from misskeycrawler.crawler.Downloader import Downloader
from misskeycrawler.crawler.Fetcher import Fetcher
from misskeycrawler.crawler.valueobject.FetchedInfo import FetchedInfo
from misskeycrawler.db.MediaDB import MediaDB
from misskeycrawler.db.NoteDB import NoteDB
from misskeycrawler.db.ReactionDB import ReactionDB
from misskeycrawler.db.UserDB import UserDB

logger = getLogger(__name__)


class Crawler:
    fetcher: Fetcher
    reaction_db: ReactionDB
    note_db: NoteDB
    user_db: UserDB
    media_db: MediaDB
    config_path: Path = Path("./config/config.json")

    def __init__(self) -> None:
        logger.info("Crawler init -> start")
        self.fetcher = Fetcher(self.config_path)
        self.downloader = Downloader(self.config_path)
        self.reaction_db = ReactionDB()
        self.note_db = NoteDB()
        self.user_db = UserDB()
        self.media_db = MediaDB()
        logger.info("Crawler init -> done")

    def run(self) -> None:
        logger.info("Crawler run -> start")
        instance_name = self.fetcher.misskey.instance_name

        # reaction_id をもとに最後につけたリアクションを取得
        last_reaction_id = ""
        last_reaction = self.reaction_db.select_last_record()
        if last_reaction:
            last_reaction_id = last_reaction.reaction_id
            last_note_id = last_reaction.note_id
            last_note_url = f"https://{instance_name}/notes/{last_note_id}"
            logger.info(f"Last reaction id is '{last_reaction_id}'.")
            logger.info(f"Last note url is '{last_note_url}'.")
        else:
            logger.info(f"Last reaction is not exist, first run.")

        # fetch
        start_time = time.time()
        fetched_list: list[FetchedInfo] = self.fetcher.fetch(last_reaction_id)
        elapsed_time = time.time() - start_time
        logger.info(f"Fetching : {elapsed_time} [sec].")
        if len(fetched_list) == 0:
            logger.info("No reaction created from last reaction.")
            logger.info("Crawler run -> done")
            return

        # FetchedInfo をそれぞれのリストに分解
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

        # メディアダウンロード・保存
        logger.info(f"Num of new media is {len(media_list)}.")
        start_time = time.time()
        self.downloader.download(media_list)
        elapsed_time = time.time() - start_time
        logger.info(f"Download : {elapsed_time} [sec].")

        # DB操作
        logger.info("DB control -> start.")
        self.reaction_db.upsert(reaction_list)
        self.note_db.upsert(note_list)
        self.user_db.upsert(user_list)
        self.media_db.upsert(media_list)
        logger.info("DB control -> done.")
        logger.info("Crawler run -> done")


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
