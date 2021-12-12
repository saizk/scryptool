import re
from pathlib import Path

import nltk
import preprocessor as p
import glob

import pandas as pd

import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Tweet parser
nltk.download('words')
words = set(nltk.corpus.words.words())


def tweet_cleaner(tweet):
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION, p.OPT.NUMBER)
    tweet = p.clean(tweet)  # Remove URLs, Emojis and Mentions
    tweet = tweet.lower()

    remove_characters = [".", ",", ";", "/", "|" ":", "-", "+", "?", "!"]
    for character in remove_characters:
        tweet = tweet.replace(character, "")
    tweet = re.sub(r'#\S+', '', tweet).strip()
    tweet = re.sub(rf'\$\S+', '', tweet).strip()
    tweet = re.sub(rf'\&\S+', '', tweet).strip()

    return tweet


def tweet_parser(raw_tweets_df, path):
    raw_tweets_df["clean_tweets"] = raw_tweets_df["tweet"]
    raw_tweets_df["clean_tweets"] = raw_tweets_df["clean_tweets"].apply(lambda x: tweet_cleaner(x))

    raw_tweets_df.to_csv(rf'{path}', index_label=False)
    return raw_tweets_df


# dashboard 4.1
def sentiment(tweet_list):
    tokenizer = AutoTokenizer.from_pretrained("finiteautomata/beto-sentiment-analysis")
    model = AutoModelForSequenceClassification.from_pretrained("finiteautomata/beto-sentiment-analysis")
    classifier = transformers.pipeline("sentiment-analysis", model=model, tokenizer = tokenizer)

    santiment = classifier(tweet_list)
    santiment_list = [s["label"] for s in santiment]

    return santiment_list


def create_sentiment_df(parsed_tweets_df):
    parsed_tweets_df["sentiment"] = sentiment(list(parsed_tweets_df["clean_tweets"]))
    return parsed_tweets_df

def create_influencer_sentiment_df(df):
    pass

# DASHBOARD 4.2



