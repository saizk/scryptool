import os
import spacy
import pandas as pd
from collections import Counter
from concurrent.futures import ThreadPoolExecutor


class NLPPipeline(object):

    def __init__(self, model_name: str, data: pd.DataFrame):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            os.system(f'python -m spacy download {model_name}')

        self.nlp = spacy.load(model_name)
        self.data = data

    def get_docs(self):
        with ThreadPoolExecutor() as pool:
            docs = pool.map(
                lambda tw: self.nlp(str(tw)),
                self.data['clean_tweets']
            )
        return docs

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
    def filter_text(doc):
        return [
            token for token in doc
            if not token.is_stop and not token.is_punct and not token.is_space
        ]

    @staticmethod
    def remove_stpwrds(counter, typos):
        remove_stpwrds = {coin: Counter() for coin in counter}
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

    @staticmethod
    def from_counter_to_df(counter):
        df = pd.DataFrame()
        coins, words, counts = [], [], []
        for coin, counters in counter.items():
            coins += [coin] * len(counters)
            words += [word for word, _ in counters]
            counts += [count for _, count in counters]

        df['coin'], df['words'], df['count'] = coins, words, counts
        return df
