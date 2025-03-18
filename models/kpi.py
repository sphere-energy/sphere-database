from sqlalchemy import String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel
from models.test_data import TestData

class KPI(BaseModel):
    __tablename__ = 'KPI'

    cycle_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_DATA.id'), primary_key=True)

    I_max_ch: Mapped[float | None] = mapped_column(Float)
    I_max_dch: Mapped[float | None] = mapped_column(Float)
    T_max_ch: Mapped[float | None] = mapped_column(Float)
    T_max_dch: Mapped[float | None] = mapped_column(Float)
    U_max: Mapped[float | None] = mapped_column(Float)
    U_min: Mapped[float | None] = mapped_column(Float)
    average_voltage_ch_cc: Mapped[float | None] = mapped_column(Float)
    average_voltage_dch_cc: Mapped[float | None] = mapped_column(Float)
    new_column: Mapped[float | None] = mapped_column(Float)
    capacity_ch_cc: Mapped[float | None] = mapped_column(Float)
    capacity_ch_cv: Mapped[float | None] = mapped_column(Float)
    capacity_ch_total: Mapped[float | None] = mapped_column(Float)
    capacity_dch_cc: Mapped[float | None] = mapped_column(Float)
    capacity_dch_cv: Mapped[float | None] = mapped_column(Float)
    capacity_dch_total: Mapped[float | None] = mapped_column(Float)
    coulombic_efficiency: Mapped[float | None] = mapped_column(Float)
    energy_ch_cc: Mapped[float | None] = mapped_column(Float)
    energy_ch_cv: Mapped[float | None] = mapped_column(Float)
    energy_ch_total: Mapped[float | None] = mapped_column(Float)
    energy_dch_cc: Mapped[float | None] = mapped_column(Float)
    energy_dch_cv: Mapped[float | None] = mapped_column(Float)
    energy_dch_total: Mapped[float | None] = mapped_column(Float)
    energy_efficiency: Mapped[float | None] = mapped_column(Float)
    t_ch_total: Mapped[float | None] = mapped_column(Float)
    t_dch_total: Mapped[float | None] = mapped_column(Float)

    test_data: Mapped[TestData | None] = relationship('TestData', back_populates='kpi')