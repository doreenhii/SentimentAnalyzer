import os,csv

def get_sentiment(word):
	scores = []
	f = open(os.getcwd()+'/Dataset/Affective-Ratings/Ratings_Warriner_et_al.csv', 'rb') #1-9
	reader = csv.reader(f)
	for row in reader:
		if(row[1] == word.lower()):
			scores.append((float(row[2]) - 5.0)/4.0)
			break
	f.close()
	f = open(os.getcwd()+'/Dataset/ANEW/ALL-Table 1.csv', 'rb') #1-9
	reader = csv.reader(f)
	for row in reader:
		if(row[1] == word.lower()):
			scores.append((float(row[2]) - 5.0)/4.0)
			break
	f.close()
	if(len(scores)>0):
		return sum(scores)/len(scores)
	else:
		return -999

def get_modifier_value(word):
	mod = 0.0
	f = open(os.getcwd()+'/Dataset/modifiers.csv', 'rb') #percentage increase
	reader = csv.reader(f)
	for row in reader:
		if(row[0] == word.lower()):
			mod = float(row[1])
	f.close()
	return 1.0+mod

