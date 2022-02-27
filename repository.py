import abc
import os
import sqlite3

from abc import ABC
from datetime import date, datetime
from typing import List, Dict, Generator
from csv import DictReader
from utils import convert_datetime


class Repository(ABC):

    @abc.abstractmethod
    def init_db(self):
        ...

    @abc.abstractmethod
    def get_daily_avg(self, fields: List[str], d_from: date, d_to: date) -> Dict[date, float]:
        ...

    @abc.abstractmethod
    def get_values(self, fields: List[str], dt_from: datetime, dt_to: datetime) -> Generator:
        ...

    @abc.abstractmethod
    def get_avg_values(self, fields: List[str], dt_from: date, dt_to: date) -> Generator:
        ...

    @abc.abstractmethod
    def get_sum_values(self, fields: List[str], dt_from: date, dt_to: date) -> Generator:
        ...

    @abc.abstractmethod
    def add_row(self, row: dict):
        ...

    @abc.abstractmethod
    def commit(self):
        ...

    def import_csv(self, csv_path: str):
        self.init_db()
        with open(csv_path, "r") as fp:
            line_number = 1
            reader = DictReader(fp)
            for row in reader:
                try:
                    self.add_row(Repository._process_csv_row(row))
                except Exception as e:
                    print(f"Error with row {line_number}:", str(e))
                line_number += 1
            self.commit()

    @staticmethod
    def _process_csv_row(csv_row: dict) -> dict:
        for value in csv_row.values():
            if value == '':
                raise Exception(f"invalid row {csv_row}")

        return {
            'date_time': convert_datetime(csv_row['Date']),
            'energy': csv_row['Energy (kWh)'],
            'reactive_energy': csv_row['Reactive energy (kVArh)'],
            'power': csv_row['Power (kW)'],
            'maximeter': csv_row['Maximeter (kW)'],
            'reactive_power': csv_row['Reactive power (kVAr)'],
            'voltage': csv_row['Voltage (V)'],
            'intensity': csv_row['Intensity (A)'],
            'power_factor': csv_row['Power factor (φ)'],
        }


class SqlLite3Repository(Repository):
    DB_FILE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/data/appdata.db'

    def __init__(self):
        self._connection = None

    def _get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(SqlLite3Repository.DB_FILE_PATH)
        return self._connection

    def _get_cursor(self):
        return self._get_connection().cursor()

    def _run_query(self, sql):
        result = self._get_cursor().execute(sql)
        return result

    def add_row(self, row: dict):
        sql = f'''INSERT INTO monitoring_report(
        date_time, energy, reactive_energy, power, maximeter,reactive_power, voltage, intensity, power_factor) VALUES 
        (\'{row['date_time']}\', {row['energy']}, {row['reactive_energy']}, {row['power']}, {row['maximeter']}, 
        {row['reactive_power']}, {row['voltage']}, {row['intensity']}, {row['power_factor']})
        '''
        #print(sql)
        self._run_query(sql)

    def commit(self):
        self._get_connection().commit()
        self._get_connection().close()
        self._connection = None

    def init_db(self):
        basedir = os.path.dirname(SqlLite3Repository.DB_FILE_PATH)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        with open(SqlLite3Repository.DB_FILE_PATH, 'a'):
            os.utime(SqlLite3Repository.DB_FILE_PATH, None)

        #Date,Energy (kWh),Reactive energy (kVArh),Power (kW),Maximeter (kW),Reactive power (kVAr),Voltage (V),Intensity (A),Power factor (φ)
        self._run_query("DROP TABLE IF EXISTS monitoring_report")

        sql = '''CREATE TABLE monitoring_report (
        date_time DATETIME, 
        energy FLOAT, 
        reactive_energy FLOAT, 
        power FLOAT, 
        maximeter FLOAT,
        reactive_power FLOAT, 
        voltage FLOAT, 
        intensity FLOAT, 
        power_factor FLOAT) 
        '''

        self._run_query(sql)
        self.commit()

    def get_daily_avg(self, fields: List[str], d_from: date, d_to: date) -> Dict[date, float]:
        pass

    def get_values(self, fields: List[str], dt_from: datetime, dt_to: datetime) -> Generator:
        columns = ",".join(fields)
        sql = f'''SELECT {columns} from monitoring_report WHERE date_time BETWEEN '{dt_from}' AND '{dt_to}' 
        ORDER BY date_time'''
        return (dict(zip(fields, row)) for row in self._run_query(sql))

    def get_avg_values(self, fields: List[str], dt_from: datetime, dt_to: datetime) -> Generator:
        columns = [f"AVG({x}) as {x}" for x in fields if x != "date_time"]
        columns.append("DATE(date_time) AS date")
        columns_sql = ",".join(columns)

        sql = f'''SELECT {columns_sql} from monitoring_report WHERE DATE (date_time) BETWEEN '{dt_from}' AND '{dt_to}' 
        GROUP BY date ORDER BY date'''
        return (dict(zip(fields, row)) for row in self._run_query(sql))

    def get_sum_values(self, fields: List[str], dt_from: datetime, dt_to: datetime) -> Generator:
        columns = [f"SUM({x}) as {x}" for x in fields if x != "date_time"]
        columns.append("DATE(date_time) AS date")
        columns_sql = ",".join(columns)

        sql = f'''SELECT {columns_sql} from monitoring_report WHERE DATE (date_time) BETWEEN '{dt_from}' AND '{dt_to}' 
        GROUP BY date ORDER BY date'''
        return (dict(zip(fields, row)) for row in self._run_query(sql))


def create_repository():
    return SqlLite3Repository()
