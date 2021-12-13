import re
import preprocessor as p


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


def tweet_parser(raw_tweets_df):
    raw_tweets_df["clean_tweets"] = raw_tweets_df["tweet"]
    raw_tweets_df["clean_tweets"] = raw_tweets_df["clean_tweets"].apply(lambda x: tweet_cleaner(x))
    return raw_tweets_df
