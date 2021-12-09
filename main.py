import csv
import json
import time
import datetime

from pprint import pprint
# from IPython.display import display

import san
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

    start = datetime.datetime(2021, 12, 4, 0, 0, 0)
    end = datetime.datetime(2021, 12, 5, 0, 0, 0)
    # recent_tweets = bot.get_recent_tweets(
    #     query=coin, lang='en',
    #     start_time=start, end_time=end
    # )
    # print(recent_tweets)
    # all_tweets_count = bot.get_all_tweets_count(
    # query=coin, granularity='day', start_time=start
    # )  # 403 Forbidden :(
    # for coin in TICKERS:
    #     recent_tweets_count = bot.get_recent_tweets_count(
    #         query=gen_query(coin),
    #         granularity='hour', lang='en',
    #         start_time=start, end_time=end
    #     )
    #     save_json(recent_tweets_count, f'data/twitter/{coin.lower()}_count.json')
    #
    #     for tw in recent_tweets_count:
    #         pprint(tw)
    count = 0
    resume = {}
    for coin in TICKERS:
        with open(f'data/twitter/{coin}_count.json') as f:
            data = json.load(f)
            count += data[-1]['total_tweet_count']
            resume[coin] = data[-1]
    pprint(resume)
    print(count)


def async_twitter():
    end = datetime.datetime(2021, 12, 4, 16, 38, 22)
    start = datetime.datetime(2021, 12, 5, 0, 0, 0)

    async_bot = AsyncTwitter()

    queries = list(map(gen_query, TICKERS))
    coins = list(TICKERS)

    async_bot.search(search=gen_query('BTC'), lang='en',
                     end_date=end, start_date=start, limit=5,
                     show_cashtags=True, output='data/twitter/btc_tweets.csv')
    # async_bot.thread_run()

    async_bot.run()

    # async_bot.search(queries=queries, coins=coins, lang='en',
    #                  end_date=end, start_date=start, lowercase=True,
    #                  show_cashtags=True, output=f'data/twitter/tweets.csv')
    #
    # async_bot.parallel_run()


def dashboard_1():
    sanbot = Santiment(SANTIMENT_API_KEY)

    db1_1 = dashboards.gen_dashboard_1_1(
        sanbot, TICKERS, save_all=False,
        from_date='2021-09-01', to_date='2021-12-01',
        interval='1d'
    )
    db1_1.to_csv(f'data/dashboard1/db1_data_1.csv')

    db1_2 = dashboards.gen_dashboard_1_2(
        sanbot, TICKERS, save_all=False,
        from_date='2021-09-01', to_date='2021-12-01',
        interval='1d'
    )
    db1_2.to_csv(f'data/dashboard1/db1_data_2.csv')
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')


def dashboard_2():
    sanbot = Santiment(SANTIMENT_API_KEY)
    lcbot = LunarCrush()

    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    end = datetime.datetime(2021, 12, 1, 0, 0, 0)

    # SANTIMENT
    db2_1 = dashboards.gen_dashboard_2_santiment(
        sanbot, platforms=['twitter', 'reddit', 'telegram', 'bitcointalk'],
        tickers=TICKERS, save_all=False,
        from_date='2021-09-01', to_date='2021-12-01',
        interval='1d'
    )
    db2_1.to_csv(f'data/dashboard2/db2_data_1.csv')
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')

    # LUNARCRUSH
    data_points = (datetime.datetime.today() - start).days + 1
    lcmetrics = lcbot.get_assets(
        symbol=list(TICKERS), data_points=data_points,
        interval='day', change='6m'
    )

    db2_2 = dashboards.gen_dashboard_2_lunarcrush(lcmetrics, end)
    db2_2.to_csv('data/dashboard2/db2_data_2.csv')


def dashboard_3():
    sanbot = Santiment(SANTIMENT_API_KEY)

    db3 = dashboards.gen_dashboard_3(
        sanbot, TICKERS, save_all=False,
        from_date='2021-09-01', to_date='2021-12-01',
        interval='1d'
    )
    db3.to_csv(f'data/dashboard3/db3_data.csv')
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')


def main():
    # twitter_bot()
    async_twitter()
    # dashboard_1()
    # dashboard_2()
    # dashboard_3()


if __name__ == '__main__':
    main()
