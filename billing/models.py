from sqlmodel import SQLModel, Field
from typing import Optional, List
import datetime


class BaseLoggedRequest(SQLModel):
    uuid: str
    n: int
    x: int
    rank: int
    date: datetime.datetime = Field(sa_column_kwargs={"default": datetime.datetime.utcnow()})


class LoggedRequest(BaseLoggedRequest, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    result: Optional[float] = Field(default=0.0)
    price: Optional[int] = Field(default=0)
