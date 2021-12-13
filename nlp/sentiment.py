import nltk
import pandas as pd


import transformers
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Tweet parser
nltk.download('words')
words = set(nltk.corpus.words.words())


# dashboard 4.1
def sentiment(tweet_list):
    tokenizer = AutoTokenizer.from_pretrained("finiteautomata/beto-sentiment-analysis")
    model = AutoModelForSequenceClassification.from_pretrained("finiteautomata/beto-sentiment-analysis")
    classifier = transformers.pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    # with ThreadPoolExecutor() as pool:
    #     santiment = pool.map(classifier, tweet_list)
    santiment = classifier(tweet_list)
    return santiment


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
