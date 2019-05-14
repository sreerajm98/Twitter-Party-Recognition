"""
Calculates the sentiment score for every state given each state's tweets
using the TextBlob library.

Rodney Shibu <rodneyss@umich.edu>
"""


from partycity.training.train import train_text_blob
from partycity.topic_classification.preprocess import ppTweet
from textblob import TextBlob

def sentiment(tweets):
	#Format: party_details = {'d':{'economy': -0.6}, 'r':{'economy': 0.5}}
	party_details = train_text_blob(False)

	frq_score = {'abortion': 0.45, 'economy': 0.84, 'education': 0.66, 'environment': 0.52, 'immigration': 0.7, 'health_care': 0.74, 'gun_policy': 0.72, 'terrorism': 0.8, 'social_security': 0.67, 'trade': 0.57}

	running_scores = {}
	users_avg = {}
	sentiment_result = {}
	for state in tweets:
		running_scores[state] = {}
		for tweet in tweets[state]:
			tweet_arr = tweet.split(" ")
			topic = tweet_arr[0].replace("'","")
			user = tweet_arr[1]
			tweet_arr.pop(0)
			tweet_arr.pop(0)
			tweet = ppTweet(' '.join(tweet_arr))
			
			blob = TextBlob(tweet)
			polarity = blob.sentiment.polarity
			subjectivity = blob.sentiment.subjectivity
			if subjectivity > 0.3:
				dem_diff = float(abs(polarity - party_details['d'][topic]))
				repub_diff = float(abs(polarity - party_details['r'][topic]))
				score = 0.5 + ((1 - (repub_diff/2)) * frq_score[topic] * subjectivity * 0.5) - ((1 - (dem_diff/2)) * frq_score[topic] * subjectivity * 0.5)
				if score > 1:
					score = 1
				elif score < 0:
					score = 0
				if user in running_scores[state]:
					running_scores[state][user]['total'] += score
					running_scores[state][user]['num'] += 1
				else:
					running_scores[state][user] = {'total': score, 'num': 1}

	for state in running_scores:
		for user in running_scores[state]:
			if state not in users_avg:
				users_avg[state] = {}
			users_avg[state][user] = running_scores[state][user]['total'] / running_scores[state][user]['num']
	for state in users_avg:
		num_d = 0
		num_r = 0
		for user in users_avg[state]:
			if users_avg[state][user] >= 0.5:
				num_r += 1
			else:
				num_d += 1
		if num_d > num_r:
			sentiment_result[state] = "d"
		else:
			sentiment_result[state] = "r"
	return sentiment_result
