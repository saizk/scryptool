import csv
import datetime
import json
import time
from IPython.display import display

from pprint import pprint

import pandas as pd
from dataprep.eda import create_report

from scraper._config import *
from scraper.utils import *
from scraper.twitter import Twitter, AsyncTwitter
from scraper.lunarcrush import LunarCrush



def gen_query(query):
    TICKERS = {
        'BTC': ['BTC', 'bitcoin'],
        'ETH': ['ETH', 'ethereum'],
        'SHIB': ['SHIB', 'shiba inu'],
        '': []
    }
    return ' OR '.join(TICKERS[query])


def twitter_bot():
    bot = Twitter(BEARER_TOKEN)

    coin = gen_query('BTC')
    # recent_tweets = bot.get_recent_tweets(query=coin, max_results=10)
    # print(recent_tweets)

    recent_tweets_count = bot.get_recent_tweets_count(coin, granularity='day')
    for tw in recent_tweets_count:
        pprint(tw)


def async_twitter():
    coin = gen_query('ETH')
    # coin = 'ETH'
    async_bot = AsyncTwitter()
    async_bot.get_all_tweets(query=coin, limit=10,
                             show_cashtags=True, output='test.db')


def save_json(data, file='results.json'):
    with open(file, "w") as f:
        json.dump(data, f)


def lunarcrush_bot():
    bot = LunarCrush(LUNAR_CRUSH_API_KEY)
    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    end = datetime.datetime(2021, 12, 1, 0, 0, 0)
    info = bot.get_assets(symbol=['ETH'],
                          start=start, end=end, interval='hour')
    data = info['data']
    time_series = data[0].pop('timeSeries')

    file, ts = 'results.csv', 'time_series.csv'
    save_csv(data, file)
    save_csv(time_series, ts)

    df = pd.read_csv(file)
    display(df)
    report = create_report(df)
    print(report)


def main():
    # twitter_bot()
    # async_twitter()
    lunarcrush_bot()


if __name__ == '__main__':
    main()
