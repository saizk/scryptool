import datetime

import pandas as pd

from pathlib import Path
from scraper.tickers import *


def gen_dashboard_1(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass


def gen_dashboard_2_santiment(sanbot, platforms, tickers, save_all, **kwargs) -> pd.DataFrame:
    coin_dfs = []
    path = Path('data/dashboard2/santiment')
    path.mkdir(parents=True, exist_ok=True)

    for idx, coin in enumerate(tickers):
        print(f'{coin}  {idx + 1}/{len(tickers)}')
        dfs_metrics = [sanbot.get_social_volume(coin, platform=plat, **kwargs) for plat in platforms]

        df = pd.concat(dfs_metrics, axis='columns')
        df.insert(0, 'asset', [coin] * len(df), True)
        df['price_usd'] = sanbot.get_price(coin, **kwargs)['price_usd']

        if save_all:
            df.to_csv(f'{path}/{coin.lower()}_social_volume.csv')

        coin_dfs.append(df)

    merged_df = pd.concat(coin_dfs, axis='index')

    return merged_df


def gen_dashboard_2_lunarcrush(lcmetrics, end):
    data = lcmetrics['data']

    symbols = {s.pop('id'): s.pop('symbol') for s in data}
    time_series = [ts.pop('timeSeries') for ts in data]

    df = pd.concat([pd.DataFrame(ts) for ts in time_series])
    df.reset_index()
    df['time'] = pd.to_datetime(df['time'], unit='s')
    additional_points = (datetime.datetime.today() - end).days
    df.drop(df.tail(additional_points).index,
            inplace=True)  # remove additional data (> 1/12/21)
    df.drop(
        ['open', 'close', 'high', 'low', 'volume', 'market_cap', 'reddit_comments', 'reddit_comments_score',
         'tweet_spam', 'tweet_quotes', 'tweet_sentiment1', 'tweet_sentiment2', 'tweet_sentiment3',
         'tweet_sentiment4', 'tweet_sentiment5', 'tweet_sentiment_impact1', 'tweet_sentiment_impact2',
         'tweet_sentiment_impact3', 'tweet_sentiment_impact4', 'tweet_sentiment_impact5',
         'sentiment_absolute', 'sentiment_relative', 'search_average', 'price_score', 'social_impact_score',
         'alt_rank', 'alt_rank_30d', 'alt_rank_hour_average', 'market_cap_rank', 'percent_change_24h_rank',
         'volume_24h_rank', 'social_volume_24h_rank', 'social_score_24h_rank', 'percent_change_24h'],
        axis=1, inplace=True
    )
    df['asset_id'].replace(symbols, inplace=True)
    df = df.rename(columns={'asset_id': 'asset'})
    return df


def gen_dashboard_3(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass


def gen_dashboard_4(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass
