import datetime

import pandas as pd

from pathlib import Path

import pycoingecko

import scraper
from scraper.tickers import *


def gen_santiment_dashboard(dashboard, coin, metrics, save_all):
    path = Path(f'data/{dashboard}/santiment')

    df = pd.concat(metrics, axis='columns')
    df.insert(0, 'asset', [coin] * len(df), True)

    if save_all:
        path.mkdir(parents=True, exist_ok=True)
        df.to_csv(f'{path}/{coin.lower()}_{dashboard}.csv')

    return df


def gen_dashboard_1_1(sanbot: scraper.Santiment, tickers, save_all, **kwargs) -> pd.DataFrame:
    coin_dfs = []

    for idx, coin in enumerate(tickers):
        print(f'Dashboard 1.1: {coin}  {idx + 1}/{len(tickers)}')

        metrics = [sanbot.get_sentiment(coin, 'positive', **kwargs),
                   sanbot.get_sentiment(coin, 'negative', **kwargs),
                   sanbot.get_development_activity(coin, **kwargs),
                   sanbot.get_development_activity(coin, 'change_30d', **kwargs),
                   sanbot.get_development_activity(coin, 'contributors_count', **kwargs),
                   sanbot.get_github_activity(coin, 'contributors_count', **kwargs),
                   sanbot.get_marketcap(coin, **kwargs)]

        df = gen_santiment_dashboard('dashboard1', coin, metrics, save_all)
        coin_dfs.append(df)

    db1 = pd.concat(coin_dfs, axis='index').reset_index()

    return db1


def gen_dashboard_1_2(
        sanbot: scraper.Santiment,
        geckobot: pycoingecko.CoinGeckoAPI,
        tickers, save_all, **kwargs
):
    coin_dfs = []
    path = Path('data/dashboard1/santiment')

    for idx, coin in enumerate(tickers):
        print(f'Dashboard 1.2: {coin}  {idx + 1}/{len(tickers)}')

        metrics = [
                   sanbot.get_price(coin, **kwargs),
                   sanbot.get_marketcap(coin, **kwargs),
                   sanbot.get_volume(coin, **kwargs)]

        df = gen_santiment_dashboard('dashboard1', coin, metrics, save_all)
        coin_dfs.append(df)

    db1 = pd.concat(coin_dfs, axis='index').reset_index()

    return db1


def gen_dashboard_2_santiment(sanbot: scraper.Santiment, platforms, tickers, save_all, **kwargs) -> pd.DataFrame:
    coin_dfs = []
    path = Path('data/dashboard2/santiment')

    for idx, coin in enumerate(tickers):
        print(f'Dashboard 2.1: {coin}  {idx + 1}/{len(tickers)}')
        dfs_metrics = [sanbot.get_social_volume(coin, platform=plat, **kwargs) for plat in platforms]

        df = pd.concat(dfs_metrics, axis='columns')
        df.insert(0, 'asset', [coin] * len(df), True)
        df['price_usd'] = sanbot.get_price(coin, **kwargs)['price_usd']

        if save_all:
            path.mkdir(parents=True, exist_ok=True)
            df.to_csv(f'{path}/{coin.lower()}_social_volume.csv')

        coin_dfs.append(df)

    merged_df = pd.concat(coin_dfs, axis='index')

    return merged_df


def gen_dashboard_2_lunarcrush(lcbot: scraper.LunarCrush, tickers, start, end):
    path = Path('data/dashboard2')
    print(f'Dashboard 2.2:')

    data_points = (datetime.datetime.today() - start).days + 1
    lcmetrics = lcbot.get_assets(
        symbol=tickers, data_points=data_points,
        interval='day', change='6m'
    )

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


def gen_dashboard_3(sanbot: scraper.Santiment, tickers, save_all, **kwargs) -> pd.DataFrame:
    coin_dfs = []
    path = Path('data/dashboard3/santiment')

    for idx, coin in enumerate(tickers):
        print(f'Dashboard 3: {coin}  {idx + 1}/{len(tickers)}')

        metrics = [sanbot.get_price(coin, **kwargs),
                   sanbot.get_marketcap(coin, **kwargs),
                   sanbot.get_circulation(coin, **kwargs)]

        df = gen_santiment_dashboard('dashboard3', coin, metrics, save_all)
        coin_dfs.append(df)

    db3 = pd.concat(coin_dfs, axis='index').reset_index()

    return db3


def gen_dashboard_4(bot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass
