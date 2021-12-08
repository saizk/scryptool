import time
import datetime
import requests
import urllib.parse


class LunarCrush(object):
    _BASE_URL = 'https://api2.lunarcrush.com/v2'

    def __init__(self, api_key=None):
        self._api_key = api_key

    def _gen_url(self, endpoint, **kwargs):
        url = f'{self._BASE_URL}?data={endpoint}'
        url += f'&key={self._api_key}' if self._api_key else ''
        url += '&' + urllib.parse.urlencode(kwargs) if kwargs else ''
        return url

    def _request(self, endpoint, **kwargs):
        kwargs = self._parse_kwargs(kwargs)
        url = self._gen_url(endpoint, **kwargs)
        return requests.get(url).json()

    @staticmethod
    def _parse_kwargs(kwargs):
        assert kwargs['data_points'] <= 720
        for param, value in kwargs.items():
            if isinstance(value, list):
                kwargs[param] = ','.join(value)
            if isinstance(value, datetime.datetime):
                kwargs[param] = time.mktime(value.timetuple())
        return kwargs

    def get_assets(self, symbol: list, **kwargs) -> dict:
        """
        Details, overall metrics, and time series metrics for one or multiple assets.

        :param list symbol: List of coins to fetch data for
        :key str interval: Provide an interval string value of either "hour" or "day". Defaults to "hour" if omitted.
        :key str time_series_indicators: A comma-separated list of metrics to include in the time series values.
             All available metrics provided if parameter is omitted.
        :key str change: A comma-separated list of change intervals to provide metrics for. 1d, 1w, 1m, 3m, 6m, 1y, 2y.
             Output will include the sum of the selected interval (such as 3 months) the previous sum of
             the time period before and the percent change.
        :key int data_points: Number of time series data points to include for the asset. Maximum of 720 data points
             accepted, to not use time series data set data_points=0
        :key int start (prohibited): A unix timestamp (seconds) of the earliest time series point to provide. Use in combination with
             data_points to start at a certain hour or day and provide X hours/days of data.
        :key int end (prohibited): A unix timestamp (seconds) of the latest time series point to provide. Use in combination with
             data_points to provide the most recent X data points leading up to a certain time.
        """
        return self._request('assets', symbol=symbol, **kwargs)

    def get_market(self, **kwargs) -> dict:
        """
        Summary information for all supported assets (Markets page) including 5 recent time series values for some metrics.

        :param kwargs:
        :key int limit: Limit the number of coins
        :key int page: Specify a page number in combination with the limit parameter. First page starts at 0 so page
             two will be &page=1
        :key str sort: Sort output by: s,n,sc,p,p_btc,v,vt,pc,pch,mc,gs,ss,as,sp,na,md,t,r,yt,sv,u,c,sd,d,acr,cr
        :key bool desc: Reverse the sort. Default is to sort lowest to highest, add &desc=true to sort highest to lowest
        """
        return self._request('market', **kwargs)

    def get_market_pairs(self, symbol: list, **kwargs) -> dict:
        """
        Provides the exchange information for assets and the other assets they are being traded for.

        :param list symbol: List of coins to fetch data for
        :key int limit: Limit the number of rows
        :key int page: Specify a page number in combination with the limit parameter. First page starts at 0
             so page two will be &page=1
        """
        return self._request('market-pairs', symbol=symbol, **kwargs)

    def get_global(self, **kwargs) -> dict:
        """
        Overall aggregated metrics for all supported assets (top of Markets page).

        :key str interval: Provide an interval string value of either "hour" or "day". Defaults to "hour" if omitted.
        :key str change: A comma-separated list of change intervals to provide metrics for. 1d, 1w, 1m, 3m, 6m, 1y, 2y.
             Output will include the sum of the selected interval (such as 3 months) the previous sum of th
             time period before and the percent change
        :key int data_points: Number of time series data points to include for the asset.
        """
        return self._request('global', **kwargs)

    def get_meta(self, **kwargs) -> dict:
        """
        Meta information for all supported assets

        :key str type: The type of meta data to get. Try "counts", "price", or "full"
        """
        return self._request('meta', **kwargs)

    def get_exchange(self, exchange) -> dict:
        """
        Meta information and market pairs for a single exchange that we track

        :key str exchange: Lunar id of the exchange to fetch information for
        """
        return self._request('exchange', exchange=exchange)

    def get_exchanges(self, **kwargs) -> dict:
        """
        Meta information for all exchanges that we track

        :key int limit: Limit the number of results
        :key str order_by: Sort the results by column
        """
        return self._request('exchanges', **kwargs)

    def get_coin_of_the_day(self) -> dict:
        """
        The current coin of the day
        """
        return self._request('coinoftheday')

    def get_coin_of_the_day_info(self) -> dict:
        """
        Provides the history of the coin of the day on LunarCRUSH when it was last changed, and when each coin was
        last coin of the day
        """
        return self._request('coinoftheday_info')

    def get_feeds(self, symbol: list, **kwargs) -> dict:
        """
        Social posts, news, and shared links for one or multiple coins.

        :param list symbol: List of coins to fetch data for
        :key str sources: A comma-separated list of sources to include. Default shows all sources:
             (twitter, reddit, news, urls)
        :key int limit: Number of posts per data source.
        :key int page: Use this for pagination of data.
        :key str type: order/sort/query by 'influential' or 'chronological' posts
        :key int start: A unix timestamp (seconds) of the earliest time series point to provide.
             Use in combination with data_points to start at a certain hour or day and provide X hours/days of data.
        :key int end: A unix timestamp (seconds) of the latest time series point to provide. Use in combination with
             data_points to provide the most recent X data points leading up to a certain time.
        """
        return self._request('feeds', symbol=symbol, **kwargs)

    def get_influencer(self, **kwargs) -> dict:
        """
        Individual influencer details including actual posts.

        :key str id: The id of the twitter account to get details for
        :key str screen_name: The @screen_name of the twitter account to get details for
        :key int days: The number of days of tweets to provide statistics for. Default is 90 days.
        :key int limit: Limit the number of tweets to display
        :key int page: Specify a page number in combination with the limit parameter.
             First page starts at 0 so page two will be &page=1
        """
        return self._request('influencer', **kwargs)

    def get_influencers(self, symbol: list, **kwargs) -> dict:
        """
        List of social accounts that have the most influence on different assets based on number of followers,
        engagements and volume of posts.

        :param list symbol: List of coins to fetch data for
        :key int days: Number of days to aggregate stats for
        :key int num_days: Number of days to aggregate from the calculated date using the days parameter.
             Use the value 1 to get the influencers on a single day.
        :key int limit: Limit number of influencers to return
        :key str order_by: Order by engagement, followers, volume, or influential (influential is a score based on
            engagement, num followers and volume)
        """
        return self._request('influencers', symbol=symbol, **kwargs)
