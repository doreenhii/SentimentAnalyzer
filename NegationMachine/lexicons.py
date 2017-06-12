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
	return 1.0


def isNegation(word):
	if(word == "not" or word == "NOT"):
		return True
	else:
		return False