from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

class AnodeChemistry(BaseModel):
    __tablename__ = 'ANODE_CHEMISTRY'

    name: Mapped[str | None] = mapped_column(String)