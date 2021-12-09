import san
import time
import pandas as pd

from pathlib import Path

class Santiment(object):

    def __init__(self, api_key):
        san.ApiConfig.api_key = api_key

    def _from_ticker_to_slug(self, ticker, coins_csv='data/coins.csv'):
        Path(Path(coins_csv).parent).mkdir(parents=True, exist_ok=True)

        if not Path(coins_csv).exists():
            coins = self.list_all_coins()
            coins.to_csv(coins_csv)

        df = pd.read_csv(coins_csv)
        slug = df[df['ticker'] == ticker.upper()]['slug'].values[0]
        return slug

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

    def get_sentiment_positive(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'sentiment_positive_total/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_sentiment_negative(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'sentiment_negative_total/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_developers_activity(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'dev_activity/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_developers_activity_change_30d(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'dev_activity_change_30d/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_developers_activity_contributors_count(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'dev_activity_contributors_count/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_github_activity_contributors_count(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'github_activity_contributors_count/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_active_addresses(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'active_addresses_24h/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_exchange_balance(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'exchange_balance/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_network_growth(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'network_growth/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_transaction_volume(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'transaction_volume/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_bitmex_perpetuals_funding_rate(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'bitmex_perpetual_funding_rate/{self._from_ticker_to_slug(coin)}', **kwargs)

    def get_circulation_1d(self, coin: str, **kwargs) -> pd.DataFrame:
        return self._request(san.get, f'circulation_1d/{self._from_ticker_to_slug(coin)}', **kwargs)

