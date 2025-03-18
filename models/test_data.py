from sqlalchemy import Float, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel
from models.test_metadata import TestMetadata
from sqlalchemy.dialects.postgresql import JSONB

class TestData(BaseModel):
    __tablename__ = 'TEST_DATA'
    # __table_args__ = {'quote': False}
    test_metadata_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_METADATA.id'))

    data_point: Mapped[int | None] = mapped_column(BigInteger)
    data_time: Mapped[Date | None] = mapped_column(Date)
    test_time: Mapped[float | None] = mapped_column(Float)
    step_time: Mapped[float | None] = mapped_column(Float)
    cycle_index: Mapped[int | None] = mapped_column(BigInteger)
    step_index: Mapped[int | None] = mapped_column(BigInteger)
    current: Mapped[float | None] = mapped_column(Float)
    voltage: Mapped[float | None] = mapped_column(Float)
    charge_capacity: Mapped[float | None] = mapped_column(Float)
    discharge_capacity: Mapped[float | None] = mapped_column(Float)
    charge_energy: Mapped[float | None] = mapped_column(Float)
    discharge_energy: Mapped[float | None] = mapped_column(Float)
    data_flags: Mapped[int | None] = mapped_column(BigInteger)
    additional_data: Mapped[dict | None] = mapped_column(JSONB)
    

    # test_metadata: Mapped[TestMetadata | None] = relationship('TestMetadata', back_populates='test_data')

