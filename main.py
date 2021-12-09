import san
import csv
import json
import time
import datetime
import pandas as pd
import pickle

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
    bot = Twitter(BEARER_TOKEN)

    coin = gen_query('BTC')
    end = datetime.datetime(2021, 12, 3, 0, 0, 0)
    start = datetime.datetime(2021, 12, 8, 0, 0, 0)
    # recent_tweets = bot.get_recent_tweets(
    #     query=coin, lang='en',
    #     start_time=start, end_time=end
    # )
    # print(recent_tweets)
    # all_tweets_count = bot.get_all_tweets_count(
    # query=coin, granularity='day', start_time=start
    # )  # 403 Forbidden :(
    recent_tweets_count = bot.get_recent_tweets_count(
        query=gen_query('coin'),
        granularity='hour', lang='en',
        start_time=start, end_time=end
    )
    # save_json(recent_tweets_count, 'btc_test.json')
    for tw in recent_tweets_count:
        pprint(tw)


def async_twitter():
    end = datetime.datetime(2021, 12, 3, 0, 0, 0)
    start = datetime.datetime(2021, 12, 8, 0, 0, 0)

    async_bot = AsyncTwitter()

    queries = list(map(gen_query, TICKERS))
    coins = list(TICKERS)

    async_bot.search(search=gen_query('BTC'), lang='en',
                     end_date=end, start_date=start,
                     show_cashtags=True, output='btc_test.csv')
    async_bot.run()

    # async_bot.search(queries=queries, coins=coins, lang='en',
    #                  end_date=end, start_date=start, lowercase=True,
    #                  show_cashtags=True, output=f'data/twitter/tweets.csv')
    #
    # async_bot.parallel_run()


def lunarcrush_bot():
    bot = LunarCrush()

    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    end = datetime.datetime(2021, 12, 1, 0, 0, 0)

    data_points = (datetime.datetime.today() - start).days + 1

    lcmetrics = bot.get_assets(
        symbol=list(TICKERS), data_points=data_points,
        interval='day', change='6m'
    )
    df = dashboards.gen_dashboard_2_lunarcrush(lcmetrics, end)
    df.to_csv('data/dashboard2/lunarcrush_data2.csv')

    display(df)


def santiment_bot():
    sanbot = Santiment(SANTIMENT_API_KEY)

    #DASHBOARD 1
    print(dashboards.gen_dashboard_1(sanbot, 1))
    #print(dashboards.gen_dashboard_1(sanbot, 2))

    """
    platforms = ['twitter', 'reddit', 'telegram', 'bitcointalk']

    # DASHBOARD 2
    db2 = dashboards.gen_dashboard_2_santiment(
        sanbot, platforms, TICKERS, save_all=False,
        from_date='2021-09-01', to_date='2021-12-01',
        interval='1d'
    )
    db2.to_csv(f'data/dashboard2/santiment_data.csv')
    display(db2)
    """
    #dashboards.gen_dashboard_3(sanbot)
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')


def main():
    # twitter_bot()
    # async_twitter()
    #lunarcrush_bot()
    santiment_bot()


if __name__ == '__main__':
    main()
