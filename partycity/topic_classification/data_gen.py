"""
Generate 
"""

""" IMPORTS """
import sys
import os
import tweepy
from partycity import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from partycity import KEYWORDS
from partycity.topic_classification import TRAINING_DIR
from partycity.topic_classification.preprocess import ppTweet

def data_gen():
    # Setup connection
    print('Setting up connection with Twitter...', end='')
    sys.stdout.flush()
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    print('Done')


    # Scrape Twitter for tweets to train on
    for topic, related in KEYWORDS.items():
        print(f'Scraping tweets for {topic}...')
        sys.stdout.flush()

        output_file = os.path.join(TRAINING_DIR, f'{topic}.txt')
        with open(output_file, 'a') as fout:
            # Clear the file
            # UNCOMMENT ONLY IF YOU WANT TO RESET THE TRAINING DATA
            # fout.truncate(0)

            # Scrape twitter
            tweets = []
            for keyword in related:
                print(f'\tUsing keyword {keyword} to filter tweets...', end='')
                sys.stdout.flush()

                data_count = 25 if len(related) == 4 else 100
                tweets += api.search(
                    q=f'{keyword}-filter:retweets',
                    count=data_count, 
                    show_user=False, 
                    tweet_mode='extended'
                )
                print('Done')

            # Preprocess tweets
            print(f'\tPreprocessing tweets for {topic}...', end='')
            sys.stdout.flush()
            tweets = [ppTweet(tweet.full_text) for tweet in tweets]
            print('Done')

            # Remove non-ascii characters and write to file
            print(f'\tWriting tweets to file...', end='')
            for tweet in tweets:
                fout.write(tweet + "\n")
            print('Done')
            print(f'Added 100 new tweets for {topic}')
