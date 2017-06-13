from pycorenlp import StanfordCoreNLP
from negation_functions import *
from negation_scope_detection import *
from averaging_functions import *
from lexicons import *

#can be either word or phrase
#can have structural capabilities (tree)
class Node:
	def __init__(self):
		self.parent = None
		self.children = []

		self.POS_tag = ""
		self.word = ""
		self.node_type = "" #"word" or "phrase"


		self.base_valence = 0 # [-5,5] from dataset **ONLY WORDS ** -1 if no valence found
		self.effective_valence = -999 #processed valence value used to add up sentiment

		self.isNegated = False #used to flag the use of the negation fn
class Sentence:
	def __init__(self, string):
		self.word_nodes_list = [] #the sentence in a list of nodes (words only!)
		self.sentence_parsed_string = string #in parsed format

		#tree structure
		self.root = None

		#output
		self.sentence = ""
		self.sentiment = 0

	def generateTreeStructure(self):
		current_substring = self.sentence_parsed_string
		current_node = self.root

		while (len(current_substring) > 0):
			try:
				#print(current_substring)
				expand_idx = current_substring.index("(")
				close_idx = current_substring.index(")")

				if( expand_idx < close_idx ):
					#expanding tree
					new_node = Node()

					#extract POS tag
					current_substring = current_substring[expand_idx+1:] #cuts to the POS tag
					
					POS_tag_end = current_substring.index(' ')
					pos_tag = current_substring[:POS_tag_end]

					#sets POS tag
					new_node.POS_tag = pos_tag

					#links node to tree
					if(pos_tag == "ROOT"):
						self.root = new_node
						current_node = new_node
					else:
						new_node.parent = current_node
						current_node.children.append(new_node)

					#try if there is a word (checks if this node is a word node)
					space_idx = current_substring.index(' ')
					if(current_substring[space_idx+1] != '('):
						WORD_end = current_substring.index(')')
						word = current_substring[space_idx+1:WORD_end]
						new_node.word = word

						self.sentence += word + " "
						#where you define the sentiment value of the individual word
						new_node.base_valence = get_sentiment(word)

						#storing the word nodes in an accessible list
						self.word_nodes_list.append(new_node)

					#if(new_node.parent):
						#print"New Node -- POS:[{}] Word:[{}] Parent:[{}]".format(new_node.POS_tag,new_node.word,new_node.parent.POS_tag)
					current_node = new_node
				else:
					#closing tree
					current_substring = current_substring[close_idx+1:]
					current_node = current_node.parent

			except ValueError:
				break
class SentimentAnalyzer:
	def __init__(self):
		self.sentences = []

		self.NSD_method = ""
		self.neg_method = ""
		self.avg_method = ""


	def init(self, sentences_parsed_string, NSD_method = "parse_tree", neg_method = "invert", avg_method = "parse_tree"):
		self.NSD_method = NSD_method
		self.neg_method = neg_method
		self.avg_method = avg_method
		for sentence in sentences_parsed_string:
			new_sentence = Sentence(sentence)
			new_sentence.generateTreeStructure()
			self.sentences.append(new_sentence)

	def run(self):
		for s in self.sentences:

			#[DIMENSION 1]negation scope detection method
			idNegationScope(s, self.NSD_method)

			#[DIMENSION 2]negation method
			process_negation(s, self.neg_method)

			#[DIMENSION 3]averaging method
			if(self.avg_method == "parse_tree"):
				parsed_average(s, self.neg_method)
				s.sentiment = s.root.effective_valence
			elif(self.avg_method == "flat"):
				s.sentiment = flat_average(s)

if __name__ == '__main__':
	sentences = ["(ROOT (FRAG (S (S (NP (LS i)) (ADVP (RB never)) (VP (VBD thought) (SBAR (S (NP (PRP it)) (VP (VBD was) (ADJP (JJ good))))))) (, ,) (CC but) (S (NP (FW i)) (VP (VBP 've) (ADVP (RB never)) (VP (VBN tried)))))))","(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB n't) (ADJP (JJ great)))) (, ,) (CC but) (S (NP (PRP it)) (VP (VBZ is) (RB n't) (ADJP (JJ terrible)))))))","(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB not) (ADJP (JJ great)))) (, ,) (CC but) (S (NP (PRP it)) (VP (VBZ is) (RB not) (ADJP (JJ bad)))))))","(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB not) (ADJP (JJ bad)))) (, ,) (CC but) (S (NP (FW i)) (VP (VBP do) (RB not) (VP (VB prefer) (NP (PRP it))))))))","(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB not) (ADJP (RB too) (JJ terrible)))) (, ,) (CC but) (S (NP (FW i)) (VP (VBP do) (RB not) (VP (VB like) (NP (PRP it))))))))","(ROOT (S (S (NP (DT this)) (VP (VBZ is) (ADJP (RB absolutely) (JJ terrible)))) (, ,) (CC and) (S (NP (FW i)) (VP (VBP do) (RB not) (VP (VB like) (SBAR (WHADVP (WRB how)) (S (NP (PRP it)) (VP (VBZ 's) (ADVP (RB so))))))))))"]
	analyzer = SentimentAnalyzer()
	analyzer.init(sentences, NSD_method = "parse_tree", neg_method = "shift_asym", avg_method = "parse_tree")
	analyzer.run()
	for sentence in analyzer.sentences:
		#traverse_tree(sentence)
		print"sentence: '{}' [{}]".format(sentence.sentence, sentence.sentiment)

"""
**WHATS UP WITH ADVP???? ('NEVER')

NSD_method = "parse_tree" neg_method = "shift_asym", avg_method = "parse_tree"
sentence: 'i never thought it was good , but i 've never tried ' [-0.58125]
sentence: 'this is n't great , but it is n't terrible ' [-0.675]
sentence: 'this is not great , but it is not bad ' [-0.5325]
sentence: 'this is not bad , but i do not prefer it ' [-0.15625]
sentence: 'this is not too terrible , but i do not like it ' [-0.4125]
sentence: 'this is absolutely terrible , and i do not like how it 's so ' [-1.5]
"""