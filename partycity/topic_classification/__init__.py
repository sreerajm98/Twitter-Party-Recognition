"""
Python module for the Topic Classifier.
----------------------------------------------------
This is where we specify all module variables and outward facing 
functions, i.e. functions that we may call from __main.py__ in the 
partycity package root folder.

Brian Sutherland <bsuth@umich.edu>
"""

import os
TOPIC_DIR = os.path.dirname(__file__)
TRAINING_DIR = os.path.join(TOPIC_DIR, 'training_data/')

from partycity.topic_classification.train import create_naive_bayes
from partycity.topic_classification.data_gen import data_gen
from partycity.topic_classification.preprocess import ppTweet
