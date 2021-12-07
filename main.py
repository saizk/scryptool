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
    bot = Twitter(BEARER_TOKEN)

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
    end = datetime.datetime(2021, 12, 1, 0, 0, 0)
    start = datetime.datetime(2021, 12, 2, 0, 0, 0)

    async_bot = AsyncTwitter()

    queries = list(map(gen_query, TICKERS))
    coins = list(TICKERS)

    # async_bot.search(search=gen_query('ETH'), lang='en',
    #                  end_date=end, start_date=start,
    #                  show_cashtags=True, limit=5, output='test.csv')
    # async_bot.run()

    async_bot.search(queries=queries, coins=coins, lang='en',
                     end_date=end, start_date=start,
                     show_cashtags=True, output=f'data/twitter/tweets.csv')

    async_bot.parallel_run(n_workers=15)


def lunarcrush_bot():
    bot = LunarCrush()

    info = bot.get_assets(symbol=list(TICKERS), data_points=100, interval='day')

    data = info['data']
    time_series = [ts.pop('timeSeries') for ts in data]
    pprint(time_series)

    df = pd.DataFrame(data, index=[i for i in range(len(TICKERS))])
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
    display(db2.head())
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
    async_twitter()
    # lunarcrush_bot()
    # santiment_bot()


if __name__ == '__main__':
    main()
