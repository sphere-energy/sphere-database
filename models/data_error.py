from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel
from models.test_metadata import TestMetadata


class DataError(BaseModel):
    __tablename__ = 'DATA_ERROR'

    test_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_METADATA.id'), primary_key=True)
    error_message: Mapped[str | None] = mapped_column(String)
    error_type: Mapped[str | None] = mapped_column(String)

    test_metadata: Mapped[TestMetadata | None] = relationship('TestMetadata', back_populates='data_error')
