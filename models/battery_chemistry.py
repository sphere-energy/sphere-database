from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

class BatteryChemistry(BaseModel):
    __tablename__ = 'BATTERY_CHEMISTRY'
    # __table_args__ = {'quote': False}

    name: Mapped[str | None] = mapped_column(String)