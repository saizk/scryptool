import tweepy
from scraper import twint


class Twitter(object):
    BASE_URL = "https://twitter.com"

    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        self.config = twint.Config()  # for asynchronous Twitter scraping (no api key)

    @staticmethod
    def _pagination(method, query, max_results, *args, **kwargs):
        return tweepy.Paginator(method, query=query, max_results=max_results, *args, **kwargs).flatten()

    def get_users_by_name(self, user: str, count: int = 5):
        return self.client.get_user(username=user, count=count)

    def get_followers(self, user: str, count: int = 100, **kwargs):
        return self.client.get_users_followers(screen_name=user, count=count, **kwargs)

    def get_recent_tweets(self, query: str = 'BTC', *args, **kwargs) -> list[tweepy.Tweet]:
        return [tweet for tweet in
                self._pagination(self.client.search_recent_tweets, query=query, *args, **kwargs)]

    def get_all_tweets(self, query: str = 'BTC', *args, **kwargs) -> list[tweepy.Tweet]:
        return [tweet for tweet in
                self._pagination(self.client.search_all_tweets,    query=query, *args, **kwargs)]

    def async_get_all_tweets(self, **kwargs):
        output = kwargs.get('file')
        if output.endswith('.csv'):
            self.config.Store_csv = True
        elif output.endswith('.db'):
            self.config.Database = output
        elif output.endswith('.json'):
            self.config.Store_json = True

        self.config.Output = output
        self.config.Query = kwargs.get('query')
        self.config.Limit = kwargs.get('limit')
        twint.run.Search(self.config)

    def get_all_tweets_count(self, query: str = 'BTC',
                             granularity: str = 'hour', **kwargs) -> tweepy.client.Response:
        return self.client.get_all_tweets_count(query=query, granularity=granularity, **kwargs)

    def get_recent_tweets_count(self, query: str = 'BTC',
                                granularity: str = 'hour', **kwargs) -> tweepy.client.Response:
        return self.client.get_recent_tweets_count(query=query, granularity=granularity, **kwargs)
