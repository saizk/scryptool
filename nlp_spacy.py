import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import pandas as pd
import spacy
from collections import Counter

from IPython.display import display


def main():
    try:
        nlp = spacy.load(model)
    except OSError:
        os.system(f'python -m spacy download {model}')
    nlp = spacy.load(model)
    df = pd.read_csv("nlp/parsed_tweets2.csv")

    # with ThreadPoolExecutor(max_workers=32) as pool:
    with ProcessPoolExecutor(None) as pool:
        docs = pool.map(
            lambda tw: nlp(str(tw)),
            df['clean_tweets']
        )
    # docs = [nlp(str(tw)) for tw in df['clean_tweets']]
    print('nlp finished mthfka')
    print(len(df['coin']))
    print(len(docs))
    exit()
    global_counter = {}
    for coin, doc in zip(df['coin'], docs):
        words = [
            token.text
            for token in doc
            if not token.is_stop and not token.is_punct and not token.is_space
        ]  # all tokens that arent stop words or punctuations
        global_counter[coin] = Counter(words)

        # nouns = [
        #     token.text
        #     for token in doc
        #     if (not token.is_stop and not token.is_punct and token.pos_ == "NOUN")
        # ]  # noun tokens that arent stop words or punctuations
        #
        # noun_freq = Counter(nouns)  # five most common noun tokens

        # common_nouns = noun_freq.most_common(5)

    print(global_counter)
    common_words = {
        coin: counter.most_common(5)
        for coin, counter in global_counter.items()
    }
    print(common_words)


if __name__ == '__main__':
    model = 'en_core_web_sm'
    main()
