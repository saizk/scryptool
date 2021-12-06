import san
import csv
import json
import time
import datetime
import pandas as pd

from pprint import pprint
from IPython.display import display
from dataprep.eda import create_report

import dashboards
from scraper._config import *
from scraper.utils import *
from scraper.twitter import Twitter, AsyncTwitter
from scraper.lunarcrush import LunarCrush
from scraper.santiment import Santiment
from scraper.tickers import *


def gen_query(query):
    return ' OR '.join(TICKERS[query])


def twitter_bot():
    bot = scraper.twitter.Twitter(BEARER_TOKEN)

    coin = gen_query('BTC')
    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    # recent_tweets = bot.get_recent_tweets(query=coin, max_results=10)
    # print(recent_tweets)
    recent_tweets_count = bot.get_all_tweets_count(coin, granularity='day', start_time=start)  # 403 Forbidden :(
    # recent_tweets_count = bot.get_recent_tweets_count(coin, granularity='day', start_time=start)
    save_json(recent_tweets_count)
    for tw in recent_tweets_count:
        pprint(tw)


def async_twitter():
    coin = gen_query('ETH')
    # coin = 'ETH'
    end = datetime.datetime(2021, 9, 1, 0, 0, 0)
    start = datetime.datetime(2021, 12, 1, 0, 0, 0)

    async_bot = AsyncTwitter()
    async_bot.search(search=coin, count=None, end_date=start, start_date=end,
                             show_cashtags=True, output='test.db')
    # async_bot.run()
    # async_bot.parallel_run()  # not implemented yet


def lunarcrush_bot():
    bot = LunarCrush('9qjtop453be13yhh6nzmq2j')
    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    end = datetime.datetime(2021, 10, 1, 0, 0, 0)
    info = bot.get_assets(symbol=['ETH'],
                          start=start, end=end, interval='hour')
    data = info['data'][0]
    time_series = data.pop('timeSeries')
    pprint(data)

    df = pd.DataFrame(data)
    display(df)


def santiment_bot():
    sanbot = Santiment(SANTIMENT_API_KEY)
    from_date, to_date = '2021-09-01', '2021-12-01'

    # DASHBOARD 1
    # db1 = dashboards.gen_dashboard_1(
    #     sanbot,
    #     from_date=from_date, to_date=to_date,
    #     interval='1d'
    # )
    # print(f'{san.api_calls_made()[0}[-1 out of {san.api_calls_remaining()}')

    # DASHBOARD 2
    db2 = dashboards.gen_dashboard_2(
        sanbot,
        from_date=from_date, to_date=to_date,
        interval='1d'
    )
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')

    # DASHBOARD 3
    # db3 = dashboards.gen_dashboard_3(
    #     sanbot,
    #     from_date=from_date, to_date=to_date,
    #     interval='1d'
    # )
    # print(f'{san.api_calls_made()[0}[-1 out of {san.api_calls_remaining()}')


def main():
    # twitter_bot()
    # async_twitter()
    # lunarcrush_bot()
    santiment_bot()


if __name__ == '__main__':
    main()
