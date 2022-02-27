from repository import Repository
from datetime import datetime, date
from typing import List, Generator


class DataFetcher:
    def __init__(self, repository: Repository):
        self._repository = repository

    def get_values(self, fields: List[str], dt_from: datetime, dt_to: datetime) -> Generator:
        if "date_time" not in fields:
            fields.append("date_time")
        raw_data = self._repository.get_values(fields, dt_from, dt_to)
        for item in raw_data:
            yield item['date_time'], self._process_item(item)

    def get_avg_values(self, fields: List[str], dt_from: datetime, dt_to: datetime) -> Generator:
        if "date_time" not in fields:
            fields.append("date_time")
        raw_data = self._repository.get_avg_values(fields, dt_from, dt_to)
        for item in raw_data:
            yield item['date_time'], self._process_item(item)

    def get_sum_values(self, fields: List[str], dt_from: date, dt_to: date) -> Generator:
        if "date_time" not in fields:
            fields.append("date_time")
        raw_data = self._repository.get_sum_values(fields, dt_from, dt_to)
        for item in raw_data:
            yield item['date_time'], self._process_item(item)

    @staticmethod
    def _process_item(item: dict) -> dict:
        del item['date_time']
        return item
