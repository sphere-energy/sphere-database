
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base_model import BaseModel


class WidgetType(BaseModel):
    __tablename__ = "WIDGET_TYPE"

    name: Mapped[str | None] = mapped_column(String)
