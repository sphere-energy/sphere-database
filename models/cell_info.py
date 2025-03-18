from sqlalchemy import String, Float, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel
from models.form_factor import FormFactor
from models.customer import Customer
from models.producer import Producer
from models.cell_model import CellModel
from models.battery_chemistry import BatteryChemistry
from models.test_engineer import TestEngineer
from models.anode_chemistry import AnodeChemistry
from models.cathode_chemistry import CathodeChemistry

class CellInfo(BaseModel):
    __tablename__ = 'CELL_INFO'

    form_factor_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('FORM_FACTOR.id'))
    customer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('CUSTOMER.id'))
    cell_producer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('CELL_PRODUCER.id'))
    cell_model_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('CELL_MODEL.id'))
    battery_chemistry_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('BATTERY_CHEMISTRY.id'))
    responsible_person_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_ENGINEER.id'))
    anode_chemistry_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('ANODE_CHEMISTRY.id'))
    cathode_chemistry_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('CATHODE_CHEMISTRY.id'))

    type_id: Mapped[str | None] = mapped_column(String)
    cell_number: Mapped[int | None] = mapped_column(BigInteger)
    serial_number: Mapped[str | None] = mapped_column(String)
    date_received: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    date_released: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    purpose: Mapped[str | None] = mapped_column(String)
    voltage: Mapped[float | None] = mapped_column(Float)
    ac_ir: Mapped[float | None] = mapped_column(Float)
    weight: Mapped[float | None] = mapped_column(Float)
    dimensions: Mapped[str | None] = mapped_column(String)
    additional_tags: Mapped[str | None] = mapped_column(String)
    storage_location: Mapped[int | None] = mapped_column(BigInteger)
    nominal_capacity: Mapped[float | None] = mapped_column(Float)
    charge_max_rated_current: Mapped[float | None] = mapped_column(Float)
    discharge_max_rated_current: Mapped[float | None] = mapped_column(Float)

    # Define relationships if necessary
    # cell_producer: Mapped[Producer | None] = relationship('Producer', back_populates='cell_infos')
    # cell_model: Mapped[CellModel | None] = relationship('CellModel', back_populates='cell_infos')
    # battery_chemistry: Mapped[BatteryChemistry | None] = relationship('BatteryChemistry', back_populates='cell_infos')
    # responsible_person: Mapped[TestEngineer | None] = relationship('TestEngineer', back_populates='cell_infos')
    # battery_anode: Mapped[AnodeChemistry | None] = relationship('AnodeChemistry', back_populates='cell_infos')
    # battery_cathode: Mapped[CathodeChemistry | None] = relationship('CathodeChemistry', back_populates='cell_infos')
    # form_factor: Mapped[FormFactor | None] = relationship('FormFactor', back_populates='cell_infos')
    # customer: Mapped[Customer | None] = relationship('Customer', back_populates='cell_infos')
