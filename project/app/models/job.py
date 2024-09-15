from typing import Any, Optional

from app.models.base import PostgresBase
from sqlalchemy.types import JSON
from sqlmodel import Column, Field, SQLModel


class Meta(SQLModel):
    columns: list[str]
    types: dict[str, str]
    num_rows: int


class JobBase(SQLModel):
    status: str
    data: list[dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    meta: dict = Field(default={}, sa_column=Column(JSON))


class Job(JobBase, PostgresBase, table=True):
    __tablename__ = "jobs"


class JobCreate(JobBase):
    csv_contents: str
    status: Optional[str]
    data: Optional[list]
    meta: Optional[dict]
