"""
LAUNCH CORENLP SERVER: 
cd /Users/alanyuen/Desktop/untitled\ folder/SA/stanford-corenlp-python 

python corenlp.py 


"""


import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint

import argparse
import sys

FLAGS = None

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

def parse(nlp, sentence):
	result = nlp.parse(sentence)
	for i in range(len(result['sentences'])):
		line = result['sentences'][i]['parsetree']
		print(line)


nlp = StanfordNLP()
parse(nlp, "i never thought it was good , but i've never tried")
"""
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_dir', type=str, default='/Users/alanyuen/Desktop/SentimentAnalysisResearch/RawData/amazon_labelled.txt',
		              help='Directory for sentences data')
	FLAGS, unparsed = parser.parse_known_args()
	with open(FLAGS.data_dir) as f:
		sentences = f.readlines()


	
	parsed_sentence_file = open("parsed_sentence_file.txt","wb")

	for s in sentences:
		s = s.split("\t")[0]
		try:
			result = nlp.parse(s)
			for i in range(len(result['sentences'])):
				line = result['sentences'][i]['parsetree']
				print(line)
				parsed_sentence_file.write(line+"\n")
		except:
			pass

"""