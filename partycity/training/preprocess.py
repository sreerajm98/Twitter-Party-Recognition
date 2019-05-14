"""
Scrape presidential debates and preprocess text. Write training
data to output folders in the format

{party}_{topic}_{debate#}

with party either 'r' or 'd'.

Brian Sutherland <bsuth@umich.edu> (Tokenization)
Nikita Badhwar <nbadhwar@umich.edu>
"""


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

# List to contain month words. This is
# used in tokenizeDate()
MONTH_WORDS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

STOPWORDS = []


""" IMPORTS """
import sys
import requests
import os
import re
import operator
import math
import glob
from nltk import PorterStemmer
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from partycity import TOPICS
from partycity.topic_classification.test import naive_bayes, get_naive_bayes
from partycity.training import TRAINING_DIR



""" HELPER FUNCTIONS """
# Tokenizes the text
def tokenizeText(text):
    words = text.split()
    tokens = []
    i = 0

    # Use a while loop here rather than a for loop
    # so we may manipulate i. This is useful when
    # we have to join words together into a single
    # token, such as dates.
    while i < len(words):
        word = words[i]

        # Tokenize periods
        word = re.sub("\.", "", word)
        if not word:
            i += 1
            continue

        # Tokenize periods
        # Periods appear as whole words in the docs,
        # so only tokenize these instances. Otherwise,
        # leave periods in acronyms, abbreviations, etc.
        if word == ".":
            i += 1
            continue

        # Tokenize quotes
        # Remove quotes -> unnecessary and interferes
        # with apostrophe tokenization
        if word[0] == "'" and word[-1] == "'":
            word = word[1:-1]
        elif word[0] == '"' and word[-1] == '"':
            word = word[1:-1]

        # Tokenize commas
        # Only tokenize comma if it does not look
        # like a number
        if not re.match("([0-9]+,[0-9]+)+", word):
            word = re.sub(",", "", word)

        # Tokenize hyphen
        # Only tokenize hyphen if it occurs at the
        # end of a word, otherwise it is most likely
        # a phrase or date.
        # if word[-1] == '-':
        #     if i+1 < len(words):
        #         word = word[:-1] + words[i+1]
        #         i += 1
        #     else:
        #         word = word[:-1]

        # Tokenize apostrophes
        if "'" in word:
            tokens += tokenizeApost(word)
            i += 1
            continue

        # Tokenize dates
        # Merge phrases of the following forms into
        # a single token:
        #
        # Month Date
        # Month Date, Year
        # Month Year
        if word in MONTH_WORDS:
            # Check if next word starts with a day
            # (allow ending comma for dates like January 31, 2019)
            if i+1 < len(words) and re.match("[0-9]+,*", words[i+1]):
                word += " " + words[i+1]
                i += 1

                # Check if the next next word is a year
                # NOTE: We only check for years with 4 digits,
                # as it is uncommon to see years with 5+ digits
                # and extremely old dates are generally written
                # without the day. (Ex. 300 AD)
                if i+1 < len(words) and re.match("[1-9]\d{3}", words[i+1]):
                    word += " " + words[i+1]
                    i += 1

            # Check if next word starts with a year
            if i+1 < len(words) and re.match("[1-9]\d{3},*", words[i+1]):
                # Remove commas if they trail the year
                # Ex: "It was January 2019, the harshest winter of all time."
                word += " " + re.sub(",", "", words[i+1])
                i += 1

        # Add token and increment i
        tokens.append(word)
        i += 1

    return tokens


# Handle apostrophes
def tokenizeApost(word):
    # check irregular apostrophes
    if word in APOST_DICT:
        return [ APOST_DICT[word] ]

    # check 3 letter apostrophes
    wordEnd = word[-3:]
    if wordEnd == "n't":
        return [ word[:-3], "not" ]
    elif wordEnd == "'re":
        return [ word[:-3], "are" ]
    elif wordEnd == "'ve":
        return [ word[:-3], "have" ]
    elif wordEnd == "'ll":
        return [ word[:-3], "will" ]

    # check 2 letter apostrophes
        if word[:-2] in QUESTION_WORDS:
            return [ word[:-2], "did" ]
        else:
            # Default to 'would'
            # The cases between 'would' and 'had'
            # are near impossible to tell apart w/o
            # the tense of the verb, so we simply
            # default to 'would'.
            return [ word[:-2], "would" ]
    elif wordEnd == "'s":
        # The cases between the possessive s and
        # the contraction of 'is' is very difficult
        # to tell apart without context, so we
        # default to possessive only when the word
        # is a proper noun.
        if ord(word[0]) > 64 and ord(word[0]) < 91:
            return [ word[:-2], "'s" ]
        return [ word[:-2], "is" ]
    else:
        return [ re.sub("'", "", word) ]


# Removes all STOPWORDS
def removeStopwords(tokens):
    return [ t for t in tokens if t not in STOPWORDS ]


# Stems the words
def stemWords(tokens):
    return [ PorterStemmer().stem(t) for t in tokens ]


#file of urls
#webscrape
#parse
#preprocess
#list: speaker, content, id

class trainingInformation:
    def __init__(x, content, speaker):
        x.content = content
        x.speaker = speaker

def gen_training_data():
    print('Clearing old training data...', end='')
    sys.stdout.flush()
    for f in glob.glob(os.path.join(TRAINING_DIR, 'training_data/*')):
        os.remove(f)
    print('Done')
    moderators = [
    "WALLACE:",
    "COOPER:",
    "RADDATZ:",
    "HOLT:",
    "QUIJANO:",
    "BASH:",
    "RAMOS:",
    "SALINAS:",
    "IFILL:",
    "WOODRUFF:",
    "TODD:",
    "MADDOW:",
    "CUOMO:",
    "MITCHElL:",
    "TAPPER:",
    "BASH:",
    "BAIER:",
    "KELLY:",
    "DICKERSON:",
    "MUIR:",
    "BARTIROMO:",
    "CAVUTO:"
    ]
    speakers = [
    "CLINTON:",
    "TRUMP:",
    "SANDERS:",
    "O'MALLEY",
    "CARSON:",
    "CRUZ:",
    "RUBIO:",
    "CLINTON:",
    "KASICH:"
    ]

    helper = []
    listOfInformation = []


    f = open(os.path.join(TRAINING_DIR, "stopwords"), 'r')
    STOPWORDS = re.split('\s+', f.read())
    f.close()

    f = open(os.path.join(TRAINING_DIR, "DebateURLS.txt"), 'r')
    files  = f.readlines()
    nb = get_naive_bayes()
    count = 0

    for i in range(0, len(files)):
        print('Training on ' + files[i].strip("\n") + ':')
        print(f'\tScraping...', end='')
        sys.stdout.flush()
        r = requests.get(files[i])
        soup = BeautifulSoup(r.text, "html.parser")
        temp = []
        count += 1
        print('Done')
        print(f'\tPreprocessing...', end='')
        sys.stdout.flush()
        for node in soup.findAll('p'):
            node = ''.join(node.findAll(text = True))
            helper = node.split()
            if(len(helper) > 0):
                if(helper[0] in moderators or helper[0] in speakers):
                    topic = (naive_bayes(nb, temp))
                    currentSpeaker = helper[0]
                    if(currentSpeaker == "CLINTON:" or currentSpeaker == "SANDERS:" or currentSpeaker == "O'MALLEY:"):
                        val = "d"
                        tempstring =  val + "_" + str(topic) + "_" + str(count)
                        with open(os.path.join(TRAINING_DIR, f'training_data/{tempstring}'), 'a') as fin:
                            for i in range(0, len(temp)):
                                fin.write(temp[i] + "\n")
                    elif(currentSpeaker != "CLINTON:" and currentSpeaker != "SANDERS:" and currentSpeaker != "O'MALLEY:"):
                        if(currentSpeaker in speakers):
                            val = "r"
                            tempstring =  val + "_" + str(topic) + "_" + str(count)
                            with open(os.path.join(TRAINING_DIR, f'training_data/{tempstring}'), 'a') as fin:
                                for i in range(0, len(temp)):
                                    fin.write(temp[i] + "\n")
                    del temp[:]
                    node = node.replace(helper[0], " ")
                    x = tokenizeText(node)
                    x = removeStopwords(x)
                    x = stemWords(x)
                    for token in x:
                        temp.append(token)
                else:
                    x = tokenizeText(node)
                    x = removeStopwords(x)
                    x = stemWords(x)
                    for token in x:
                        temp.append(token)
        print('Done')
