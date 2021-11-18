from pprint import pprint
from scraper._config import *
from scraper.twitter import Twitter
from scraper.lunarcrush import LunarCrush


def lunarcrush_bot():
    bot = LunarCrush(LUNAR_CRUSH_API_KEY)
    info = bot.get_assets(coins=['ETH'], interval='day')
    pprint(info)


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

    # coin = 'BTC'
    # recent_tweets = bot.get_recent_tweets(coin, max_results=10)
    # print(recent_tweets)

    bot.async_get_all_tweets(query='BTC', limit=10, file='test.db')
    # recent_tweets_count = bot.get_recent_tweets_count('ETH')
    # for tw in recent_tweets_count:
    #     pprint(tw)


def main():
    twitter_bot()
    # lunarcrush_bot()
    # test_twint()


if __name__ == '__main__':
    main()
