from datetime import datetime
import uuid
from typing import Optional

import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    public_id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    created_by: uuid.UUID = Field(foreign_key="user.public_id")
    created_at : datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
    )
    updated_by: uuid.UUID = Field(foreign_key="user.public_id")
    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": sa.func.now(), "server_default": sa.func.now()},
    )
    deleted_by: Optional[uuid.UUID] = Field(default=None, foreign_key="user.public_id")
    deleted_at: Optional[datetime] = Field(default=None)
