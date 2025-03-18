from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

class TestStatus(BaseModel):
    __tablename__ = 'TEST_STATUS'
    # __table_args__ = {'quote': False}
    
    channel: Mapped[int | None] = mapped_column(BigInteger)
    chamber: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str | None] = mapped_column(String)

