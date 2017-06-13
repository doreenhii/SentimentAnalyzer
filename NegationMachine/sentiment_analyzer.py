
from pycorenlp import StanfordCoreNLP
from negation_functions import *
from negation_scope_detection import *
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
				


def idNegationScope(sentence, NSD_method):
	if(NSD_method == "parse_tree"):
		#parsed neg scope
		traverse_tree(sentence,fn = "NEG_SCOPE")

	elif(NSD_method == "neg_nn"):
		pass
	elif(NSD_method == "neg_tool"):
		pass

def process_negation(sentence, neg_method):
	for word in sentence.word_nodes_list:
		if(word.isNegated and word.base_valence != -999):
			word.effective_valence = negate(word.base_valence, neg_method)
		else:
			word.effective_valence = word.base_valence

def parsed_average(sentence, neg_method, node = None):	
	if(node == None):
		node = sentence.root

	scores = []
	for c in node.children:

		if(c.effective_valence == -999):#if c has not been reached yet
			if(len(c.children) > 0):
				#recursion on children
				parsed_average(sentence, neg_method, node = c)
		#print"NODE: POS:{} WORD:{} SCORE:{}".format(c.POS_tag, c.word, c.aggregate_value)

		#0 here has to mean does not have valence.. if 0 here means neutral, it needs to be part of the scores
		if(c.effective_valence != -999):
			scores.append(c.effective_valence)
		
	if(len(scores) > 0):
		node.effective_valence = sum(scores)/float(len(scores)) #average of children

def flat_average(sentence):
		total_score = 0
		counter = 0
		for word in sentence.word_nodes_list:
			if(word.effective_valence != -999):
				total_score += word.effective_valence
				counter += 1
		total_score /= float(counter)
		return total_score

def traverse_tree(sentence, node = None, fn = "PRINT"):
	if(node == None):
		node = sentence.root

	if(fn == "PRINT"):
		children_string = "["
		for c in node.children:
			children_string += " **POS:[\""+str(c.POS_tag)+"\"] Word:[\""+str(c.word)+"\"]** "
		#print main details of node
		print"\nNODE: POS_Tag:[{}] Word:[{}] EffectiveV:[{}] BaseV:[{}]".format(node.POS_tag, node.word, node.effective_valence, node.base_valence)
		#print parent node
		if(node.parent):
			print("\tParent: [" + node.parent.POS_tag + "]")
		#print children node(s)
		print("\tChildren:" + children_string + "]")

	elif(fn == "NEG_SCOPE"):
		#if current node word is a negation word, negate all consecutive siblings
		if(isNegation(node.word)):
			index = node.parent.children.index(node)
			if(index + 1 < len(node.parent.children)):
				for sibling in node.parent.children[index+1:]:
					neg_subtree(sibling)
					#sibling.isNegated = not node.isNegated

	#traverse children
	for c in node.children:
		traverse_tree(sentence, c, fn)

def neg_subtree(node):
	node.isNegated = not node.isNegated
	if(len(node.children) > 0):
		for c in node.children:
			neg_subtree(c)

if __name__ == '__main__':
	sentences = ["(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB not) (ADJP (JJ great)))) (, ,) (CC but) (S (NP (PRP it)) (VP (VBZ is) (RB not) (ADJP (JJ bad)))))))","(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB not) (ADJP (JJ bad)))) (, ,) (CC but) (S (NP (FW i)) (VP (VBP do) (RB not) (VP (VB prefer) (NP (PRP it))))))))","(ROOT (FRAG (S (S (NP (DT this)) (VP (VBZ is) (RB not) (ADJP (RB too) (JJ terrible)))) (, ,) (CC but) (S (NP (FW i)) (VP (VBP do) (RB not) (VP (VB like) (NP (PRP it))))))))","(ROOT (S (S (NP (DT this)) (VP (VBZ is) (ADJP (RB absolutely) (JJ terrible)))) (, ,) (CC and) (S (NP (FW i)) (VP (VBP do) (RB not) (VP (VB like) (SBAR (WHADVP (WRB how)) (S (NP (PRP it)) (VP (VBZ 's) (ADVP (RB so))))))))))"]
	analyzer = SentimentAnalyzer()
	analyzer.init(sentences, avg_method = "parse_tree")
	analyzer.run()
	for sentence in analyzer.sentences:
		print"sentence: '{}' [{}]".format(sentence.sentence, sentence.sentiment)