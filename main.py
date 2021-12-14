import san
import glob
import datetime
import pandas as pd

from pathlib import Path

import dashboards

from utils import *
from nlp.pipeline import NLPPipeline
from scrapers import Santiment, LunarCrush, Twitter, AsyncTwitter, Kraken, GlassNode, TICKERS
from _config import *


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
    )
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


def dashboard_4(start, end):

    # twitter_bot(start, end)
    # async_twitter(start, end)  # scrape tweets

    # DASHBOARD 4.1 SENTIMENT ANALYSIS
    sentiment_df = dashboards.gen_dashboard_4_1_sentiment(
        f'data/twitter/raw_tweets',
        list(TICKERS)
    )
    sentiment_df.to_csv(f'data/dashboard4/sentiment_df.csv', index=False)

    influencer_sent_df = dashboards.gen_dashboard_4_1_influencers_sentiment(sentiment_df)
    influencer_sent_df.to_csv(f'data/dashboard4/db4_data1.csv', index=False)

    # DASHBOARD 4.2 TOP 5 TWEETS
    sentiment_df = pd.read_csv(rf'data/dashboard4/sentiment_df.csv', index_col=False)
    top_5 = dashboards.gen_dashboard_4_2(sentiment_df, top_n_tweets=5)
    top_5.to_csv(f'data/dashboard4/db4_data_2.csv', index=False)

    # DASHBOARD 4.3 CLOUD WORD
    model_name = 'en_core_web_sm'
    n_words = 50
    nlp_pipeline = NLPPipeline(
        model_name=model_name,
        data=pd.read_csv("data/dashboard4/parsed_tweets.csv")
    )
    cloud_word_df = dashboards.gen_dashboard_4_3(nlp_pipeline)
    cloud_word_df.to_csv(f'data/dashboard4/db4_data_3_{n_words}.csv')


def main():
    start = datetime.datetime(2021, 9, 1, 0, 0, 0)
    end = datetime.datetime(2021, 12, 1, 0, 0, 0)
    dashboard_1(start, end)
    dashboard_2(start, end)
    dashboard_3(start, end)
    dashboard_4(start, end)


if __name__ == '__main__':
    main()
