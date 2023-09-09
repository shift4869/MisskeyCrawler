# coding: utf-8
import re
from typing import Self

from sqlalchemy import and_, asc, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from misskeycrawler.db.Base import Base
from misskeycrawler.db.Model import Media


class MediaDB(Base):
    def __init__(self, db_path: str = "mc_db.db"):
        super().__init__(db_path)

    def select(self):
        Session = sessionmaker(bind=self.engine, autoflush=False)
        session = Session()
        result = session.query(Media).all()
        session.close()
        return result

    def upsert(self, record: Media | list[Media] | list[dict]) -> list[int]:
        """upsert

        Args:
            record (Media | list[dict] | list[Media]): 投入レコード、またはレコード辞書のリスト

        Returns:
            list[int]: レコードに対応した投入結果のリスト
                       追加したレコードは0、更新したレコードは1が入る
        """
        result: list[int] = []
        record_list: list[Media] = []
        if isinstance(record, Media):
            record_list = [record]
        elif isinstance(record, list):
            if len(record) == 0:
                raise ValueError("record list is empty.")
            if isinstance(record[0], dict):
                record_list = [Media.create(r) for r in record]
            elif isinstance(record[0], Media):
                record_list = record
            else:
                raise ValueError("record list include invalid element.")

        Session = sessionmaker(bind=self.engine, autoflush=False)
        session = Session()

        for r in record_list:
            try:
                q = session.query(Media).filter(
                    and_(Media.media_id == r.media_id, Media.note_id == r.note_id)
                ).with_for_update()
                p = q.one()
            except NoResultFound:
                # INSERT
                session.add(r)
                result.append(0)
            else:
                # UPDATE
                p.note_id = r.note_id
                p.media_id = r.media_id
                p.name = r.name
                p.type = r.type
                p.md5 = r.md5
                p.size = r.size
                p.url = r.url
                p.created_at = r.created_at
                p.registered_at = r.registered_at
                result.append(1)

        session.commit()
        session.close()
        return result
