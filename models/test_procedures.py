from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base_model import BaseModel

class TestProcedures(BaseModel):
    __tablename__ = 'TEST_PROCEDURE'

    name: Mapped[str | None] = mapped_column(String)
