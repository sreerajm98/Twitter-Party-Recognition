"""
Train several different party classification models. Write the
classifiers as json data to external files (for the testing
module to read).

1) Naive Bayes (Multinomial)
2) Rocchio Text Classifier
3) TextBlob (external library)

Shameek Ray <shameek@umich.edu>
"""


""" IMPORTS """
import sys
import re
import os
import json
from collections import defaultdict
from pprint import pprint
from math import log, log10, sqrt
from textblob import TextBlob
from partycity.training import TRAINING_DIR
from partycity import TOPICS

""" GLOBALS """
TRAINING_DATA_DIR = os.path.join(TRAINING_DIR, 'training_data/')
# TRAINING_DIR =  'rocchio_class_example/'
# TRAINING_DIR =  'naive_class_example/'

OUTPUT_DIR = 'classifiers/'
PARTIES = ['d', 'r']
# List of possible political topics TODO import from package instead

def fileToString(filename):
    document = open(filename)
    document_string = document.read()
    document.close()
    return document_string

def get_default_nb():
    nb = {
        topic: {
            'vocab': defaultdict(int),
            **{ 
                 party: {
                    'tokens': defaultdict(int),
                    'count_words': 0,
                    'count_docs': 0
                } for party in ['d', 'r']
            }
        } for topic in TOPICS
    }
    return nb

def get_default_rocchio():
    rocchio = {
        topic: {
            'vocab': defaultdict(int),
            **{ 
                 party: {
                    'tf': defaultdict(lambda: defaultdict(int)),
                    'df': defaultdict(lambda: defaultdict(int)),
                    "count_docs": 0
                } for party in ['d', 'r']
            }
        } for topic in TOPICS
    }
    return rocchio

def train_nb():
    nb = get_default_nb()
    for topic in TOPICS:
        nb["vocab"] = get_vocabulary(topic)

    for party in PARTIES:
        print(f'Training Naive Bayes for {party}...')
        for filename in os.listdir(TRAINING_DATA_DIR):
            print(f'\tRecording data from {filename}...', end='')
            sys.stdout.flush()
            try:
                topic = get_file_topic(filename)
                if party == filename[0] and topic != "None":
                    nb[topic][party]["count_docs"] += 1
                    for word in fileToString(TRAINING_DATA_DIR + filename).rstrip().split("\n"):
                        nb[topic][party]["tokens"][word] += 1
                        nb[topic][party]["count_words"] += 1
            except KeyError as ke:
                print (party, topic)
            print('Done')
        print(f'Finished Naive Bayes for {party}')

    print(f'Writing Naive Bayes data structure to file...', end='')
    sys.stdout.flush()
    with open(os.path.join(TRAINING_DIR, "nb_model.txt"), "w") as f:
        f.write(json.dumps(nb))     
    print('Done')

def get_vocabulary(topic):
    vocab = set()
    for filename in os.listdir(TRAINING_DATA_DIR):
        if topic in filename:
            for word in fileToString(TRAINING_DATA_DIR + filename).rstrip().split("\n"):
                vocab.add(word)

    vocab_dict = dict.fromkeys(vocab, 0)
    return vocab_dict

def get_naive_probability(nb, word, topic, party):
    try:
        if word not in nb[topic][party]["tokens"]:
            numer = 1
        else:
            numer = nb[topic][party]["tokens"][word] + 1
    except:
        print (word, topic, party)
        
    denom = len(nb["vocab"]) + nb[topic][party]["count_words"]
    ans = float(numer / denom)
    return log10(ans)

def test_nb(nb, query_tokens, topic):
    nb_probs = [0] * len(PARTIES)
    i = 0
    for party in PARTIES:
        for word in query_tokens:
            nb_probs[i] += get_naive_probability(nb, word, topic, party)
        class_cond = float(nb[topic][party]["count_docs"]/len(os.listdir(TRAINING_DATA_DIR)))
        nb_probs[i] += 0 if not class_cond else log10(class_cond)
        i += 1
    # return class with highest probability
    return PARTIES[nb_probs.index(max(nb_probs))]

def compute_tfidf(rocchio, topic, word, doc):
    tfidf = 0.0
    tf = 0.0
    df = 0.0
    idf = 0.0
    N = len(os.listdir(TRAINING_DATA_DIR))
    party = 'd' if doc[0] == 'd' else 'r' 
    if rocchio[topic][party]["df"][word]:
        tf = rocchio[topic][party]["tf"][doc][word]
        df = len(rocchio[topic][party]["df"][word])
        idf = log10(float(N/df))
    else:
        tf = 0
        idf = 0
    tfidf = float(tf * idf)
    return tfidf

def cosine_similarity(a, b):
    dot_product = 0
    a_length = 0
    b_length = 0
    
    for word, score in a.items():
        a_length += score * score
    a_length = sqrt(a_length)
    
    for word, score in b.items():
        b_length += score * score
    b_length = sqrt(b_length)

    for word, score in a.items():
        dot_product += (a[word] * b[word])
    
    return 0 if not a_length * b_length else float(dot_product/float(a_length * b_length))

def get_file_topic(filename):
    for topic in TOPICS:
        if topic in filename:
            return topic
    return "None"
 
def train_rocchio():
    rocchio = get_default_rocchio()
    for party in PARTIES:
        print(f'Training Rocchio for {party}...')
        for filename in os.listdir(TRAINING_DATA_DIR):
            print(f'\tRecording data from {filename}...', end='')
            sys.stdout.flush()
            topic = get_file_topic(filename)
            if topic != "None":
                if party in filename:
                    words = fileToString(TRAINING_DATA_DIR + filename).rstrip().split("\n")
                    for word in words:
                        rocchio[topic]["vocab"][word] = 0
                    for word in words:
                        if word not in rocchio[topic][party]:
                            rocchio[topic][party]["df"][word][filename] = 0
                        rocchio[topic][party]["df"][word][filename] = 1                        
                        rocchio[topic][party]["tf"][filename][word] += 1
            print('Done')

    vectors = {
        topic: {
            party: {
                doc: {
                    word: 0.0 for word in rocchio[topic]["vocab"].keys()
                } for doc in get_topic_docs(party)
            } for party in PARTIES
        } for topic in TOPICS
    }

    print(f'Computing weights from recorded data...', end='')
    sys.stdout.flush()
    for topic in TOPICS: 
        for party in PARTIES:
            for doc in get_topic_docs(party):
                for word in rocchio[topic]["vocab"].keys():
                    vectors[topic][party][doc][word] = compute_tfidf(rocchio, topic, word, doc)
    print('Done')
            
    print(f'Creating prototype vectors...', end='')
    sys.stdout.flush()
    prototypes = {}

    for topic in TOPICS: 
        prototypes[topic] = {party: defaultdict(int) for party in PARTIES}
        for party in PARTIES:
            for doc in get_topic_docs(party):
                for word in rocchio[topic]["vocab"].keys():
                    try:
                        prototypes[topic][party][word] += vectors[topic][party][doc][word]
                    except KeyError:
                        print (topic, party, doc, word)
    print('Done')
                        
    print(f'Writing Rocchio data structure to file...', end='')
    sys.stdout.flush()
    with open(os.path.join(TRAINING_DIR, "rocchio_model.txt"), "w") as f:
        f.write(json.dumps(rocchio))
    print('Done')

    print(f'Writing Rocchio prototypes to file...', end='')
    sys.stdout.flush()
    with open(os.path.join(TRAINING_DIR, "rocchio_prototypes.txt"), "w") as f:
        f.write(json.dumps(prototypes))        
    print('Done')

def get_query_vector(rocchio, query, topic):
    q_rocchio = {
        'tf': defaultdict(int),
        'df': defaultdict(int),
    }
    unique_words = set(query)
    unique_words_copy = list(unique_words)
    for party in PARTIES:
        for word in unique_words_copy:
            if word not in rocchio[topic][party]["df"] and word in unique_words:
                unique_words.remove(word)

    for word in unique_words:
        for party in PARTIES:
            if word in rocchio[topic][party]["df"]:
                for doc in rocchio[topic][party]["df"][word]:
                    q_rocchio["df"][word] += rocchio[topic][party]["df"][word][doc] 
                for doc in rocchio[topic][party]["tf"]:
                    try:
                        if word not in rocchio[topic][party]["tf"][doc]:
                            rocchio[topic][party]["tf"][doc][word] = 0
                        q_rocchio["tf"][word] += rocchio[topic][party]["tf"][doc][word] 
                    except KeyError:
                        print ("NOT FOUND", word, doc)

    query_prototype = defaultdict(float)

    N = len(os.listdir(TRAINING_DATA_DIR))
    for word in unique_words:
        tf = q_rocchio["tf"][word]
        df = q_rocchio["df"][word]
        idf = log10(N / df)
        query_prototype[word] = float(tf * idf)

    return query_prototype

def get_topic_docs(topic):
    docs = []
    for doc in os.listdir(TRAINING_DATA_DIR):
        if topic in doc[0]:
            docs.append(doc)

    return docs

def test_rocchio(rocchio, train_prototypes, query_vector, topic):
    query_protytpe = get_query_vector(rocchio, query_vector, topic)
    max_party = ""
    max_party_score = -1000000
    for party in PARTIES:
        score = cosine_similarity(train_prototypes[topic][party], query_protytpe)
        if score > max_party_score:
            max_party_score = score
            max_party = party
    return max_party

def run_rocchio(test_vector, test_topic, rocchio, prototypes):
    # train_rocchio()
    # rocchio = get_default_rocchio()
    # prototypes = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    # with open(os.path.join(TRAINING_DIR, "rocchio_model.txt")) as rm:
    #     rocchio = json.load(rm)
    # with open(os.path.join(TRAINING_DIR, "rocchio_prototypes.txt")) as rp:
    #     prototypes = json.load(rp)
    return test_rocchio(rocchio, prototypes, test_vector, test_topic)

def run_nb(test_vector, test_topic):
    # train_nb()
    with open(os.path.join(TRAINING_DIR, "nb_model.txt")) as model:
        nb = json.load(model)
    return test_nb(nb, test_vector, test_topic)

def train_text_blob(printOutput=True):
    tb = {
        topic: {
            party: {
                "words": ""
            } for party in PARTIES
        } for topic in TOPICS
    }

    for filename in os.listdir(TRAINING_DATA_DIR):
        if printOutput:
            print(f'Training TextBlob from {filename}...', end='')
        sys.stdout.flush()
        topic = get_file_topic(filename)
        if topic != "None":
            party = 'd' if filename[0] == 'd' else 'r'
            document_words = fileToString(TRAINING_DATA_DIR + filename).rstrip().split("\n")
            tb[topic][party]["words"] += " ".join(str(word) for word in document_words)
        if printOutput:
            print('Done')

    tb_scores = {
        party: {
            topic: {

            } for topic in TOPICS
        } for party in PARTIES        
    }

    if printOutput:
        print(f'Calculating TextBlob scores...', end='')
    for topic in TOPICS:
        for party in tb[topic].keys(): 
            for topic in tb.keys():
                tb_scores[party][topic] = TextBlob(tb[topic][party]["words"]).sentiment.polarity
    if printOutput:
        print('Done')

    if printOutput:
        print(f'Writing TextBlob results to file...', end='')
    sys.stdout.flush()
    with open(os.path.join(TRAINING_DIR, "textBlob_train.txt"), "w") as f:
        f.write(json.dumps(tb_scores))        
    if printOutput:
        print('Done')
    
    return tb_scores
def main():
    # run_rocchio(["gun", "control"], "gun_control")
    # run_nb(["gun", "control"], "gun_control")
    train_nb()
    train_rocchio()
if __name__ == "__main__":
    main()

# for each topic t
    # for each party p 
    #   string  
    #   for each document in topic
    #       string += all words in document
    #   blob = TextBlob(string)


# data model
#party_details[party][topic] = blob.sentiment.polarity
