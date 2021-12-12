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

    @staticmethod
    def filter_text(doc):
        return [
            token for token in doc
            if not token.is_stop and not token.is_punct and not token.is_space
        ]

    def count_words(self, remove_words=None):
        docs = self.get_docs()

        global_counter = {coin: Counter() for coin in set(self.data['coin'])}

        for coin, doc in zip(self.data['coin'], docs):
            doc = self.filter_text(doc)
            words = [token.text for token in doc]
            global_counter[coin].update(Counter(words))

        if remove_words is not None:
            global_counter = self.remove_stpwrds(global_counter, remove_words)

        return global_counter

    @staticmethod
    def remove_stpwrds(counter, typos):
        remove_stpwrds = {coin: Counter() for coin in TICKERS}
        for coin, v in counter.items():
            for word, count in v.items():
                if word in typos:
                    continue
                remove_stpwrds[coin].update({word: count})
        return remove_stpwrds

    @staticmethod
    def get_most_n_common(counter, n=20):
        return {
            coin: counter.most_common(n)
            for coin, counter in counter.items()
        }


def from_counter_to_df(counter):
    df = pd.DataFrame()
    coins, words, counts = [], [], []
    for coin, counters in counter.items():
        coins += [coin] * len(counters)
        words += [word for word, _ in counters]
        counts += [count for _, count in counters]

    df['coin'], df['words'], df['count'] = coins, words, counts
    return df


def main():

    coin_typos = [word.lower() for words in TICKERS.values() for word in words]
    typos = ['nt', 'tj', 'm', 'tg', 's', 'el', 'rt', '00', 'th', '2', '$', '|',
             'utc', 'crypto', 'vs', 'coin', 'token', 'currency', 'cryptocurrency',
             'currency', 'inu', 'hrs', '24hrs', 'usd'] + list(string.ascii_lowercase) + coin_typos

    nlp_pipeline = NLPPipeline(
        model_name=model,
        data=pd.read_csv("data/nlp/parsed_tweets.csv")
    )
    common_words = nlp_pipeline.count_words(remove_words=typos)
    all_words_count = nlp_pipeline.get_most_n_common(common_words, n=20)

    save_json(all_words_count, 'data/nlp/all_words_count.json')
    # all_words_count = json.load(open('data/nlp/all_words_count.json'))

    df_all_words = from_counter_to_df(all_words_count)

    df_all_words.to_csv('data/nlp/all_words_count.csv')


if __name__ == '__main__':
    model = 'en_core_web_sm'
    main()
