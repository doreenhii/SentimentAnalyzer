"""
LAUNCH SENTIMENT ANALYZER SERVER: 

cd /Users/alanyuen/Desktop/SA/stanford-corenlp-full-2016-10-31 
java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000
"""

from pycorenlp import StanfordCoreNLP
from negation_functions import *
from negation_scope_detection import *
from lexicons import *

class Node:
	def __init__(self):
		#links
		self.parent = None
		self.children = []

		#identity
		self.POS_tag = ""
		self.word = ""

		#word values
		self.base_value = 0 #value retrieved from lexicon
		self.effective_value = 0 #base_value modified by code

		#parent value
		self.aggregate_value = -1 #value of node as an combination of children values

		#is in scope of negation flag
		self.isNegated = False


class ParseTree:
	"""
		init()				sets up the parameters of the model
								-NSD_method: ["off", "neg_nn", "neg_tool", "parse_tree"]
								-neg_method: ["ignore", "invert", "shift_sym", "shift_asym", "lexicon"]
								-scoring_method: ["flat", "structure"]

		generate() 			generates the tree from the sentence in parsed format:
								[set up]
									need to generate self.scope_of_negation if "neg_nn" or "neg_tool"
								[functions used] 
									getSentiment() - returns valence for word from lexicon
									label_words_in_neg_scope():	uses the generated self.scope_of_negation, then returns if word is negated

		process_negation()	called after generate() to generate the effective values of each valence

		traverse_tree()  	a function to traverse the tree preorder with functionalities such as print or "negate" (used for parsed_negation)
								[functions used]
									isNegated() - returns true if word is in negator word bank

		parsed_average_score() 	a method of combining sentiment scores via the tree by averaging layer by layer, 
							in place of flat averaging

		flat_average(): 	averages all of the effective values for the nodes, and ignores syntactic structure
	"""
	def __init__(self):
		self.root = None
		self.sentence = ""
		self.sentence_as_nodes = []

		self.nlp = StanfordCoreNLP('http://localhost:9000')
		
		#negation scope detection
		self.NSD_method = ""
		self.scope_of_negation = []
		self.label_counter = 0

		#negation_function
		self.neg_method = ""

		#score_aggr
		self.scoring_method = ""

	def init(self, parsed_sentence, neg_scope_detection_method = "off", neg_function = "invert", score_aggr = "flat"):
		"""
		NSD_method = ["off", "neg_nn", "neg_tool", "parse_tree"]
		neg_method = ["ignore", "invert", "shift_sym", "shift_asym", "lexicon"]
		scoring_method = ["flat", "structure"]
		"""
		#sets sentence
		self.sentence = parsed_sentence

		#sets NSD_method
		self.NSD_method = neg_scope_detection_method
		self.scope_of_negation = get_neg_scope(neg_scope_detection_method) #retrieves scope of negation of sentence

		#sets negation method
		self.neg_method = neg_function

		#sets scoring method
		self.scoring_method = score_aggr

	def label_words_in_neg_scope(self):
		"""
			for neg_nn or neg_tool, negation scope is provided before generating the tree
			for parse_tree, negation scope will have to be determined after generating the tree
				-you will need to manually code that in
		"""
		if(self.NSD_method == "off" or self.NSD_method == "parse_tree"):
			return False

		if(self.label_counter in self.scope_of_negation):
			self.label_counter += 1
			return True
		else:
			self.label_counter += 1
			return False

	def generate(self):
		current_substring = self.sentence
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

						#where you define the sentiment value of the individual word
						new_node.base_value = get_sentiment(word)

						#extracts sentence for later use
						self.sentence += word + " "

						#if negation_scope is provided, label the word if is negated
						new_node.isNegated = self.label_words_in_neg_scope()

						#storing the word nodes in an accessible list
						self.sentence_as_nodes.append(new_node)

					#if(new_node.parent):
						#print"New Node -- POS:[{}] Word:[{}] Parent:[{}]".format(new_node.POS_tag,new_node.word,new_node.parent.POS_tag)
					current_node = new_node
				else:
					#closing tree
					current_substring = current_substring[close_idx+1:]
					current_node = current_node.parent

			except ValueError:
				break

	def process_negation(self):
		#if negation scope is provided before tree generation, then apply the negation functions to negated words
		#if negation scope is not provided (parse_tree method), then identify the scope of negation here, then apply negation functions to words
		if(self.NSD_method == "parse_tree"):
			#traverse tree, preorder
			#if word is found in a negator dictionary, then mark its siblings as negated
			self.traverse_tree(fn = "NEGATE")

		#not only are the words negated, but the phrases too!
		for word in self.sentence_as_nodes:
			if(word.isNegated):
				word.effective_value = negate(word.base_value, self.neg_method)
			else:
				word.effective_value = word.base_value

	def parsed_average_score(self, node = None):	
		if(node == None):
			node = self.root

		scores = []
		for c in node.children:

			if(c.aggregate_value == -1):#if c has not been reached yet
				if(len(c.children) > 0):
					#recursion on children
					self.parsed_average_score(c) 
				else:
					#if it is a leaf, assign aggregate_value as base_value 
					c.aggregate_value = c.effective_value #c.base_value 

			#print"NODE: POS:{} WORD:{} SCORE:{}".format(c.POS_tag, c.word, c.aggregate_value)
			scores.append(c.aggregate_value)
			
		if(len(scores) > 0):

			node.aggregate_value = sum(scores)/float(len(scores)) #average of children
			if(node.isNegated):
				node.aggregate_value = negate(node.aggregate_value,self.neg_method)

	def flat_average(self):
		total_score = 0
		for word in self.sentence_as_nodes:
			total_score += word.effective_value
		total_score /= float(len(self.sentence_as_nodes))
		return total_score

	def traverse_tree(self,node = None, fn = "PRINT"):
		if(node == None):
			node = self.root
		
		children_string = "Children: ["
		for c in node.children:
			children_string += " **POS:[\""+str(c.POS_tag)+"\"] Word:[\""+str(c.word)+"\"]** "

		if(fn == "PRINT"):
			#print main details of node
			print"\nNODE: POS_Tag:[{}] Word:[{}] Sentiment:[{}]".format(node.POS_tag, node.word, node.aggregate_value)
			#print parent node
			if(node.parent):
				print("\tParent:" + node.parent.POS_tag)
			#print children node(s)
			print("\tChildren:" + children_string + "]")

		elif(fn == "NEGATE"):
			#if current node word is a negation word, negate all consecutive siblings
			if(isNegation(node.word)):
				index = node.parent.children.index(node)
				if(index + 1 < len(node.parent.children)):
					for sibling in node.parent.children[index+1:]:
						print("##################")
						print(sibling.POS_tag)
						#if sibling is already negated, then double negation?
						#"i never do not like apples"???
						if(sibling.isNegated):
							sibling.isNegated = False
						else:
							sibling.isNegated = True
		#traverse children
		for c in node.children:
			self.traverse_tree(c, fn)

if __name__ == '__main__':
	new_parse = ParseTree()
	new_parse.init("(ROOT (S (NP (PRP I)) (VP (VBP do) (RB not) (VP (VB like) (NP (NN pie))))))", neg_scope_detection_method = "parse_tree")
	new_parse.generate()
	#new_parse.traverse_tree()

	new_parse.process_negation()
	new_parse.parsed_average_score()
	new_parse.traverse_tree()
	print("structured score average:",new_parse.root.aggregate_value)
	print("flat score average:", new_parse.flat_average())
