import tweepy
from textblob import TextBlob
import preprocessor
import statistics
from typing import List
import preprocessor as p

# Below values helps you access the twitter api, you can get these values by creating
# a developers account on twitter
# Don't share these values to anyone, as they can be misused to access your 
# twitter account

consumer_key = '#############################################'		#your keys here
consumer_secret = '#######################################'
Access_token = '###########################################'
Access_token_secret = '#######################################'

authenticate = tweepy.OAuthHandler(consumer_key,consumer_secret)
authenticate.set_access_token(Access_token,Access_token_secret)
api = tweepy.API(authenticate)

# Function to get tweets from Twitter related to given keyword

def get_tweets(keyword: str) -> List[str]:

    all_tweets = []

    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode='extended', lang='en').items(100):
        all_tweets.append(tweet.full_text)

    return all_tweets

# Function to clean received tweets (eliminating hashtags, mentions, emogis etc.)

def clean_tweets(all_tweets: List[str]) -> List[str]:

    tweets_clean = []

    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    return tweets_clean

# Function to calculate sentiment score of tweets individually and store in a list

def get_sentiment(all_tweets: List[str]) -> List[float]:

    sentiment_scores = []

    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores

# Function to calculate average sentiment score from list of sentiment scores

def generate_average_sentiment_score(keyword: str) -> int:

    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)
    average_score = statistics.mean(sentiment_scores)

    return average_score

if __name__ == '__main__':

    while(True):

        print('###########################################################################################')
        print('\nwhat does the world prefer:\n')
        first_thing = input()       # input name( like Chai)
        print('--or--')
        second_thing = input()      # input name of the opponent( like Coffee)
        print('\n')

        first_score = generate_average_sentiment_score(first_thing)
        second_score = generate_average_sentiment_score(second_thing)

        # The result will be announced in a given below format
        # (don't take it personally, it's only based on comparison of 10 tweets ;) )

        if (first_score > second_score):

            print(f'The humanity prefers {first_thing} over {second_thing}')

        if (first_score < second_score):

            print(f'The humanity prefers {second_thing} over {first_thing}')

        if (first_score == second_score):

            print(f'Both {first_thing} and {second_thing} are equally preferred by humanity, it\'s a tie')

        print()




