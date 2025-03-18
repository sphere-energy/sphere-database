
from sqlalchemy import String, BigInteger, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel


class Widget(BaseModel):
    __tablename__ = "WIDGET"
    
    test_metadata_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_METADATA.id'))
    workspace_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('WORKSPACE.id'))
    widget_type_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('WIDGET_TYPE.id'))

    name: Mapped[str | None] = mapped_column(String)
    is_default: Mapped[bool | None] = mapped_column(Boolean, default=False)

    __table_args__ = (UniqueConstraint(
        'workspace_id', 'name', name='unique_workspace_name'),)
