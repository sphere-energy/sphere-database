from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

class CathodeChemistry(BaseModel):
    __tablename__ = 'CATHODE_CHEMISTRY'

    name: Mapped[str | None] = mapped_column(String)