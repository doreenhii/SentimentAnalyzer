import os,csv

def get_sentiment(word):
	#**find lexicon/dictionary
	"""
	res = self.nlp.annotate(word,
	                   properties={
	                       'annotators': 'sentiment',
	                       'outputFormat': 'json',
	                       'timeout': 1000,
	                   })
	return int(res["sentences"][0]["sentimentValue"])
	"""
	f = open(os.getcwd()+'/Dataset/Affective-Ratings/BRM-emot-submit.csv', 'rb')
	reader = csv.reader(f)
	for row in reader:
		if(row[1] == word.lower()):
			return (float(row[2]) - 5.0)
	return -999


def isNegation(word):
	if(word == "not" or word == "NOT"):
		return True
	else:
		return False
