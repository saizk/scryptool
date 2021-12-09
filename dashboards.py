import datetime

import pandas as pd

from pathlib import Path
from scraper.tickers import *


def gen_dashboard_1(sanbot, option, **kwargs) -> pd.DataFrame:
    #coin_dfs = []
    #path = Path('data/dashboard1/mean_last_month')
    #path.mkdir(parents=True, exist_ok=True)
    #DASHBOARD 1.1
    if option == 1:
        stats = ["Asset", "sentiment_positive_total", "sentiment_negative_total", "dev_activity", "dev_activity_change_30d",
                 "dev_activity_contributors_count", "github_activity_contributors_count", "marketcap_usd"]
        df = pd.DataFrame(columns=stats)
        for idx, coin in enumerate(TICKERS):
            counter = 0
            print(f'{coin}  {idx + 1}/{len(TICKERS)}')
            row = {stats[counter]: coin}
            counter += 1
            #Fact 1: for sentiment metrics there is no data available from some dates
            positive_sentiment = sanbot.get_sentiment_positive(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
            row[stats[counter]] = positive_sentiment[stats[counter]].mean()
            counter += 1

            negative_sentiment = sanbot.get_sentiment_negative(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
            row[stats[counter]] = negative_sentiment[stats[counter]].mean()
            counter += 1

            #Fact 2: tickers 'SHIB' and 'CRO' has no activity in the last month, returns empty dataframes
            try:
                dev_activity = sanbot.get_developers_activity(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
                row[stats[counter]] = dev_activity[stats[counter]].mean()
                counter += 1

            except:
                row[stats[counter]] = 0
                counter += 1

            try:

                dev_activity_change_30d = sanbot.get_developers_activity_change_30d(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
                row[stats[counter]] = dev_activity_change_30d[stats[counter]].mean()
                counter += 1

            except:
                row[stats[counter]] = 0
                counter += 1

            try:
                dev_activity_contributors_count = sanbot.get_developers_activity_contributors_count(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
                row[stats[counter]] = dev_activity_contributors_count[stats[counter]].mean()
                counter += 1

            except:
                row[stats[counter]] = 0
                counter += 1

            try:
                github_activity_contributors_count = sanbot.get_github_activity_contributors_count(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
                row[stats[counter]] = github_activity_contributors_count[stats[counter]].mean()
                counter += 1

            except:
                row[stats[counter]] = 0
                counter += 1

            marketcap = sanbot.get_marketcap(coin, from_date="2021-11-01", to_date="2021-12-01", **kwargs)
            row[stats[counter]] = marketcap[stats[counter]].mean()

            df = df.append(row, ignore_index=True)
            df = df.round(2)

        return df

    if option == 2:
        c_names = ["Asset", "Month", "Day", "active_addresses_24h", "exchange_balance", "network_growth",
                   "transaction_volume", "bitmex_perpetual_funding_rate", "price_usd", "marketcap_usd", "volume_usd"]
        df_end = pd.DataFrame(columns=c_names)
        for idx, coin in enumerate(TICKERS):
            counter = 0
            print(f'{coin}  {idx + 1}/{len(TICKERS)}')
            if coin == 'SOL' or coin == 'ADA' or coin == 'DOT' or coin == 'LUNA' or coin == 'DOGE' or coin == 'AVAX' or coin == 'ALGO':
                counter += 1
            else:
                active_addresses_24h = sanbot.get_active_addresses(coin, from_date="2021-09-01", to_date="2021-11-08", **kwargs).reset_index(level=0)
                active_addresses_24h['Month'] = pd.DatetimeIndex(active_addresses_24h['datetime']).month
                active_addresses_24h['Day'] = pd.DatetimeIndex(active_addresses_24h['datetime']).day
                active_addresses_24h.insert(0, 'Asset', pd.Series(coin).repeat(69).values)
                cols = active_addresses_24h.columns.tolist()
                reorder = cols.pop(2)
                cols.append(reorder)
                active_addresses_24h = active_addresses_24h[cols]

                try:
                    exchange_balance = sanbot.get_exchange_balance(coin, from_date="2021-09-01", to_date="2021-12-01", **kwargs).reset_index(level=0)
                except:
                    exchange_balance = pd.Series(0).repeat(69)
                try:
                    network_growth = sanbot.get_network_growth(coin, from_date="2021-09-01", to_date="2021-12-01", **kwargs).reset_index(level=0)
                except:
                    network_growth = pd.Series(0).repeat(69)
                transaction_volume = sanbot.get_transaction_volume(coin, from_date="2021-09-01", to_date="2021-12-01", **kwargs).reset_index(level=0)
                try:
                    bitmex_perpetuals_funding_rate = sanbot.get_bitmex_perpetuals_funding_rate(coin, from_date="2021-09-01", to_date="2021-12-01", **kwargs).reset_index(level=0)
                except:
                    bitmex_perpetuals_funding_rate = pd.Series(0).repeat(69)
                price_usd = sanbot.get_price(coin, from_date="2021-09-01", to_date="2021-11-08", **kwargs).reset_index(level=0)
                marketcap_usd = sanbot.get_marketcap(coin, from_date="2021-09-01", to_date="2021-11-08", **kwargs).reset_index(level=0)
                volume_usd = sanbot.get_volume(coin, from_date="2021-09-01", to_date="2021-11-08", **kwargs).reset_index(level=0)
                try:
                    df = pd.merge(active_addresses_24h, exchange_balance)
                except:
                    df = active_addresses_24h.assign(exchange_balance=exchange_balance)
                try:
                    df = pd.merge(df, network_growth)
                except:
                    df = df.assign(network_growth=network_growth)
                df = pd.merge(df, transaction_volume)
                try:
                    df = pd.merge(df, bitmex_perpetuals_funding_rate)
                except:
                    df = df.assign(bitmex_perpetual_funding_rate=bitmex_perpetuals_funding_rate)

                df = df.assign(price_usd=price_usd["price_usd"])
                df = df.assign(marketcap_usd=marketcap_usd["marketcap_usd"])
                df = df.assign(volume_usd=volume_usd["volume_usd"])
                df = df.fillna(0)

            df_end = pd.concat([df_end, df])
        df_end = df_end.drop(labels='datetime', axis = 1)
        print(df_end)


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
    df_end = pd.DataFrame(columns=["Asset", "price_usd", "volume_usd", "circulation_1d"])
    for coin in TICKERS.keys():
        print(coin)
        price_usd = sanbot.get_price(coin, from_date="2021-11-01", to_date="2021-11-01", **kwargs).reset_index(level=0)
        price_usd.insert(0, 'Asset', pd.Series(coin).repeat(1).values)
        volume_usd = sanbot.get_volume(coin, from_date="2021-11-01", to_date="2021-11-01", **kwargs).reset_index(level=0)
        try:
            circulation_1d = sanbot.get_circulation_1d(coin, from_date="2021-11-01", to_date="2021-11-01", **kwargs).reset_index(level=0)
        except:
            circulation_1d = pd.Series(0).repeat(1)

        df = pd.merge(price_usd, volume_usd)
        try:
            df = pd.merge(df, circulation_1d)
        except:
            df = df.assign(circulation_1d=circulation_1d)
        df_end = pd.concat([df_end, df])
    df_end = df_end.drop(labels='datetime', axis=1)
    df_end = df_end.fillna(0)
    df_end = df_end.reset_index(drop=True)
    print(df_end)

def gen_dashboard_4(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass
