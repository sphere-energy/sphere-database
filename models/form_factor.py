from sqlalchemy import String, Float, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel

class FormFactor(BaseModel):
    __tablename__ = 'FORM_FACTOR'

    name: Mapped[str | None] = mapped_column(String)

    # Define relationships if necessary
    # cell_infos = relationship('CellInfo', back_populates='form_factor')