import time
import datetime
import requests


class GlassNode(object):

    _BASE_URL = 'https://api.glassnode.com/v1'

    def __init__(self, api_key):
        self._api_key = api_key

    @staticmethod
    def _parse_kwargs(kwargs):
        params = {}

        for key, value in kwargs.items():
            if isinstance(value, datetime.datetime):
                value = int(time.mktime(value.timetuple()))
            if key == 'asset':
                params['a'] = value.upper()
            elif key == 'interval':
                params['i'] = value
            elif key == 'format':
                params['f'] = value.upper()
            elif key == 'start':
                params['s'] = value
            elif key == 'end':
                params['u'] = value
            else:
                params[key] = value

        params['c'] = 'native'
        return params

    def _request(self, endpoint, **kwargs):
        url = self._BASE_URL + endpoint
        params = self._parse_kwargs(kwargs)
        params['api_key'] = self._api_key
        res = requests.get(url, params=kwargs)
        return res

    def get_active_addresses(self, **kwargs):
        return self._request('/metrics/addresses/active_count', **kwargs)
