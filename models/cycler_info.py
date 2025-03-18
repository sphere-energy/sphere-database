from sqlalchemy import String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel


class CyclerInfo(BaseModel):
    __tablename__ = 'CYCLER_INFO'
    
    arbin_raw_data_name: Mapped[str | None] = mapped_column(String)
    active_from: Mapped[DateTime | None] = mapped_column(DateTime)
    serial_number: Mapped[str | None] = mapped_column(String)
    short_name: Mapped[str | None] = mapped_column(String)
    long_name: Mapped[str | None] = mapped_column(String)