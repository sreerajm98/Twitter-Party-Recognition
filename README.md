# PartyCity
PartyCity is a Twitter party recognition algorithm that attempts to predict a state's political stance based off of tweets from users within that state.

## Table of Contents
* [Introduction](#introduction)
* [Running the Project](#running-the-project)
* [Topic Classifier Module](#topic-classifier-module)
* [Training Module](#training-module)
* [Testing Module](#testing-module)
* [Contributors](#contributors)


## Introduction
PartyCity is a Twitter party recognition algorithm that attempts to predict a state's political stance based off of tweets from users within that state. The algorithm is mainly split into three modules: [topic classification](#topic-classifier-module), [training](#training-module) and [testing](#testing-module). More information on each of these modules can be found below. 

In order to make our algorithm more accurate, we create separate classifiers for several political "topics". For example, if a tweet is determined to be about 'Education', then we will use classifiers built for Liberal: Education vs Conservative: Education rather than a generalized Liberal vs Conservative classifier. To choose these topics, we looked at the most important issues among voters for the 2016 Presidential Election using data from [Pew Research Center](https://www.people-press.org/2016/07/07/4-top-voting-issues-in-2016-election/). It should be noted that some of these topics were not included, due to some topics becoming irrelevant in current day politics (for example, Supreme Court Appointments).


## Running the Project
First, you'll need to clone the repo and install partycity as a python package.
### In addition you would also need to apply for Twitter developer API which includes ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_SECRET, and CONSUMER_KEY which needs to be added to the required spots in this project.
```
git clone https://github.com/sreerajm98/Twitter-Party-Recognition.git
cd partycity
pip3 install -e .
```
If you don't want to install partycity to your root system, you can also use a virtual environment (after `cd partycity`):
```
python3 -m venv env
source .env/bin/activate # this may vary based on your shell
pip install -e .
```
Note that if you install using a virtual environment, then you will have to rerun `source .env/bin/activate` whenever the virtual environment is deactivated (this happens automatically when you exit the shell).

To run the program, simply run the `partycity` command.

If you unpacked these files from a zip folder, simply do:
```
unzip partycity.zip
cd partycity
python3 -m venv env
source .env/bin/activate # this may vary based on your shell
pip install -e .
partycity
```


## Topic Classifier Module
This is a module that, given a piece of text, will determine the topic of that text from a predetermined list. The possible topics are as follows:

* Abortion
* Economy
* Education
* Environment
* Immigration
* Health Care
* Gun Policy
* Terrorism
* Social Security
* Trade Policy

At a high level, the topic classifier scrapes tweets from Twitter using several related words for each topic and uses those tweets to train a Naive Bayes topic classifier. For example, to train the Naive Bayes classifier on the 'abortion' class, we scrape tweets from Twitter using Twitter's search api with the keywords 'abortion', 'pro-life', 'pro-choice' and 'planned parenthood'. These tweets are then proprocessed and appended to an 'abortion.txt' file, which is later used as the training data for the 'abortion' class of the Naive Bayes classifier.

The necessity for a topic classifier came from a lack of annotated training data. As training data for our party classifier, we could only find presidential debate transcripts from [here](https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-candidates-debates-1960-2016?fbclid=IwAR2xkzSTf8ygEfraZ-lac6ta-rDYya3jfmSKVZVMTWBWHDWAbkHcu2EwGc8). This data is, of course, not annoted (for both party AND topic). Since we will be creating party classifiers for each topic, our topic classifier is required when training our party recognition algorithm to determine which party classifier to train given an excerpt from any one of the debates. 


## Training Module
This is a module that scrapes the web for training data, preprocesses that data, and then creates several party classifiers using this data. Training data is retrieved by scraping the debate transcripts from General, Democratic and Republic debates, fetched from [here](https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/presidential-candidates-debates-1960-2016?fbclid=IwAR2xkzSTf8ygEfraZ-lac6ta-rDYya3jfmSKVZVMTWBWHDWAbkHcu2EwGc8). We then wrote a preprocessor python function to tokenize, remove stopwords and stem words. Preprocessed files are then output to a separate directory to be read by the main training algorithm. Using the files created by the scraper/preprocessor, several different party classifiers are created for each topic. These classifiers are listed as follows:

* Naive Bayes (Multinomial)
* Rocchio Text Classifier
* Semantic Classifier (TextBlob)

This means that in total, we created 30 classifiers. For example, 'abortion' had a Democratic vs Republican classifier implemented using each of the three classifiers listed above, and this was true for all other topics as well. The classifier data structures are then written to external files in JSON format. This is so that the testing module won't need to create all classifiers each time a test is run.


## Testing Module
This module scrapes Twitter for tweets from each state, then uses those tweets to determine whether the state is more liberal or conservative. Party classification is done using the JSON files generated from the [Training Module](#training-module) and the accuracy of these classifiers is calculated using the election results from the 2016 election to determine correctness.

## Contributors
* Sreeraj Marar (sreerajm)
* Brian Sutherland (bsuth)
* Nikita Badhwar (nbadhwar)
* Shameek Ray (shameek)
* Rodney Shibu (rodneyss)
