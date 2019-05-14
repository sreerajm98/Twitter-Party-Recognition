"""
Train Naive Bayes model for topic classification.
Note: To filter noise, we only keep the highest
100 term probabilities per topic.

Brian Sutherland <bsuth@umich.edu>
"""


""" IMPORTS """
import sys
import re
import os
import json
import math
import glob
from collections import defaultdict
from operator import itemgetter
from partycity import TOPICS
from partycity.topic_classification import TOPIC_DIR
from partycity.topic_classification import TRAINING_DIR


""" HELPER FUNCTIONS """
# Returns the topic of the text within the file.
# Valid return values are anything within TOPICS (global)
def get_topic(file):
    filename = os.path.basename(file)
    return re.match(r"([a-z, _]+)\.txt", filename).group(1)


""" NAIVE BAYES CLASSIFIER """
def create_naive_bayes():
    # Initialize Naive Bayes data structure
    print('Instantiating Naive Bayes data structure...', end='')
    sys.stdout.flush()
    nb = {
        topic: {
            'prob': 0,
            'tokens': defaultdict(int),
        } for topic in TOPICS
    }
    print('Done')

    # Record data from training files
    print('Recording tokens and frequencies...')
    sys.stdout.flush()
    for file in glob.glob(os.path.join(TRAINING_DIR, '*.txt')):
        topic = get_topic(file)
        print(f'\tRecording data for {topic}...', end='')
        sys.stdout.flush()
        _class = nb[topic]
        with open(file, 'r') as fin:
            for line in fin:
                _class['prob'] += 1
                for token in line.split():
                    _class['tokens'][token] += 1
        print('Done')
    print('Finished recording tokens and frequencies')

    # Get total number of docs and update probabilities
    print('Calculating topic probabilities...', end='')
    sys.stdout.flush()
    total_docs = sum([topic['prob'] for topic in nb.values()])
    for topic in nb.values():
        topic['prob'] /= total_docs
    print('Done')

    # Filter for top tokens
    print('Filtering data structure for most common tokens...', end='')
    sys.stdout.flush()
    for topic in nb.values():
        # Sort by tf
        topic['tokens'] = sorted(
            topic['tokens'].items(), 
            key=itemgetter(1), 
            reverse=True
        )
        # Take top 100 results (or num tokens, whichever is smaller)
        topic['tokens'] = dict(topic['tokens'][0:min(60, len(topic['tokens']))])
    print('Done')

    # Write to output file
    print('Writing data structure to file as JSON...', end='')
    sys.stdout.flush()
    output_file = os.path.join(TOPIC_DIR, 'naive_bayes.txt')
    with open(output_file, 'w') as fout:
        fout.write(json.dumps(nb))
    print('Done')
