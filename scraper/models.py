import sqlalchemy as sq
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from .utils import classproperty

Model = declarative_base()
Model.__tablename__ = classproperty(lambda o: o.__name__.lower())


def init_db(db_uri):
    engine = sq.create_engine(db_uri)
    Model.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker(bind=engine))
    Tweet.__table__.create(bind=engine, checkfirst=True)
    Politician.__table__.create(bind=engine, checkfirst=True)
    Party.__table__.create(bind=engine, checkfirst=True)
    return session, engine


def create_politician(db, name, party, twitter):
    pol = db.query(Politician).filter_by(politician_id=hash(name)).first()
    if pol is None:
        pol = Politician(
            name=name, party=party,
            twitter=twitter, politician_id=hash(name)
        )
        db.add(pol)


def create_party(db, party, twitter):
    pol_party = db.query(Party).filter_by(name=party).first()
    if pol_party is None:
        pol_party = Party(
            name=party, twitter=twitter, party_id=hash(party)
        )
        db.add(pol_party)


def save_tweet(db, tweet):
    db_tweet = db.query(Tweet).filter_by(tweet_id=hash(tweet.id)).first()
    if db_tweet is None:
        politician = get_politicians(db, tweet.user.screen_name)
        db_tweet = Tweet(
            party=politician.party,
            text=tweet.full_text,
            retweets=tweet.retweet_count,
            favs=tweet.favorite_count,
            created_at=tweet.created_at,
            author_id=politician.id,
            tweet_id=hash(tweet.id),
        )
        db.add(db_tweet)


def get_politicians(db, twitter):
    politician = db.query(Politician).filter_by(twitter=twitter).first()
    return politician


def get_politicians_twitter_dict(db):
    twitters = {
        user[0]: twitter[0].lower() for user, twitter in zip(db.query(Politician.name),
                                                             db.query(Politician.twitter)) if twitter[0]
    }
    return twitters


class Tweet(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    text = sq.Column(sq.String, nullable=False)

    retweets = sq.Column(sq.Integer, nullable=False)
    favs = sq.Column(sq.Integer, nullable=False)
    party = sq.Column(sq.String(128), nullable=False)

    created_at = sq.Column(sq.DateTime, nullable=False)
    author_id = sq.Column(sq.Integer, sq.ForeignKey('politician.id'), nullable=False)
    tweet_id = sq.Column(sq.Integer, nullable=False)  # hash


class Politician(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    twitter = sq.Column(sq.String(128))
    party = sq.Column(sq.String(128), nullable=False)
    politician_id = sq.Column(sq.Integer, nullable=False)  # hash
    tweets = orm.relationship("Tweet",
                              backref="politician",
                              cascade="all, delete-orphan")


class Party(Model):
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False)
    twitter = sq.Column(sq.String(128))
    party_id = sq.Column(sq.Integer, nullable=False)  # hash

