import unittest
from unittest.mock import Mock
from repository import create_repository
from data_fetcher import DataFetcher
from datetime import datetime


class TestDataFetcher(unittest.TestCase):

    def test_repository_called_once(self):
        repository_mock = create_repository()
        repository_mock.get_values = Mock(return_value=[])

        sut = DataFetcher(repository_mock)
        dt_from = datetime.strptime("2018-02-04 00:30:00", "%Y-%m-%d %H:%M:%S")
        dt_to = datetime.strptime("2018-03-04 01:30:00", "%Y-%m-%d %H:%M:%S")
        sut.get_values(['power'], dt_from, dt_to)
        self.assertEqual(repository_mock.get_values.call_count, 1)
        repository_mock.get_values.assert_called_once_with(['power', 'date_time'], dt_from, dt_to)
