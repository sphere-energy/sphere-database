from sqlalchemy import BigInteger, DateTime, func, Identity
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True, autoincrement=True, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
