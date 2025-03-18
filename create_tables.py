from sqlalchemy import create_engine
from models.base_model import BaseModel
from models.anode_chemistry import AnodeChemistry
from models.battery_chemistry import BatteryChemistry
from models.cathode_chemistry import CathodeChemistry
from models.cell_info import CellInfo
from models.cell_model import CellModel
from models.customer import Customer
from models.cycler_info import CyclerInfo
from models.data_error import DataError
from models.form_factor import FormFactor
from models.kpi import KPI
from models.producer import Producer
from models.test_data import TestData
from models.test_engineer import TestEngineer
from models.test_metadata import TestMetadata
from models.test_procedures import TestProcedures
from models.test_status import TestStatus
from models.widget import Widget
from models.widget_type import WidgetType
from models.workspace import Workspace

URL = "postgresql://postgres:dotcep-demjak-qosmI6@database-sphere.chvqqqs41kgo.eu-central-1.rds.amazonaws.com/sphere"

engine = create_engine(URL, echo=True)

# BaseModel.metadata.drop_all(engine)
BaseModel.metadata.create_all(engine)
