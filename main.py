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

    info = bot.get_assets(symbol=list(TICKERS), data_points=90, interval='day', change='3m')


    #Dashboard2
    data = info['data']
    symbols = {s.pop("id"): s.pop("symbol") for s in data}

    time_series = [ts.pop('timeSeries') for ts in data]
    # pprint(time_series)

    # with open("timeseries.pickle", 'wb') as f:
    #     pickle.dump(time_series, f)

    dashboard2 = pd.concat([pd.DataFrame(ts) for ts in time_series])
    dashboard2.reset_index()
    dashboard2['time'] = pd.to_datetime(dashboard2['time'], unit='s')
    dashboard2['time'] = dashboard2['time'].apply(lambda x: x - datetime.timedelta(days=8))
    dashboard2.drop(['open', 'close', 'high', 'low', 'volume', 'market_cap', 'reddit_comments', 'reddit_comments_score',
                     'tweet_spam', 'tweet_quotes', 'tweet_sentiment1', 'tweet_sentiment2', 'tweet_sentiment3',
                     'tweet_sentiment4', 'tweet_sentiment5', 'tweet_sentiment_impact1', 'tweet_sentiment_impact2',
                     'tweet_sentiment_impact3', 'tweet_sentiment_impact4', 'tweet_sentiment_impact5',
                     'sentiment_absolute', 'sentiment_relative', 'search_average', 'price_score', 'social_impact_score',
                     'alt_rank', 'alt_rank_30d', 'alt_rank_hour_average', 'market_cap_rank', 'percent_change_24h_rank',
                     'volume_24h_rank', 'social_volume_24h_rank', 'social_score_24h_rank', 'percent_change_24h'],
                    axis=1, inplace=True)

    dashboard2["asset_id"].replace(symbols, inplace=True)

    dashboard2.to_csv("data\lunarcrush_data.csv")
    display(dashboard2)


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
    # async_twitter()
    lunarcrush_bot()
    # santiment_bot()


if __name__ == '__main__':
    main()
