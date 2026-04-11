from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class InteractionType:
    LIKE = "like"
    COMMENT = "comment"
    CLICK = "click"


@dataclass
class UserInteraction:
    account_id: int
    symbol: str
    interaction_type: str
    count: int = 0
    content: Optional[str] = None
    created_at: datetime = None
    id: Optional[int] = None
