from uuid import UUID
from pydantic import BaseModel


class Character(BaseModel):
    work: str
    character: str


class BoxItem(BaseModel):
    box: list[float]
    box_id: UUID
    character: list[Character]


class AnimeTraceResult(BaseModel):
    ai: bool
    data: list[BoxItem]
    code: int
    trace_id: UUID
