import re
import nltk
import preprocessor as p
import glob

import pandas as pd

# dashboard 4.1

def sentiment(tweet):
    pass

def create_sentiment_df():
    pass

# nltk.download('words')
# words = set(nltk.corpus.words.words())


# def cleaner(tweet):
#     p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION)
#     tweet = p.clean(tweet)  # Remove URLs, Emojis and Mentions
#     tweet = tweet.lower()
#
#     remove_characters = [".", ",", "/", ":", "-", "?", "!"]
#     for character in remove_characters:
#         tweet = tweet.replace(character, "")
#     tweet = re.sub(r'#\S+', '', tweet).strip()
#     tweet = re.sub(r'\$\S+', '', tweet).strip()
#
#     return tweet


# def tweet_parser(df_path):
#     raw_df = pd.read_csv(df_path)
#     raw_df["cleaned_tweet"] = raw_df["tweet"]
#
#     for row in raw_df["cleaned_tweet"]:
#         row.apply(cleaner())
#
#     return



# DASHBOARD 4.2
def create_coin_df(TICKERS):
    for ticker in list(TICKERS):
        merged_df = pd.concat(
                [pd.read_csv(f) for f in glob.glob(f'data/twitter/{ticker}*.csv')],
                axis='index'
            )
        merged_df["coin"] = ticker
        merged_df.to_csv(f'data/twitter/nlp/{ticker}_all_tweets.csv', index=False)
    return

def read_all_csv():
    df = pd.concat(
        [pd.read_csv(f) for f in glob.glob(input_directory)],
        axis='index'
    )
    return df

def create_top5_df(input_directory, output_directory):
    df = pd.concat(
        [pd.read_csv(f) for f in glob.glob(input_directory)],
        axis='index'
    )
    df["tweet_score"] = df["retweets_count"] + df["likes_count"] * 0.25
    df = df.sort_values(['tweet_score'], ascending=False).groupby('coin').head(5).reset_index(drop=True)
    df.to_csv(output_directory, index=False)
    return df




