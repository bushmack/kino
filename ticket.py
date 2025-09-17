from dataclasses import dataclass
from typing import Optional

@dataclass
class Ticket:
    id: Optional[int] = None
    row: int = None
    place: int = None
    name_movie: str = ''
    prise: float = 0.0