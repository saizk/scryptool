import re
from pathlib import Path

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
