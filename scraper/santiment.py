from pathlib import Path

import san
import time
import pandas as pd


class Santiment(object):

    def __init__(self, api_key):
        san.ApiConfig.api_key = api_key

    @staticmethod
    def _request(func, *args, **kwargs):
        try:
            col_name = args[0].split('/')[0]
            df = func(*args, **kwargs).rename(columns={'value': col_name})
            return df

        except Exception as e:
            if san.is_rate_limit_exception(e):
                rate_limit_seconds = san.rate_limit_time_left(e)
                print(f'Will sleep for {rate_limit_seconds}')
                time.sleep(rate_limit_seconds)

    def list_all_coins(self) -> pd.DataFrame:
        return self._request(san.get, 'projects/all')

    def get_price(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'price_usd/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_volume(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'volume_usd/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_marketcap(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'marketcap_usd/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_social_volume(self, coin: str, platform: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'social_volume_{platform}/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_sentiment_balance(self, coin: str, platform: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'sentiment_balance_{platform}/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_social_dominance(self, coin: str, platform: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'social_dominance_{platform}/{self._from_ticker_to_slug(coin)}', **kwargs)

    def _from_ticker_to_slug(self, ticker, coins_csv='data/coins.csv'):
        Path(Path(coins_csv).parent).mkdir(parents=True, exist_ok=True)

        if not Path(coins_csv).exists():
            coins = self.list_all_coins()
            coins.to_csv(coins_csv)

        df = pd.read_csv(coins_csv)
        slug = df[df['ticker'] == ticker]['slug'].values[0]
        return slug
