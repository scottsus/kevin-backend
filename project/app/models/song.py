from typing import Optional

from app.models.base import PostgresBase
from sqlmodel import SQLModel


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, PostgresBase, table=True):
    __tablename__ = "songs"


class SongCreate(SongBase):
    pass
