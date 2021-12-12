import csv
import glob
import json
import time
import datetime

from pprint import pprint
from IPython.display import display
import san
import pandas as pd
import dashboards
import nlp

from scraper._config import *
from scraper.utils import *
from scraper.tickers import *
from scraper import GlassNode, Santiment, LunarCrush, Twitter, AsyncTwitter, Kraken


def gen_query(query: list):
    return ' OR '.join(query)


def twitter_bot(start, end):
    bot = Twitter(BEARER_TOKEN)
    lcbot = LunarCrush()

    data = lcbot.get_top_n_influencers_by_coin(list(TICKERS), limit=5)
    influencers = [infl for coin in data.values() for infl in coin]
    unique_influencers = set(influencers)

    total_tweets = 0
    for coin, users in data.items():
        for user in users:
            recent_tweets_count = bot.get_recent_tweets_count(
                query=gen_query(coin), user=user,
                granularity='day',
                start_time=start, end_time=end
            )
            # save_json(recent_tweets_count, f'data/twitter/{user.lower()}_count.json')

            total_tweets += recent_tweets_count[-1]['total_tweet_count']
            for tw in recent_tweets_count:
                print(tw, user)
    print(total_tweets)


def async_twitter(start, end):

    async_bot = AsyncTwitter()
    lcbot = LunarCrush()

    n_influencers_per_coin = 10
    if not Path('data/influencers.json').exists():
        influencers = lcbot.get_top_n_influencers_by_coin(
            list(TICKERS), limit=n_influencers_per_coin
        )
        save_json(influencers, 'data/influencers.json')
    influencers = json.load(open('data/influencers.json'))

    queries = {t: gen_query(TICKERS[t]) for t in TICKERS}

    async_bot.search(
        users=influencers,
        queries=queries, lang='en',
        end_date=end, start_date=start,
        remove_mentions=True, show_cashtags=True,
        output='data/twitter/raw_tweets/tweets.csv'
    )
    async_bot.parallel_run()

    merged_df = pd.concat(
        [pd.read_csv(f) for f in glob.glob('data/twitter/raw_tweets/*.csv')],
        axis='index'
    ).drop("Unnamed: 0", axis=1)
    merged_df.to_csv('data/influencers_tweets.csv')

    # async_bot.search(
    #     queries=queries, lang='en',
    #     end_date=end, start_date=start,
    #     lowercase=True, show_cashtags=True,
    #     output=f'data/twitter/tweets.csv'
    # )
    # async_bot.parallel_run()


def dashboard_1(start, end):

    sanbot = Santiment(PRO_SANTIMENT_API_KEY)

    # SANTIMENT
    db1_1 = dashboards.gen_dashboard_1_1(
        sanbot, TICKERS, save_all=False,
        start=start, end=end,
        interval='1d'
    )
    db1_1.to_csv(f'data/dashboard1/db1_data_1.csv')

    db1_2 = dashboards.gen_dashboard_1_2(
        sanbot, TICKERS, save_all=False,
        start=start, end=end,
        interval='1d'
    )
    db1_2.to_csv(f'data/dashboard1/db1_data_2.csv')
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')


def dashboard_2(start, end):
    sanbot = Santiment(PRO_SANTIMENT_API_KEY)
    lcbot = LunarCrush()

    # SANTIMENT
    db2_1 = dashboards.gen_dashboard_2_santiment(
        sanbot, platforms=['telegram', 'bitcointalk'],
        tickers=TICKERS, save_all=False,
        start=start, end=end,
        interval='1d'
    )
    db2_1.to_csv(f'data/dashboard2/db2_data_1.csv')
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')

    # LUNARCRUSH
    db2_2 = dashboards.gen_dashboard_2_lunarcrush(lcbot, list(TICKERS), start, end)
    db2_2.to_csv('data/dashboard2/db2_data_2.csv')


def dashboard_3(start, end):
    sanbot = Santiment(PRO_SANTIMENT_API_KEY)

    db3 = dashboards.gen_dashboard_3(
        sanbot, TICKERS, save_all=False,
        start=start, end=end,
        interval='1d'
    )
    db3.to_csv(f'data/dashboard3/db3_data.csv')
    print(f'{san.api_calls_made()[0][-1]} out of {san.api_calls_remaining()}')


def dashboard_4():
    # All tweets with coin label
    df = dashboards.group_tweets_dfs(f'data/twitter/raw_tweets',
                                     list(TICKERS))
    df.to_csv(rf'data\all_tweets_coin.csv', index_label=False)
    # Parse tweets for future dashboards
    parsed_tweets_df = nlp.tweet_parser(df, rf'nlp\parsed_tweets2.csv')

    # DASHBOARD 4.1 SENTIMENT ANALYSIS
    # nlp.sentiment("This restaurant is awesome")
    # sentiment_df = nlp.create_sentiment_df(parsed_tweets_df)
    # print(sentiment_df)


    # DASHBOARD 4.2 TOP5 TWEETS
    top_5 = dashboards.get_top_n_tweets(df, n=5)
    top_5.to_csv(f'data/top_5.csv', index=False)


    # DASHBOARD 4.3 CLOUD WORD
    # tweet_parser("data/influencers_tweets.csv")


def main():
    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    end = datetime.datetime(2021, 12, 1, 0, 0, 0)
    # twitter_bot(start, end)
    # async_twitter(start, end)
    dashboard_1(start, end)
    # dashboard_2(start, end)
    # dashboard_3(start, end)
    # dashboard_4()


if __name__ == '__main__':
    main()
