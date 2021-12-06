import datetime
import tweepy
import multiprocessing as mp

from typing import List
from concurrent.futures import ProcessPoolExecutor

from scraper import twint


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
            if k == 'end_date':
                params['since'] = v
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

    def _parallel_config(self, interval: int) -> list:
        """
        Creates a list of N twint.Config objects with each respective datetime configurations, where N
        is the number of cores in the CPU.
        :param interval:
        :return:
        """
        config_params = [self.config] * interval
        until = self.config.Until or datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        start = datetime.datetime.strptime(until, "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(self.config.Since, "%Y-%m-%d %H:%M:%S")

        diff = (end - start) / interval

        for i in range(interval):
            end = (start + diff * (i + 1))
            config_params[i].Since = start.strftime("%Y-%m-%d %H:%M:%S")  # noqa
            config_params[i].Until = end.strftime("%Y-%m-%d %H:%M:%S")  # noqa
            start = end

        return config_params

    def parallel_run(self):
        workers = mp.cpu_count()
        config_params = self._parallel_config(workers)
        for i in range(workers):
            with ProcessPoolExecutor(max_workers=workers) as pool:
                results = pool.submit(twint.run.Search, config_params[i])

    def run(self):
        twint.run.Search(self.config)
