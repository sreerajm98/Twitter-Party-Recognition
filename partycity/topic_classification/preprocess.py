"""
Preprocess tweets before adding them to the training data.
This includes tokenization, stopword removal, and stemming.
Note that Twitter @'s are tokenized out. Hashtags are kept
in but the '#' character is removed. URL's are also removed.

Brian Sutherland <bsuth@umich.edu>
"""


""" IMPORTS """
import sys
import os
import re
import math
import json
import glob
from nltk import PorterStemmer
from partycity import TOPICS
from partycity.topic_classification import TOPIC_DIR


""" GLOBALS """
# Dictionary to contain some of the 
# irregular apostrophe mappings
APOST_DICT = {
    "can't": "can not",
    "shan't": "shall not",
    "won't": "will not",
    "'em": "them",
    "I'm": "I am",
    "let's": "let us",
    "o'": "of",
    "o'clock": "o'clock",
    "'twas": "it was",
    "y'all": "you all",
}

# List to contain question words.
# This is useful when resolving words 
# ending with 'd in tokenizationApost(),
# as question words will always map 'd
# to 'did'
QUESTION_WORDS = [ 
    "what", 
    "when", 
    "how", 
    "where", 
    "who", 
    "why" 
]

# Read in stopwords
with open(os.path.join(TOPIC_DIR, 'stopwords'), 'r') as fin:
    STOPWORDS = fin.read().split()


""" HELPER FUNCTIONS """
# Tokenizes the text
def tokenize(text):
    # List of tokens
    tokens = []

    # Split text by whitespace and lowercase everything, then tokenize
    for token in [token.lower() for token in text.split()]:
        # Remove @'s and urls
        if token[0] == '@' or token[:4] == 'http':
            continue

        # Remove periods unless its a number
        if not re.match("([0-9]+.[0-9]+)+", token):
            token = re.sub("\.", "", token)

        # Remove comma unless it is a number
        if not re.match("([0-9]+,[0-9]+)+", token):
            token = re.sub(",", "", token)

        # Remove hashtags, question marks, and exclamation marks
        token = re.sub("#", "", token)
        token = re.sub("\?", "", token)
        token = re.sub("!", "", token)

        # Check empty token
        if not token:
            continue

        # Remove quotes
        if token[0] == "'" and token[-1] == "'":
            token = re.sub("'", "", token)

        # Check empty token
        if not token:
            continue

        if token[0] == '"' and token[-1] == '"':
            token = re.sub('"', "", token)

        # Tokenize apostrophes
        if "'" in token:
            tokens += tokenizeApost(token)
            continue

        # Add to token list
        tokens.append(token)

    # Return tokens
    return tokens


# Handle apostrophes
def tokenizeApost(token):
    # check irregular apostrophes
    if token in APOST_DICT:
        return [ APOST_DICT[token] ]

    # check 3 letter apostrophes
    tokenEnd = token[-3:]
    if tokenEnd == "n't":
        return [ token[:-3], "not" ]
    elif tokenEnd == "'re":
        return [ token[:-3], "are" ]
    elif tokenEnd == "'ve":
        return [ token[:-3], "have" ]
    elif tokenEnd == "'ll":
        return [ token[:-3], "will" ]

    # check 2 letter apostrophes
        if token[:-2] in QUESTION_WORDS:
            return [ token[:-2], "did" ]
        else:
            # Default to 'would'
            # The cases between 'would' and 'had'
            # are near impossible to tell apart w/o
            # the tense of the verb, so we simply
            # default to 'would'.
            return [ token[:-2], "would" ]

    elif tokenEnd == "'s":
        # The cases between the possessive s and
        # the contraction of 'is' is very difficult
        # to tell apart without context, so we
        # default to possessive only when the token
        # is a proper noun.
        if ord(token[0]) > 64 and ord(token[0]) < 91:
            return [ token[:-2], "'s" ]
        return [ token[:-2], "is" ]

    # If none of the above cases are matched, simply
    # remove the apostrophe
    return [ re.sub("'", "", token) ]


# Removes all STOPWORDS
def rmStopWrds(tokens):
    return [ t for t in tokens if t not in STOPWORDS ]


# Stems the words
def stem(tokens):
    return [ PorterStemmer().stem(t) for t in tokens ]


def ppTweet(tweet):
    # Remove non-ascii characters
    tweet = tweet.encode('ascii', 'ignore').decode('ascii')
    return ' '.join(stem(rmStopWrds(tokenize(tweet))))


# Preprocess articles
def preprocess():
    # Output directory
    output_dir = os.path.join(TOPIC_DIR, 'training_data/')

    # Clear output files
    for topic in TOPICS:
        with open(f'{output_dir}/{topic}.txt', 'a') as fout:
            fout.truncate(0)

    # Preprocess all data files
    for file in glob.glob(os.path.join(TOPIC_DIR, 'raw_data/*.txt')):
        topic_file = os.path.basename(file)
        with open(file, 'r') as fin:
            for line in fin:
                with open(f'{output_dir}/{topic_file}', 'a') as fout:
                    text = ppTweet(line)
                    if text:
                        fout.write(text + '\n')
