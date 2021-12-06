import pandas as pd

from pathlib import Path
from scraper.tickers import *


def gen_dashboard_1(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass


def gen_dashboard_2(sanbot, **kwargs) -> pd.DataFrame:

    path = Path('data/social_volume')
    path.mkdir(parents=True, exist_ok=True)

    coin_dfs = []
    platforms = ['twitter', 'reddit', 'telegram', 'bitcointalk', 'total']
    tickers = TICKERS.keys()

    for idx, coin in enumerate(tickers):
        print(f'{coin}  {idx + 1}/{len(tickers)}')
        dfs_metrics = [sanbot.get_social_volume(coin, platform=plat, **kwargs) for plat in platforms]

        df = pd.concat(dfs_metrics, axis='columns')
        df.insert(0, 'asset', [coin] * len(df), True)
        df['price_usd'] = sanbot.get_price(coin, **kwargs)['price_usd']
        df.to_csv(f'{path}/{coin.lower()}_social_volume.csv')

        coin_dfs.append(df)

    merged_df = pd.concat(coin_dfs, axis='index')
    merged_df.to_csv(f'{path.parent}/ALL_social_volume.csv')

    return merged_df


def gen_dashboard_3(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass


def gen_dashboard_4(sanbot, **kwargs) -> pd.DataFrame:
    for coin in TICKERS.keys():
        pass
