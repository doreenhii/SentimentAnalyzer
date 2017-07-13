import lexicons #get_sentiment in generateTreeStructure()

"""
Node object[word or phrase]:
	used to store words/phrases for tree structure for parsing functionality
"""
class Node:
	def __init__(self):
		#tree linkability
		self.parent = None
		self.children = []

		#node identification
		self.POS_tag = ""
		self.word = ""
		self.node_type = "" #"word" or "phrase"

		#valence placeholders
		self.base_valence = -999 #valence from lexicon (words)
		self.effective_valence = -999 #modified valence (words/phrases)

		self.isNegated = False #used to flag the use of the negation fn
		self.mod_value = 1.0

"""
Sentence object:
	used to store a sentence in its tree structure using generateTreeStructre()
	holds the root node and an array of word nodes (for easy access)
"""
class Tree:
	def __init__(self, string):
		self.word_nodes_list = [] #the sentence in a list of nodes (words only!)
		self.sentence_parsed_string = string #in parsed format

		#tree structure
		self.root = None

		#output
		self.sentence = ""
		self.sentiment = 0

	def generateTreeStructure(self):
		"""
			takes in parsed format string of the sentence (from stanford parser)
			and organizes each word/phrase into a tree

			-uses get_sentiment(word) to retrieve the lexical valence
		"""
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
						new_node.base_valence = lexicons.get_sentiment(word)
						if(new_node.base_valence != -999):
							print("{} - {}".format(new_node.word,new_node.base_valence))

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
