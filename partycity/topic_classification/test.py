"""
Naive Bayes Topic Classification evaluation functions.

Brian Sutherland <bsuth@umich.edu>
"""


""" IMPORTS """
import os
import json
import math
from operator import itemgetter
from collections import defaultdict
from partycity import TOPICS
from partycity.topic_classification import TOPIC_DIR


""" NAIVE BAYES CLASSIFIER """
def get_naive_bayes():
    # Read in Naive Bayes file
    nb_file = os.path.join(TOPIC_DIR, 'naive_bayes.txt')
    with open(nb_file, 'r') as fin:
        nb = defaultdict(int, json.loads(fin.read()))
    return nb


def naive_bayes(nb, tokens):
    # Class score variables
    scores = {
        topic: (0 if not nb[topic]['prob'] else math.log(nb[topic]['prob'], 2)) 
            for topic in TOPICS
    }

    # Vocab size
    vocab_size = len({t for topic in nb.values() for t in topic['tokens']})

    # Calculate class scores
    for token in tokens:
        for topic in scores.keys():
            topic_size = sum(nb[topic]['tokens'].values())
            if token in nb[topic]['tokens']:
                num = nb[topic]['tokens'][token]  + 1
                denom = topic_size + vocab_size
                scores[topic] += math.log(num / denom, 2)


    # Filter zero scores
    scores = {topic: score for topic, score in scores.items() if score != 0}

    # Check for empty scores
    if not scores:
        return 'None'

    # Sort scores dictionary into tuples of (topic, score)
    scores = sorted(scores.items(), key = itemgetter(1))
    top_score = scores[0][1]
    runner_up = scores[1][1]

    # Check for clear winner
    if top_score / runner_up < 1.2 or top_score > -60:
        return 'None'

    return scores[0][0]
