from sqlalchemy import String, Float, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.base_model import BaseModel
from models.cell_info import CellInfo
from models.test_procedures import TestProcedures
from models.test_status import TestStatus
from models.cycler_info import CyclerInfo

class TestMetadata(BaseModel):
    __tablename__ = 'TEST_METADATA'

    test_procedure_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_PROCEDURE.id'))
    test_status_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('TEST_STATUS.id'))
    cycler_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('CYCLER_INFO.id'))
    cell_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey('CELL_INFO.id'))
    
    test_name: Mapped[str | None] = mapped_column(String)
    test_id: Mapped[BigInteger | None] = mapped_column(BigInteger)
    schedule_name: Mapped[str | None] = mapped_column(String)
    timezone: Mapped[str | None] = mapped_column(String)
    tests_start: Mapped[DateTime | None] = mapped_column(DateTime)
    temperature: Mapped[float | None] = mapped_column(Float)
    test_finish: Mapped[DateTime | None] = mapped_column(DateTime)
    
    # test_procedure: Mapped[TestProcedures | None] = relationship('TestProcedures', back_populates='test_metadata')
    # test_status: Mapped[TestStatus | None] = relationship('TestStatus', back_populates='test_metadata')
    # cycler_info: Mapped[CyclerInfo | None] = relationship('CyclerInfo', back_populates='test_metadata')
    # cell_info: Mapped[CellInfo | None] = relationship('CellInfo', back_populates='test_metadata')


