"""
Read in scraped tweets from different states, preprocess the tweets,
determine party of the tweet, and determine political affiliation of
each state. Also print out total accuracy using results from the 2016
election as the correct standard.

Rodney Shibu <rodneyss@umich.edu>
"""


from partycity import TOPICS
from partycity.testing import TESTING_DIR
from partycity.testing.sentiment_analysis import sentiment
from partycity.training.train import run_rocchio
from partycity.training.train import run_nb
from partycity.topic_classification.preprocess import ppTweet
from partycity.training.train import get_default_rocchio
from partycity.training import TRAINING_DIR
from collections import defaultdict
import sys
import os
import json

def accuracy(test, correct):
    counter = 0
    for state, party in test.items():
        if party == correct[state]:
            counter += 1
    return counter / len(test)

def run(tweets, type):
        results = {}

        if type == "rocchio":
            with open(os.path.join(TRAINING_DIR, "rocchio_model.txt")) as rm:
                rocchio = json.load(rm)
            with open(os.path.join(TRAINING_DIR, "rocchio_prototypes.txt")) as rp:
                prototypes = json.load(rp)

        for state in tweets:
                num_r = 0
                num_d = 0
                for tweet in tweets[state]:
                        tweet_arr = tweet.split(" ")
                        topic = tweet_arr[0].replace("'","")
                        tweet_arr.pop(0)
                        tweet_arr.pop(0)
                        tweet = ppTweet(' '.join(tweet_arr))
                        if type == "rocchio":
                                rocchio = get_default_rocchio()
                                prototypes = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
                                
                                party = run_rocchio(tweet.split(" "), topic, rocchio, prototypes)
                        elif type == "nb": 
                                party = run_nb(tweet.split(" "), topic)
                        if party == "r":
                                num_r += 1
                        else:
                                num_d += 1

                if num_d > num_r:
                        results[state] = "d"
                else:
                        results[state] = "r"
        return results

def get_results(filename):
        #Format: tweets = {'New York': ['@user1 this is a tweet about economy!', '@user3 this is anotha tweet about economy', '@user2 this is a tweet about abortion']}}
        tweets = {}

        #Results of analysis
        sentiment_results = {}
        rocchio_results = {}
        nb_results = {}

        with open(os.path.join(TESTING_DIR, 'correct.results'), 'r') as fin:
            correct_results = json.loads(fin.read())

        #Read in data scraped using Twitter API
        next_line = ""
        state = ""
        tweet = ""
        with open(os.path.join(TESTING_DIR, filename), 'r') as tweet_file:
                for line in tweet_file:
                        if "##############################" in line and next_line != "state":
                                next_line = "state"
                        elif "---------------------------" in line:
                                next_line = "tweet"
                        elif next_line == "state" and "##############################" not in line:
                                state = line.split(":")[0]
                        elif next_line == "tweet":
                                tweet = line
                                if state not in tweets:
                                        tweets[state] = []
                                tweets[state].append(tweet)
                                next_line = ""
                        elif next_line == "":
                                new_tweet = tweets[state][-1] + line
                                tweets[state] = tweets[state][:-1]
                                tweets[state].append(new_tweet)
                        elif next_line != "state":
                                next_line = ""

        #This is where we do sentiment analysis
        print('\nRunning analysis using sentiment model...')
        sys.stdout.flush()
        sentiment_results = sentiment(tweets)
        print(sentiment_results)
        print('Accuracy:', accuracy(sentiment_results, correct_results))
        print('Finished analysis with sentiment model\n')

        #This is where we do rocchio classification
        print('Starting analysis using Rocchio classification...')
        sys.stdout.flush()
        rocchio_results = run(tweets, "rocchio")
        print(rocchio_results)
        print('Accuracy:', accuracy(rocchio_results, correct_results))
        print('Finished analysis with Rocchio classification\n')

        #This is where we do bayes classification
        print('Starting analysis using Naive Bayes...')
        sys.stdout.flush()
        nb_results = run(tweets, "nb")
        print(nb_results)
        print('Accuracy:', accuracy(nb_results, correct_results))
        print('Finished analysis with Naive Bayes\n')
