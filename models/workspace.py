from sqlalchemy import String, BigInteger, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel

class Workspace(BaseModel):
    """
    The Workspace model represents a user workspace entity in the system.

    Attributes:
        name (str | None): The name of the workspace.
        user_id (str | None): The identifier of the workspace owner.
        is_default (bool | None): Indicates whether this is the user’s default workspace.
    """

    __tablename__ = "WORKSPACE"

    name: Mapped[str | None] = mapped_column(String)
    user_id: Mapped[str | None] = mapped_column(String)
    is_default: Mapped[bool | None] = mapped_column(Boolean, default=False)

    __table_args__ = (UniqueConstraint(
        'user_id', 'name', name='unique_user_name'),)
