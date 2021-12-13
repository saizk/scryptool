# SCrypto
Crypto Currency Scraper for Twitter

```
pip install -r requirements.txt
```
## SANTIMENT API
| Method         | Description     |
|--------------|-----------|
| **list_all_coins()** | List all available coins in Santiment
| **get_price()** | Price (USD)
| **get_volume()** | Volume (USD)
| **get_daily_trading_volume()** | Daily trading volume (USD)
| **get_marketcap()** | Market Cap (USD)
| **get_social_volume()** | Social volume based on platform (Twitter, Reddit, BitcoinTalk)
| **get_sentiment_balance()** | Sentiment balance of a coin
| **get_social_dominance()** | Social dominance of a coin
| **get_sentiment()** | Sentiment score (positive / negative)
| **get_development_activity()** | Development activity
| **get_github_activity()** | Github activity
| **get_active_addresses_24h()** | On-Chain Active addresses (24h)
| **get_exchange_balance()** | On-Chain Exchange_balance
| **get_network_growth()** | On-Chain Network growth
| **get_transaction_volume()** | On-Chain Transaction volume
| **get_perpetual_funding_rate()** | On-Chain Perpetual funding rate
| **get_circulation()** | On-Chain Circulation supply
| **get_velocity()** | On-Chain Velocity
| **get_withdrawal_transactions()** | On-Chain Withdrawal transactions

## LUNARCRUSH API

### Endpoints
Here is a short description for the LunarCrush API v2 Endpoints.
You can find more details about the request parameters in <https://legacy.lunarcrush.com/developers/docs> 

| Method         | Description     |
|--------------|-----------|
| **get_assets()** | Details, overall metrics, and time series metrics for one or multiple assets.      |
| **get_market_pairs()** | Provides the exchange information for assets, and the other assets they are being traded for.  |
| **get_market()** | Summary information for all supported assets (Markets page) including 5 recent time series values for some metrics.  |
| **get_global()** | Overall aggregated metrics for all supported assets (top of Markets page).  |
| **get_meta()** | Meta information for all supported assets  |
| **get_exchanges()** | Meta information for all exchanges that we track  |
| **get_exchange()** | Meta information and market pairs for a single exchange that we track  |
| **get_coin_of_the_day()** | The current coin of the day  |
| **get_coin_of_the_day_info()** | Provides the history of the coin of the day on LunarCRUSH when it was last changed, and when each coin was last coin of the day  |
| **get_feeds()** | Social posts, news, and shared links for one or multiple coins.  |
| **get_influencers()** | List of social accounts that have the most influence on different assets based on number of followers, engagements and volume of posts.  |
| **get_influencer()** | Individual influencer details including actual posts.  |

### LC Metrics description
| Metric         | Description     |
|--------------|-----------|
| **GALAXY SCORE** | The Galaxy Score™ indicates how healthy a coin is by looking at combined performance indicators across markets and social engagement. Display the real-time Galaxy Score™ of any coin. |
| **ALT RANK** | AltRank™ measures a coin's performance VS. all other coins that we actively support. In general, it is a unique measurement that combines ALT coin price performance relative to Bitcoin and other social activity indicators across the entire crypto market. A coin can have a high AltRank of 1 even in a bear market situation. |
| **INFLUENCERS** | View Twitter influencer activity and their impact across all coins and tokens. All influencers are measured by the same metrics, which includes followers, replies, favorites, and retweets. Metrics are evaluated across all collected posts during the timeframe selected. Actual influence will vary over time and will depend on user activity. |
| **CANDLESTICK** | The incredibly powerful Candlestick widget takes any data point and compares it to price over a specified timeframe. |
| **WORD CLOUD** | Uncover keywords used throughout collected social content for any coin. The Word Cloud is generated from all recent and available social posts from Twitter and Reddit. It looks at frequency of mentions. All data is segmented by either all coins or specific, individual coins. |
| **SOCIAL FEED** | Display social feeds from multiple sources including Twitter, Reddit, news channels and more all at once. Gain unique insights into what's being talked about in real time. All social feeds have been cleaned with spam removed and can be organized by coin. |

## TWITTER API
| Method         | Description     |
|--------------|-----------|
| **get_user()** | Request user information. |
| **get_all_tweets()** | Request all tweets given a query (Academic Research only). |
| **get_recent_tweets()** | Request recent tweets given a query. |
| **get_all_tweets_count()** | Request all twitter count given a query (Academic Research only). |
| **get_recent_tweets_count()** | Request recent twitter counts given a query. |

## ASYNC TWITTER SCRAPER
Asynchronous Twitter scraper is based on twint project configuration. New parameters have been added to parallelize the scraping process and filter information:
Parameters can be found in twint/config.py

| New parameters | Type     | Description     |
|--------------|-----------|-----------|
| **Users** | *dict* | Dictionary to store the **coins** (keys) and their respective **users** (values) for parallelization purposes. |
| **Queries** | *dict* | Dictionary to store the **coins** (keys) and their respective **queries** (values) for parallelization purposes.|
| **Save_replies** | *bool* | True to store tweet's **replies**. |
| **Save_mentions** | *bool* | True to store the tweets' **mentions**. |
| **Save_meta** | *bool* | True to store **all** the information of the tweets. |
| **Remove_mentions** | *bool* | Remove tweet **mentions**. |

