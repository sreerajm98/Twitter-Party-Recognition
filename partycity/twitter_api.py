from __init__ import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_SECRET, ACCESS_TOKEN
from twython import Twython 
import json
import pandas as pd

def build_credentials():
    credentials = {}
    credentials['CONSUMER_KEY'] = CONSUMER_KEY
    credentials['CONSUMER_SECRET'] = CONSUMER_SECRET
    credentials['ACCESS_TOKEN'] = ACCESS_TOKEN
    credentials['ACCESS_SECRET'] = ACCESS_SECRET

    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)

def search_tweets():
    # Load credentials from json file
    with open("twitter_credentials.json", "r") as file:  
        creds = json.load(file)

    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

    # Create our query
    query = {'q': 'learn python',  
            'result_type': 'popular',
            'count': 10,
            'lang': 'en',
            }

    # Search tweets
    dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}  
    for status in python_tweets.search(**query)['statuses']:  
        dict_['user'].append(status['user']['screen_name'])
        dict_['date'].append(status['created_at'])
        dict_['text'].append(status['text'])
        dict_['favorite_count'].append(status['favorite_count'])

    # Structure data in a pandas DataFrame for easier manipulation
    df = pd.DataFrame(dict_)  
    df.sort_values(by='favorite_count', inplace=True, ascending=False)  
    print (df.head(5))

def state_scraper():
    all_tweets = {}
    

def main():
    build_credentials()
    search_tweets()

if __name__ == "__main__":
    main()     
