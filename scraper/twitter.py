import tweepy
from typing import List

from scraper import twint


class Twitter(object):

    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    @staticmethod
    def _pagination(method, *args, **kwargs):
        return tweepy.Paginator(method, *args, **kwargs).flatten()

    def get_user(self, *args, **kwargs):
        return self.client.get_user(*args, **kwargs)

    def get_all_tweets(self, query: str, *args, **kwargs) -> List[tweepy.Tweet]:
        return [*self._pagination(self.client.search_all_tweets,    query=query, *args, **kwargs)]

    def get_recent_tweets(self, query: str, *args, **kwargs) -> List[tweepy.Tweet]:
        return [*self._pagination(self.client.search_recent_tweets, query=query, *args, **kwargs)]

    def get_all_tweets_count(self, query: str, granularity: str, **kwargs) -> tweepy.client.Response:
        return self.client.get_all_tweets_count(query=query, granularity=granularity, **kwargs)

    def get_recent_tweets_count(self, query: str, granularity: str, **kwargs) -> tweepy.client.Response:
        return self.client.get_recent_tweets_count(query=query, granularity=granularity, **kwargs)


class AsyncTwitter(object):

    def __init__(self):
        self.config = twint.Config()  # for asynchronous Twitter scraping (no api key)

    def get_all_tweets(self, **kwargs):

        for k, v in kwargs.items():
            setattr(self.config, k.capitalize(), v)

        output = kwargs.get('output')

        if output.endswith('.csv'):
            self.config.Store_csv = True
        elif output.endswith('.db'):
            self.config.Database = output
        elif output.endswith('.json'):
            self.config.Store_json = True

        self.run()

    def run(self):
        twint.run.Search(self.config)
