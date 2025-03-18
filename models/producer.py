from sqlalchemy import String, Float, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel

class Producer(BaseModel):
    __tablename__ = 'CELL_PRODUCER'

    name: Mapped[str | None] = mapped_column(String)