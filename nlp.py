import re
import nltk
import pandas as pd
import preprocessor as p
import glob
import numpy as np

import transformers
from pathlib import Path
from IPython.core.display import display
from concurrent.futures import ThreadPoolExecutor
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
    classifier = transformers.pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    # with ThreadPoolExecutor() as pool:
    #     santiment = pool.map(classifier, tweet_list)

    santiment = classifier(tweet_list)
    return santiment


def create_sentiment_df(parsed_tweets_df):
    tweet_list = list(parsed_tweets_df["clean_tweets"])
    santiment = sentiment(tweet_list)

    parsed_tweets_df["sentiment"] = [s["label"] for s in santiment]
    return parsed_tweets_df


def create_influencer_sentiment_df(df):

    total_col_df = df.groupby(["coin", "username"]).size()
    total = total_col_df.to_frame(name='total').reset_index()["total"]

    sentiment = df.groupby(['coin', 'username', "sentiment"]).size()
    sent_counter = sentiment.to_frame(name="count").unstack().reset_index()
    sent_counter_columns = sent_counter[["coin", "username"]]

    sent_counter.columns = sent_counter.columns.droplevel()
    sent_counter["total"] = total

    sent_counter[["NEG", "NEU", "POS"]] = sent_counter[["NEG", "NEU", "POS"]].div(sent_counter.total, axis=0)
    sent_counter = sent_counter[["NEG", "NEU", "POS"]]

    sent_counter_columns.columns = sent_counter_columns.columns.droplevel("sentiment")

    sentiment_df = pd.concat([sent_counter_columns, sent_counter], axis=1)
    sentiment_df = sentiment_df.fillna(0)

    return sentiment_df
