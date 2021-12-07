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

    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    @staticmethod
    def _parse_kwargs(kwargs):
        for param, value in kwargs.items():
            if isinstance(value, datetime.datetime):
                kwargs[param] = value.strftime("%Y-%m-%dT%H:%M:%SZ")

        return kwargs

    @staticmethod
    def _pagination(method, *args, **kwargs):
        return tweepy.Paginator(method, *args, **kwargs).flatten()

    def get_user(self, *args, **kwargs):
        return self.client.get_user(*args, **self._parse_kwargs(kwargs))

    def get_all_tweets(self, query: str, *args, **kwargs) -> List[tweepy.Tweet]:
        return [*self._pagination(self.client.search_all_tweets,    query=query, *args, **self._parse_kwargs(kwargs))]

    def get_recent_tweets(self, query: str, *args, **kwargs) -> List[tweepy.Tweet]:
        return [*self._pagination(self.client.search_recent_tweets, query=query, *args, **self._parse_kwargs(kwargs))]

    def get_all_tweets_count(self, query: str, granularity: str, **kwargs) -> tweepy.client.Response:
        return self.client.get_all_tweets_count(query=query, granularity=granularity, **self._parse_kwargs(kwargs))

    def get_recent_tweets_count(self, query: str, granularity: str, **kwargs) -> tweepy.client.Response:
        return self.client.get_recent_tweets_count(query=query, granularity=granularity, **self._parse_kwargs(kwargs))


class AsyncTwitter(object):

    def __init__(self):
        self.config = twint.Config()  # for asynchronous Twitter scraping (no api key)

    @staticmethod
    def _parse_kwargs(kwargs):
        params = {}
        for k, v in kwargs.items():
            if isinstance(v, datetime.datetime):
                v = v.strftime("%Y-%m-%d %H:%M:%S")
            if k == 'start_date':
                params['until'] = v
                continue
            if k == 'end_date':
                params['since'] = v
                continue
            else:
                params[k] = v

        return params

    def search(self, **kwargs):
        kwargs = self._parse_kwargs(kwargs)

        for k, v in kwargs.items():
            setattr(self.config, k.capitalize(), v)

        output = kwargs.get('output')

        if output.endswith('.csv'):
            self.config.Store_csv = True
        elif output.endswith('.db'):
            self.config.Database = output
        elif output.endswith('.json'):
            self.config.Store_json = True

        if not kwargs.get('coins'):
            self.config.Coins = list(TICKERS)

    def _parallel_config(self) -> list:
        """
        Creates a list of N twint.Config objects with each respective coin queries
        :return:
        """
        # self.search(**kwargs)
        base_cfg = self.config
        path = Path(self.config.Output)
        config_params = [] * len(base_cfg.Queries)

        for coin, query in zip(base_cfg.Coins, base_cfg.Queries):
            config = copy.deepcopy(base_cfg)
            config.Search = query

            parents, file = path.parent, path.name
            parents.mkdir(parents=True, exist_ok=True)

            config.Output = rf'{parents}\{coin.lower()}_{file}'

            config_params.append(config)

        return config_params

    def parallel_run(self, n_workers=mp.cpu_count()):

        config_params = self._parallel_config()

        with ProcessPoolExecutor(max_workers=n_workers) as pool:
            results = pool.map(twint.run.Search, config_params)

    def run(self):
        twint.run.Search(self.config)
