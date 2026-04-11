from sqlalchemy import Column, Integer, String, Text

from app.infrastructure.database.session import Base


class UserProfileORM(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, nullable=False, unique=True)
    preferred_stocks = Column(Text, nullable=False, default="")   # JSON 문자열로 저장 ex) '["005930","000660"]'
    interests_text = Column(Text, nullable=False, default="")
