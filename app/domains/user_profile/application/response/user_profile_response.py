from typing import List, Dict, Any

from pydantic import BaseModel


class LikeHistoryItem(BaseModel):
    symbol: str
    count: int


class InteractionHistoryResponse(BaseModel):
    likes: List[LikeHistoryItem] = []
    comments: List[str] = []


class UserProfileResponse(BaseModel):
    account_id: int
    preferred_stocks: List[str] = []
    interaction_history: InteractionHistoryResponse = InteractionHistoryResponse()
    interests_text: str = ""
