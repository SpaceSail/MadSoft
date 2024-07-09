from typing import Optional

from pydantic import BaseModel


class MemAdd(BaseModel):
    name: str
    description: Optional[str] = None


class MemGet(MemAdd):
    name: list[object]
    id: Optional[int] = None
