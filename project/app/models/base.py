import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlmodel import Column, Field, SQLModel


class PostgresBase(SQLModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )
