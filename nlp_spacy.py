import json
import os
import string
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import pandas as pd
import spacy
from collections import Counter

from utils import save_json
from scraper.tickers import TICKERS

from IPython.display import display


class NLPPipeline(object):

    def __init__(self, model_name, data):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            os.system(f'python -m spacy download {model}')

        self.nlp = spacy.load(model)
        self.data = data

    def get_docs(self):
        with ThreadPoolExecutor() as pool:
            docs = pool.map(
                lambda tw: self.nlp(str(tw)),
                self.data['clean_tweets']
            )
        return docs

    def count_words(self, docs, remove_words=None):
        global_counter = {coin: Counter() for coin in set(self.data['coin'])}

        for coin, doc in zip(self.data['coin'], docs):
            words = [
                token.text
                for token in doc
                if not token.is_stop and not token.is_punct and not token.is_space
            ]  # all tokens that arent stop words or punctuations
            global_counter[coin].update(Counter(words))

        if remove_words is not None:
            global_counter = self.remove_stpwrds(global_counter, remove_words)

        return global_counter

    def count_nouns(self, docs, remove_words=None):
        global_nouns = {coin: Counter() for coin in set(self.data['coin'])}

        for coin, doc in zip(self.data['coin'], docs):
            nouns = [
                token.text
                for token in doc
                if (not token.is_stop and not token.is_punct and token.pos_ == "NOUN")
            ]  # noun tokens that arent stop words or punctuations
            global_nouns[coin].update(Counter(nouns))  # five most common noun tokens

        if remove_words is not None:
            global_nouns = self.remove_stpwrds(global_nouns, remove_words)

        return global_nouns

    @staticmethod
    def remove_stpwrds(counter, typos):
        remove_stpwrds = {coin: Counter() for coin in TICKERS}
        for coin, v in counter.items():
            for word, count in v.items():
                if word in typos or word in list(map(str.lower, TICKERS[coin])):
                    continue
                remove_stpwrds[coin].update({word: count})
        return remove_stpwrds

    @staticmethod
    def get_most_n_common(counter, n=20):
        return {
            coin: counter.most_common(n)
            for coin, counter in counter.items()
        }


def main():
    df = pd.read_csv("data/nlp/parsed_tweets.csv")

    nlp_pipeline = NLPPipeline(model_name=model, data=df)
    docs = nlp_pipeline.get_docs()
    typos = ['nt', 'tj', 'm', 'tg', 's'] + list(string.ascii_lowercase)

    common_words = nlp_pipeline.count_words(docs, remove_words=typos)
    common_nouns = nlp_pipeline.count_nouns(docs, remove_words=typos)

    common_words_20 = nlp_pipeline.get_most_n_common(common_words, n=20)
    common_nouns_20 = nlp_pipeline.get_most_n_common(common_nouns, n=20)

    df_words = from_counter_to_df(common_words_20)
    df_words.to_csv('data/nlp/common_words.csv')

    df_nouns = from_counter_to_df(common_nouns_20)
    df_nouns.to_csv('data/nlp/common_nouns.csv')


def from_counter_to_df(counter, ):
    df = pd.DataFrame()
    coins, words, counts = [], [], []
    for coin, counters in counter.items():
        coins += coin
        words += [word for word, _ in counters]
        counts += [count for _, count in counters]
    df['coin'] = coins
    df['words'] = words
    df['count'] = counts
    return df


if __name__ == '__main__':
    model = 'en_core_web_sm'
    main()
