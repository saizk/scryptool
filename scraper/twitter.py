import copy
import datetime
import tweepy
import multiprocessing as mp

from pathlib import Path
from typing import List
from concurrent.futures import ProcessPoolExecutor

from scraper import twint
from scraper.tickers import TICKERS


class Twitter(object):

    def __init__(self, bearer_token, wait_on_rate_limit=True):
        self.client = tweepy.Client(bearer_token=bearer_token,
                                    wait_on_rate_limit=wait_on_rate_limit)

    @staticmethod
    def _parse_kwargs(kwargs) -> dict:
        assert 'query' in kwargs
        params, query_params = {}, ''

        for key, value in kwargs.items():
            if isinstance(value, datetime.datetime):
                params[key] = value.strftime("%Y-%m-%dT%H:%M:%SZ")
            elif key == 'user':
                query_params += f' from:{value}'
            elif key == 'lang':
                query_params += f' lang:{value}'
            else:
                params[key] = value

        params['query'] = f'({params["query"]}){query_params}'
        return params

    @staticmethod
    def _pagination(method, **kwargs):
        return tweepy.Paginator(method, **kwargs).flatten()

    def get_user(self, **kwargs):
        return self.client.get_user(**self._parse_kwargs(kwargs))

    def get_all_tweets(self, **kwargs) -> List[tweepy.Tweet]:
        return [*self._pagination(self.client.search_all_tweets, **self._parse_kwargs(kwargs))]

    def get_recent_tweets(self, **kwargs) -> List[tweepy.Tweet]:
        return [*self._pagination(self.client.search_recent_tweets, **self._parse_kwargs(kwargs))]

    def get_all_tweets_count(self, **kwargs) -> tweepy.client.Response:
        return self.client.get_all_tweets_count(**self._parse_kwargs(kwargs))  # 403 Forbidden :(

    def get_recent_tweets_count(self, **kwargs) -> tweepy.client.Response:
        return self.client.get_recent_tweets_count(**self._parse_kwargs(kwargs))


class AsyncTwitter(object):

    def __init__(self):
        self.config = twint.Config()  # for asynchronous Twitter scraping (no api key)

    @staticmethod
    def _parse_kwargs(kwargs):
        params, query_params = {}, ''
        for key, value in kwargs.items():
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            if key == 'start_date':
                params['since'] = value
            elif key == 'end_date':
                params['until'] = value
            elif key == 'user':
                query_params += f' from:{value}'
            else:
                params[key] = value
        if params.get('search'):
            params['search'] = f'({params["search"]}){query_params}'
        return params

    @staticmethod
    def gen_query(query: list):
        return ' OR '.join(query)

    @staticmethod
    def _from_snake_to_camel(snake_str):  # PEP8 :(
        init, *temp = snake_str.split('_')
        camel_str = ''.join([init.title(), *map(str.title, temp)])
        return camel_str

    def search(self, **kwargs):
        kwargs = self._parse_kwargs(kwargs)

        for k, v in kwargs.items():
            setattr(self.config, self._from_snake_to_camel(k), v)

        output = kwargs.get('output')

        if output.endswith('.csv'):
            self.config.Store_csv = True
        elif output.endswith('.db'):
            self.config.Database = output
        elif output.endswith('.json'):
            self.config.Store_json = True

    def _parallel_config(self) -> list:
        """
        Creates a list of N twint.Config objects with each respective coin queries
        :return:
        """
        path = Path(self.config.Output)
        path.parent.mkdir(parents=True, exist_ok=True)

        if self.config.Users is not None:
            config_params = self._users_config(path)
        else:
            config_params = self._coin_config(path)

        return config_params

    def _coin_config(self, path):
        config_params = []

        for coin, query in self.config.Tickers.items():
            config = copy.deepcopy(self.config)

            config.Search = self.gen_query(query)
            config.Output = rf'{path.parent}\{coin.lower()}_{path.name}'
            config_params.append(config)

        return config_params

    def _users_config(self, path):
        config_params = []

        for coin, users in self.config.Users.items():
            for user in users:
                config = copy.deepcopy(self.config)

                config.Search = f'({self.gen_query(self.config.Tickers[coin])}) from:{user}'
                config.Output = rf'{path.parent}\{coin}_{user.lower()}_{path.name}'
                config_params.append(config)

        return config_params

    def parallel_run(self, n_workers: int = mp.cpu_count()):
        config_params = self._parallel_config()

        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            results = pool.map(twint.run.Search, config_params)

    def run(self):
        self.config.Tickers = None
        twint.run.Search(self.config)
