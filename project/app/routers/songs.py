from app.db import DB
from app.models.song import Song, SongCreate
from fastapi import APIRouter
from sqlmodel import select

router = APIRouter()


@router.get("/", response_model=list[Song])
async def get_songs(db: DB):
    result = await db.execute(select(Song))
    songs = result.scalars().all()

    return [
        Song(name=song.name, artist=song.artist, year=song.year, id=song.id)
        for song in songs
    ]


@router.post("/")
async def add_song(song: SongCreate, db: DB):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    db.add(song)
    await db.commit()
    await db.refresh(song)

    return song
