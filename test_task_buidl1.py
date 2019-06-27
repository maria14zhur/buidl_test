"""Test1 for 'coinmarketcap.com' API"""
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime
import sys


class ApiTest1:
    def __init__(self, max_ans_time_ms=500, max_pack_size_kb=10):
        self.max_ans_time_ms = max_ans_time_ms
        self.max_pack_size_kb = max_pack_size_kb

    @staticmethod
    def __is_valid_date(data):
        """Check that data was updated today"""
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")
        for i in data['data']:
            if i['last_updated'].split('T')[0] != now:
                raise ValueError('Data is outdated')
        return True

    def __is_valid_pack_size(self, data):
        """Check that size of package is less than  max_pack_size"""
        size_kb = sys.getsizeof(data) / 1024
        if size_kb > self.max_pack_size_kb:
            raise ValueError(f'Package size: {size_kb} > {self.max_pack_size_kb} kb')
        return size_kb

    def __is_valid_time(self, ans_time):
        """Check that server answer time is less than max_ans_time"""
        ans_time_ms = ans_time * 1000
        if ans_time_ms > self.max_ans_time_ms:
            raise ValueError(f'Answer time {ans_time_ms} > {self.max_ans_time_ms} ms')
        return ans_time_ms

    def api_request(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': '10',
            'convert': 'USD',
            'sort': 'volume_24h'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '1f059835-c00f-44aa-9f62-ed6e701434cb',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = dict(json.loads(response.text))
            return {'time_ms': self.__is_valid_time(response.elapsed.total_seconds()), 'size_kb': self.__is_valid_pack_size(response), 'last-updated': self.__is_valid_date(data)}

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


if __name__ == '__main__':
    request = ApiTest1()
    request.api_request()
    print('Test №1 passed')



