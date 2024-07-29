from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    blockchain: Mapped[str] = mapped_column(String(length=50))
    ticker: Mapped[str] = mapped_column(String(length=10))
