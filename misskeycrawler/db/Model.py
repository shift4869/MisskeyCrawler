from pathlib import Path
from typing import Self

from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class Reaction(Base):
    """リアクションモデル
        [id] INTEGER NOT NULL UNIQUE,
        [note_id] TEXT NOT NULL UNIQUE,
        [reaction_id] TEXT NOT NULL,
        [type] TEXT NOT NULL,
        [created_at] TEXT NOT NULL,
        PRIMARY KEY([id])
    """

    __tablename__ = "Reaction"

    id = Column(Integer, primary_key=True)
    note_id = Column(String(256), nullable=False, unique=True)
    reaction_id = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)
    created_at = Column(String(256), nullable=False)
    registered_at = Column(String(256), nullable=False)

    def __init__(self,
                 note_id: str,
                 reaction_id: str,
                 type: str,
                 created_at: str,
                 registered_at: str):
        # self.id = id
        self.note_id = note_id
        self.reaction_id = reaction_id
        self.type = type
        self.created_at = created_at
        self.registered_at = registered_at

    @classmethod
    def create(self, args_dict: dict) -> Self:
        match args_dict:
            case {
                "note_id": note_id,
                "reaction_id": reaction_id,
                "type": type,
                "created_at": created_at,
                "registered_at": registered_at,
            }:
                return Reaction(
                    note_id,
                    reaction_id,
                    type,
                    created_at,
                    registered_at
                )
            case _:
                raise ValueError("Unmatch args_dict.")

    def __repr__(self):
        return f"<Reaction(reaction_id='{self.reaction_id}', note_id='{self.note_id}')>"

    def __eq__(self, other):
        return isinstance(other, Reaction) and other.reaction_id == self.reaction_id and other.note_id == self.note_id

    def to_dict(self) -> dict:
        return {
            "note_id": self.note_id,
            "reaction_id": self.reaction_id,
            "type": self.type,
            "created_at": self.created_at,
            "registered_at": self.registered_at,
        }


class Note(Base):
    """ノートモデル
        [id] INTEGER NOT NULL UNIQUE,
        [note_id] TEXT NOT NULL UNIQUE,
        [user_id] TEXT NOT NULL,
        [url] TEXT NOT NULL,
        [text] TEXT,
        [created_at] TEXT NOT NULL,
        [registered_at] TEXT NOT NULL,
        PRIMARY KEY([id])
    """

    __tablename__ = "Note"

    id = Column(Integer, primary_key=True)
    note_id = Column(String(256), nullable=False, unique=True)
    user_id = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)
    text = Column(String(256))
    created_at = Column(String(256), nullable=False)
    registered_at = Column(String(256), nullable=False)

    def __init__(self,
                 note_id: str,
                 user_id: str,
                 url: str,
                 text: str,
                 created_at: str,
                 registered_at: str):
        # self.id = id
        self.note_id = note_id
        self.user_id = user_id
        self.url = url
        self.text = text
        self.created_at = created_at
        self.registered_at = registered_at

    @classmethod
    def create(self, args_dict: dict) -> Self:
        match args_dict:
            case {
                "note_id": note_id,
                "user_id": user_id,
                "url": url,
                "text": text,
                "created_at": created_at,
                "registered_at": registered_at,
            }:
                return Note(
                    note_id,
                    user_id,
                    url,
                    text,
                    created_at,
                    registered_at
                )
            case _:
                raise ValueError("Unmatch args_dict.")

    def __repr__(self):
        return f"<Note(note_id='{self.note_id}')>"

    def __eq__(self, other):
        return isinstance(other, Note) and other.note_id == self.note_id

    def to_dict(self) -> dict:
        return {
            "note_id": self.note_id,
            "user_id": self.user_id,
            "url": self.url,
            "text": self.text,
            "created_at": self.created_at,
            "registered_at": self.registered_at,
        }


class User(Base):
    """ユーザーモデル
        [id] INTEGER NOT NULL UNIQUE,
        [user_id] TEXT NOT NULL UNIQUE,
        [name] TEXT,
        [username] TEXT NOT NULL,
        [avatar_url] TEXT,
        [is_bot] BOOL,
        [is_cat] BOOL,
        [registered_at] TEXT NOT NULL,
        PRIMARY KEY([id])
    """

    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(256), nullable=False, unique=True)
    name = Column(String(256))
    username = Column(String(256), nullable=False)
    avatar_url = Column(String(512))
    is_bot = Column(Boolean)
    is_cat = Column(Boolean)
    registered_at = Column(String(256), nullable=False)

    def __init__(self,
                 user_id: str,
                 name: str,
                 username: str,
                 avatar_url: str,
                 is_bot: bool,
                 is_cat: bool,
                 registered_at: str):
        # self.id = id
        self.user_id = user_id
        self.name = name
        self.username = username
        self.avatar_url = avatar_url
        self.is_bot = is_bot
        self.is_cat = is_cat
        self.registered_at = registered_at

    @classmethod
    def create(self, args_dict: dict) -> Self:
        match args_dict:
            case {
                "user_id": user_id,
                "name": name,
                "username": username,
                "avatar_url": avatar_url,
                "is_bot": is_bot,
                "is_cat": is_cat,
                "registered_at": registered_at,
            }:
                return User(user_id,
                            name,
                            username,
                            avatar_url,
                            is_bot,
                            is_cat,
                            registered_at)
            case _:
                raise ValueError("Unmatch args_dict.")

    def __repr__(self):
        return f"<User(user_id='{self.user_id}')>"

    def __eq__(self, other):
        return isinstance(other, User) and other.user_id == self.user_id

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "is_bot": self.is_bot,
            "is_cat": self.is_cat,
            "registered_at": self.registered_at,
        }


class Media(Base):
    """メディアモデル
        [id] INTEGER NOT NULL UNIQUE,
        [note_id] TEXT NOT NULL,
        [media_id] TEXT NOT NULL UNIQUE,
        [name] TEXT,
        [type] TEXT NOT NULL,
        [md5] TEXT NOT NULL,
        [size] INTEGER NOT NULL,
        [url] TEXT NOT NULL,
        [created_at] TEXT NOT NULL,
        [registered_at] TEXT NOT NULL,
        PRIMARY KEY([id])
    """

    __tablename__ = "Media"

    id = Column(Integer, primary_key=True)
    note_id = Column(String(256), nullable=False)
    media_id = Column(String(256), nullable=False, unique=True)
    name = Column(String(256))
    type = Column(String(256), nullable=False)
    md5 = Column(String(256), nullable=False)
    size = Column(Integer, nullable=False)
    url = Column(String(512), nullable=False)
    created_at = Column(String(256), nullable=False)
    registered_at = Column(String(256), nullable=False)

    def __init__(self,
                 note_id: str,
                 media_id: str,
                 name: str,
                 type: str,
                 md5: str,
                 size: int,
                 url: str,
                 created_at: str,
                 registered_at: str):
        # self.id = id
        self.note_id = note_id
        self.media_id = media_id
        self.name = name
        self.type = type
        self.md5 = md5
        self.size = size
        self.url = url
        self.created_at = created_at
        self.registered_at = registered_at

    @classmethod
    def create(self, args_dict: dict) -> Self:
        match args_dict:
            case {
                "note_id": note_id,
                "media_id": media_id,
                "name": name,
                "type": type,
                "md5": md5,
                "size": size,
                "url": url,
                "created_at": created_at,
                "registered_at": registered_at,
            }:
                return Media(note_id,
                             media_id,
                             name,
                             type,
                             md5,
                             size,
                             url,
                             created_at,
                             registered_at)
            case _:
                raise ValueError("Unmatch args_dict.")

    def __repr__(self):
        return f"<Media(media_id='{self.media_id}', note_id='{self.note_id}')>"

    def __eq__(self, other):
        return isinstance(other, Media) and other.media_id == self.media_id and other.note_id == self.note_id

    def to_dict(self) -> dict:
        return {
            "note_id": self.note_id,
            "media_id": self.media_id,
            "name": self.name,
            "type": self.type,
            "md5": self.md5,
            "size": self.size,
            "url": self.url,
            "created_at": self.created_at,
            "registered_at": self.registered_at,
        }


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session

    test_db = Path("./test_DB.db")
    test_db.unlink(missing_ok=True)
    engine = create_engine(f"sqlite:///{test_db.name}", echo=True)
    Base.metadata.create_all(engine)

    session = Session(engine)
    result = session.query(Media).all()

    session.close()
    # test_db.unlink(missing_ok=True)
