import sqlite3
import json
import datetime
import logging
import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from models.test_status import TestStatus
from models.test_metadata import TestMetadata
from models.cycler_info import CyclerInfo
from models.cell_info import CellInfo
from models.test_procedures import TestProcedures
from pandasql import sqldf

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)


class IngestRawData:
    def __init__(self, file):
        URL = "postgresql://postgres:dotcep-demjak-qosmI6@database-sphere.chvqqqs41kgo.eu-central-1.rds.amazonaws.com/sphere"
        self.engine = create_engine(URL)
        self.session = Session(self.engine)
        self.conn = sqlite3.connect('Cell_inventory.db')
        self.file = file
        self.header_lines = []
        self.header_info = {}

    def _create_dataframe(self):
        with open(self.file, 'r') as f:
            for i, line in enumerate(f):
                stripped = line.strip()
                if "Data Field:" in line:
                    skiprows = i + 1
                    break
                self.header_lines.append(stripped)
                if ':' in stripped:
                    key, value = stripped.split(":", 1)
                    self.header_info[key.strip()] = value.strip()

        data = pd.read_csv(self.file, skiprows=skiprows, sep='\t')

        return data
    
    def _get_file_header(self):
        rename_dict = {
            "Serial Number": "serial_number",
            "Cycler Name": "cycler",
            "Test Name": "test_name",
            "Channel Id": "channel",
            "Schedule Name": "schedule_name",
            "Timezone": "timezone",
            "Test ID": "test_id"
        }

        self.df_header_info = (
            pd.DataFrame(self.header_info, index=[0])
            .drop(columns=['File Format Type', 'Header Lines', 'Data Type Flag'])
            .rename(columns=rename_dict)
        )

        self.df_header_info['tests_start'] = self.file.split('_')[1].split('/')[-1]
        logging.info(f"Start Time: {self.df_header_info['tests_start'][0]}")

    def _execute_sqlite_query(self, query):
        try:
            query_result = pd.read_sql_query(query, self.conn)

        except Exception as e:
            logging.info(f"An error occurred: {str(e)}")
            raise

        return query_result
    
    def _execute_postgres_query(self, query):
        try:
            query_result = pd.read_sql_query(query, self.engine)
        except Exception as e:
            logging.info(f"An error occurred: {str(e)}")
            raise

        return query_result

    def _timestamp_to_datetime(self, timestamp):
        """
        Convert Arbin timestamp to datetime. If the timestamp is NaN, returns None.
        """
        try:
            date = datetime.datetime.fromtimestamp(timestamp / 10000000.0) #Arbin timestamp in unit 10^-7 seconds
        except ValueError as e:
            if str(e)=="Invalid value NaN (not a number)":
                date = None
            else:
                raise Exception(f"ValueError: {str(e)}")
        except Exception as e2:
            logging.info(f"An error occurred: {str(e2)}")
            raise

        return date
    
    def _get_test_key(self, cycler):
        if self.df_header_info['serial_number'][0] == "229383-A" and int(self.df_header_info['tests_start'][0]) > 1734429154:
                test_key = f"A1-1_{self.df_header_info['channel'][0]}_{self.df_header_info['test_id'][0]}"
        else:
            test_key = f"{cycler.short_name}_{self.df_header_info['channel'][0]}_{self.df_header_info['test_id'][0]}" 

        return test_key
    
    def _check_test_status_exists(self, channel, chamber):
        test_status = select(TestStatus.id).where(TestStatus.channel == channel).where(TestStatus.chamber == chamber)
        test_status = self.session.execute(test_status).one_or_none()

        return test_status

    def _mount_test_status(self):
        success = True
        df_test_status = self.df_header_info.copy()

        cycler = select(CyclerInfo).where(CyclerInfo.serial_number == self.df_header_info['serial_number'][0])
        cycler = self.session.execute(cycler).first()[0]

        test_key = self._get_test_key(cycler)

        logging.info(f"Test Key: {test_key}")


        query = f"SELECT chamber FROM table_tests WHERE test_key='{test_key}'"
        chamber = self._execute_sqlite_query(query)

        # logging.info(f"Chamber: {chamber['chamber'][0]}")

        if chamber is None or chamber.empty:
            success = False
            logging.warning(f"Chamber not found for test {self.df_header_info['test_name'][0]} and channel {self.df_header_info['channel'][0]}")
            logging.warning("Setting chamber to 42")
            chamber = pd.DataFrame({'chamber': [42]})

        df_test_status = pd.concat([df_test_status, chamber], axis=1)

        test_status_id = self._check_test_status_exists(int(df_test_status['channel'][0]), chamber=int(df_test_status['chamber'][0]))

        if test_status_id is None:
            logging.info(f"Test {self.df_header_info['test_name'][0]} not ingested yet.")
            test_status_tb = TestStatus(channel=int(df_test_status['channel'][0]), chamber=int(df_test_status['chamber'][0]), status='Finished')
        
            self.session.add(test_status_tb)
            self.session.commit()

            return test_status_tb.id, cycler, success
        
        logging.info(f"Test:{self.df_header_info['test_name'][0]} has status key {test_status_id[0]}")

        return test_status_id[0], cycler, success
    
    def _check_metadata_exists(self, test_key):
        test_metadata = select(TestMetadata.id).join(TestStatus).where(TestMetadata.test_status_id == TestStatus.id).where(TestStatus.channel == self.df_header_info['channel'][0]).where(TestMetadata.test_id == self.df_header_info['test_id'][0])
        test_metadata = self.session.execute(test_metadata).one_or_none()

        return test_metadata

    def _mount_test_metadata(self, test_status_id, cycler):
        success = True
        test_key = self._get_test_key(cycler)

        test_metadata_id = self._check_metadata_exists(test_key)

        if test_metadata_id is not None:
            logging.info(f"Test {self.df_header_info['test_name'][0]} already ingested.")
            logging.info(f"Test Metadata id: {test_metadata_id[0]}")

            return test_metadata_id[0], success

        query = f"SELECT procedure, sample_id, temperature FROM table_tests WHERE test_key='{test_key}'"
        cell_sample = self._execute_sqlite_query(query)

        if not cell_sample.empty:
            cell_number = cell_sample['sample_id'][0].split('_')[-1]
            type_id = '_'.join(cell_sample['sample_id'][0].split('_')[:-1])

            cell_id = select(CellInfo).where(CellInfo.type_id == type_id and CellInfo.cell_number == cell_number)
            cell_id = self.session.execute(cell_id).first()

            if cell_id is None:
                success = False
                logging.warning(f"Cell not found for type_id {type_id} and cell number {cell_number}")

            test_procedure_id = select(TestProcedures).where(TestProcedures.name == cell_sample['procedure'][0])
            test_procedure_id = self.session.execute(test_procedure_id).first()

            test_metadata = TestMetadata(cycler_id=int(cycler.id),cell_id=int(cell_id[0].id), test_procedure_id=1, 
                                test_status_id=test_status_id, schedule_name=self.df_header_info['schedule_name'][0], 
                                timezone=self.df_header_info['timezone'][0], test_name=self.df_header_info['test_name'][0], 
                                temperature=cell_sample['temperature'][0], test_id=self.df_header_info['test_id'][0])

            self.session.add(test_metadata)
            self.session.commit()

            return test_metadata.id, success
        
        success = False
        logging.warning(f"Cell sample not found for test {self.df_header_info['test_name'][0]}, channel {self.df_header_info['channel'][0]} and cycler {cycler.short_name}")
        logging.warning(f"test_key: {test_key}")

        test_metadata = TestMetadata(cycler_id=int(cycler.id),cell_id=None, test_procedure_id=1, 
                                test_status_id=test_status_id, schedule_name=self.df_header_info['schedule_name'][0], 
                                timezone=self.df_header_info['timezone'][0], test_name=self.df_header_info['test_name'][0], 
                                temperature=None, test_id=self.df_header_info['test_id'][0])

        self.session.add(test_metadata)
        self.session.commit()

        return test_metadata.id, success


    def _mount_test_data(self, test_metadata_id, data):
        header_name = list(data.keys())
        header_name[:16]

        df_original = data.groupby('Data Point').first().reset_index()

        df_original.drop(columns=['Byte Index', 'Line Number', 'Data Type Flag'], inplace=True)
        df_original.drop(df_original.tail(1).index, inplace=True)



        for col in ["Data Point", "Cycle Index", "Step Index"]:
            df_original = df_original[df_original[col] != ' ']
            df_original[col] = [int(point) if not pd.isna(point) else point for point in df_original[col]]

        for col in df_original.columns:
            if col=='' or 'Unnamed' in col:
                df_original.drop(col, axis=1, inplace=True)

        df_original["Data Time"] = df_original["Data Time"].astype(float)
        df_original["Data Time"] = df_original["Data Time"].apply(self._timestamp_to_datetime)

        rename_dict = {
            'Data Point': 'data_point',
            'Test Time' : 'test_time',
            'Step Time' : 'step_time',
            'Cycle Index' : 'cycle_index',
            'Step Index' : 'step_index',
            'Current' : 'current',
            'Voltage' : 'voltage',
            'Charge Capacity' : 'charge_capacity',
            'Discharge Capacity' : 'discharge_capacity',
            'Charge Energy' : 'charge_energy',
            'Discharge Energy' : 'discharge_energy',
            'Data Flags' : 'data_flags',
            'Data Time': 'data_time',
            'Other Information': 'additional_data'
        }

        df_original.rename(columns=rename_dict, inplace=True)
        df_original['test_metadata_id'] = test_metadata_id if test_metadata_id != -1 else None

        df_original.to_sql('TEST_DATA', self.engine, if_exists='append', index=False)

    def ingest_csv(self):
        logging.info(f"Ingesting file {self.file}...")
        
        self.header_lines = []
        self.header_info = {}

        data = self._create_dataframe()
        self._get_file_header()
        
        test_status_id, cycler, success_status = self._mount_test_status()

        test_metadata_id, sucess_metadata = self._mount_test_metadata(test_status_id, cycler)

        self._mount_test_data(test_metadata_id, data)

        self.session.close()
        self.conn.close()
        logging.info("Data ingestion completed.")

        return success_status, sucess_metadata