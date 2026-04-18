from pydantic import BaseModel
from enum import Enum


class Types(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Parsing(BaseModel):
    pass
