import time
from partycity.topic_classification.train import create_naive_bayes
from partycity.topic_classification.data_gen import data_gen
from partycity.training.preprocess import gen_training_data
from partycity.training.train import train_nb
from partycity.training.train import train_rocchio
from partycity.training.train import train_text_blob
from partycity.testing.analyse import get_results


def main():
    user_input = ''
    while True:
        print("Welcome to PartyCity!")
        print("---------------------")
        print("1) Topic Classification")
        print("2) Training Models")
        print("3) Predicting Election Results")
        print("4) Be a good samaritan")
        print("5) Quit")
        user_input = input('Enter option: ')
        print('\n')

        if user_input == '1':
            while user_input != '3':
                print("Topic Classification")
                print("--------------------")
                print("1) Expand training data")
                print("2) Create topic classifier")
                print("3) Back")
                user_input = input('Enter option: ')
                print('\n')
                if user_input == '1':
                    data_gen()
                    print('Finished expanding training data')
                    print('\n')
                elif user_input == '2':
                    create_naive_bayes()
                    print('Finished creating Naive Bayes topic classifier')
                    print('\n')
                elif user_input != '3':
                    print('That wasn\'t a valid option but I\'ll assume you meant to go back.')

        elif user_input == '2':
            while user_input != '5':
                print("Training Models")
                print("---------------")
                print("1) Scrape and preprocess debates")
                print("2) Train Naive Bayes")
                print("3) Train Rocchio Classifier")
                print("4) Train Sentiment Model (TextBlob)")
                print("5) Back")
                user_input = input('Enter option: ')
                print('\n')
                if user_input == '1':
                    gen_training_data()
                    print('Finished scraping/preprocessing debate transcripts')
                    print('\n')
                elif user_input == '2':
                    train_nb()
                    print('Finished creating Naive Bayes classifier')
                    print('\n')
                elif user_input == '3':
                    train_rocchio()
                    print('Finished creating Rocchio classifier')
                    print('\n')
                elif user_input == '4':
                    train_text_blob()
                    print('Finished creating sentiment model (TextBlob)')
                    print('\n')
                elif user_input != '5':
                    print('That wasn\'t a valid option but I\'ll assume you meant to go back.')

        elif user_input == '3':
            get_results('final_collected_tweets.txt')
            print('Finished predicting political affiliations')
            print('How did we do?')
            print('\n')

        elif user_input == '4':
            print('Thank you for your contribution!')
            print('This counts as your digital signature approving this group for an A.')
            print('We appreciate your time and consideration.')
            time.sleep(5)
            print('\n')

        elif user_input != '5':
            print('That wasn\'t a valid option :(')
            print('\n')

        else:
            break

    print('Thanks for using our demo!')
    print('We hope you enjoyed our project and found it interesting!')
