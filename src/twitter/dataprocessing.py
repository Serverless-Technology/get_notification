import tweepy
import json

from config import *

# Twitter API credentials
consumer_key = TWITTER_CONSUMER_KEY
consumer_secret = TWITTER_CONSUMER_SECRET
access_token = TWITTER_ACCESS_TOKEN
access_token_secret = TWITTER_ACCESS_TOKEN_SECRET

# Initialize the Twitter API client
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
api = tweepy.API(auth)

# Keywords or hashtags to search for research conferences
keywords = ['#researchconference', '#academicconference', '#scienceevent']

# Fetch tweets based on keywords
def fetch_tweets():
    tweets = []
    for keyword in keywords:
        fetched_tweets = api.search_tweets(q=keyword, count=10)
        tweets.extend(fetched_tweets)
    return tweets

# Process and filter tweets based on relevance
def process_tweets(tweets):
    relevant_tweets = []
    for tweet in tweets:
        text = tweet.text.lower()
        # You can add more specific keyword checks or NLP techniques here
        if any(keyword in text for keyword in keywords):
            relevant_tweets.append(tweet._json)  # Store the JSON representation of the tweet
    return relevant_tweets

# Save relevant tweets to a JSON file
def save_to_json(tweets):
    with open('relevant_tweets.json', 'w', encoding='utf-8') as json_file:
        json.dump(tweets, json_file, ensure_ascii=False, indent=4)

# Main function
def main():
    tweets = fetch_tweets()
    relevant_tweets = process_tweets(tweets)
    save_to_json(relevant_tweets)

if __name__ == "__main__":
    main()
