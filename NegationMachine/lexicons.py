import os,csv

def get_sentiment(word):
	f = open(os.getcwd()+'/Dataset/Affective-Ratings/Ratings_Warriner_et_al.csv', 'rb')
	reader = csv.reader(f)
	for row in reader:
		if(row[1] == word.lower()):
			return (float(row[2]) - 5.0)
	return -999

