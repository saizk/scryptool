import datetime
import requests
import urllib.parse


class Kraken(object):

    _BASE_URL = 'https://futures.kraken.com/derivatives/api/v4'

    def __init__(self, api_key=None):
        self._api_key = api_key

    @staticmethod
    def _parse_kwargs(kwargs):
        params = {}
        for k, v in kwargs.items():
            if k == 'symbol':
                params[k] = 'PI_' + kwargs['symbol'] + 'USD'
        return params

    def _request(self, endpoint, kwargs):
        url = self._BASE_URL + endpoint
        url += '?' + urllib.parse.urlencode(kwargs) if kwargs else ''
        return requests.get(url).json()

    def get_historical_funding_rate(self, **kwargs):
        start, end = kwargs.get('start'), kwargs.get('end')
        params = self._parse_kwargs(kwargs)
        res = self._request('/historicalfundingrates', params)
        if start and end:
            return self.filter_by_date(res, start, end, kwargs.get('interval'))
        return res

    @staticmethod
    def filter_by_date(data, start, end, interval):
        results = []
        for entry in reversed(data.get('rates')):
            dt = datetime.datetime.strptime(entry['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

            if start <= dt <= end:

                if interval == '1d':
                    if dt.hour == 0:
                        results.append(entry)
                else:
                    results.append(entry)

            if dt < start:
                break

        return results
