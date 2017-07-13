import os,csv

def isNegation(word):
	f = open('negators.txt', 'rb')
	negators = f.readlines()
	for neg in negators:
		if(word.lower() == neg.strip("\n")):
			return True
	return False

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
	mod = 1.0
	f = open(os.getcwd()+'/Dataset/modifiers.csv', 'rb') #percentage increase
	reader = csv.reader(f)
	for row in reader:
		if(row[0] == word.lower()):
			mod = float(row[1])
	f.close()
	return mod

def create_negLex():
	f = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/S140-AFFLEX-NEGLEX-unigrams.txt', 'rb')
	f2 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredNEGLEX.txt', 'wb')

	reader = csv.reader(f)
	for row in reader:
		if "_NEG" in row[0]:
			print(row)

			string = row[0].replace('_NEGFIRST', '')
			string = string.replace('_NEG', '')
			f2.write(string+"\n")
	f.close()
	f2.close()

def create_negLex():
	f = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/S140-AFFLEX-NEGLEX-unigrams.txt', 'rb')
	f2 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredNEGLEX.txt', 'wb')
	f3 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredPOSLEX.txt', 'wb')
	reader = csv.reader(f)
	for row in reader:
		string = row[0].replace('#', '')
		if "_NEG" in row[0]:
			print(row)
			string = string.replace('_NEGFIRST', '')
			string = string.replace('_NEG', '')

			f2.write(string+"\n")
		else:
			f3.write(string+"\n")

	f.close()
	f2.close()
	f3.close()

def create_corrs_negLex():
	f = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredNEGLEX.txt', 'rb')
	f2 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredPOSLEX.txt', 'rb')
	f3 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/poslex.txt', 'wb')

	reader = csv.reader(f)
	reader2 = csv.reader(f2)
	found = False
	for row_a in reader:
		#print(row[0].split('\t'))
		word = row_a[0].split('\t')[0]
		for row_b in reader2:
			#print(row_b)
			word2 = row_b[0].split('\t')[0]
			if word == word2:
				f3.write(row_b[0] +"\n")
				found = True
				break
		if not found:
			f3.write("NOT FOUND\n")
		else:
			found = False
		f2.seek(0)
	f.close()
	f2.close()
	f3.close()

def fix_corr_lex():
	f = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredNEGLEX.txt', 'rb')
	f2 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/poslex.txt', 'rb')
	f3 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/neglex.txt', 'wb')

	reader = csv.reader(f)
	reader2 = csv.reader(f2)
	remove_indices = []
	index = 0
	for row in reader2:
		if('NOT FOUND' in row[0]):
			remove_indices.append(index)
			index += 1
	index = 0
	for row in reader:
		if index not in remove_indices:
			f3.write(row[0] + '\n')
		index += 1


	f.close()
	f2.close()
	f3.close()

def print_sentiment(words):
	for word in words:
		print("Word:{} ... Sentiment:{}".format(word, get_sentiment(word)))

if __name__ == '__main__':
	#print_sentiment(["good", "excellent", "bad", "undesirable", "unpleasant", "excellent","satisfactory", "adequate", "reasonable", "quite", "fair", "decent", "sufficient", "fine", "right", "average", 'tolerable', 'passable', 'middling'])
	#create_negLex()
	#create_corrs_negLex()
	fix_corr_lex()

"""
def create_PosLex():
	f = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/corres_neglex.txt', 'rb')
	f2 = open(os.getcwd()+'/Dataset/Sentiment140AffLexNegLex/FilteredPOSLEX.txt', 'wb')

	reader = csv.reader(f)
	for row in reader:
		if "_NEG" not in row[0]:
			f2.write(row[0]+"\n")
	f.close()
	f2.close()

"""
