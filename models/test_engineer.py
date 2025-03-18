from sqlalchemy import String, Float, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel

class TestEngineer(BaseModel):
    __tablename__ = 'TEST_ENGINEER'

    name: Mapped[str | None] = mapped_column(String)