"""
Sentiment Analyzer:
	several methods[A,B,C]

	AA] modifiers - the scope of its effect
		I] the word after
		II] parse tree: every sibling after
		III] (negation only) negtool
	AB] modifiers(negation only) - the effect
		I]Flip
		II](A)symmetrical const. shift
		III]Variable Shift
		IV]Lexicon-look up (words only)

	B] Computing parent sentiment
		I] Flat Average
		II]Structural Average w/o Buffer (bottom up)
			P_i = mean(mod(nodes)) 
				-where mod() is element wise modifier function, 
				 if node is in scope of effect, it is modified
		III]Structural Average w/ Buffer(bottom up)
			P_i = mean(mod(buffer))
				-each element in buffer is either 
					1) a word that is not in the scope of a modifier
					2) a grouping of words that is in a scope of a modifier


1) modify [I-IV] word after modifier, flat average

2) modify [I-IV] words determined by neg_tool, flat average

3) modify [I-IV] words determined by parse tree, flat average


4) modify [I-IV] word after modifier, structural average w/o buffer
	-each modified word is immediately modified

5) modify [I-IV] words determined by neg_tool, structural average w/o buffer
	-each modified word is immediately modified

6) modify [I-IV] words determined by parse tree, structural average w/o buffer
	-each modified word is immediately modified


7) modify [I-IV] word after modifier, structural average w/ buffer
	-for each scope, an averaging of the values is made and then modified

8) modify [I-IV] words determined by neg_tool, structural average w/ buffer
	-for each scope, an averaging of the values is made and then modified

9) modify [I-IV] words determined by parse tree, structural average w/ buffer
	-for each scope, an averaging of the values is made and then modified

"""
import StanfordParser
import compositionality
import treefunctions
import tree

"""
Generate parsed sentences in string format (Stanford NLP)
	import StanfordParser
		LAUNCH CORENLP SERVER: 
		cd /Users/alanyuen/Desktop/untitled\ folder/SA/stanford-corenlp-python 

		python corenlp.py 
"""
def get_sentences():
	nlp = StanfordParser.StanfordNLP()

	test_sentences = ["i do not really dislike it"]
	other_sentences = [""]

	return [StanfordParser.parse(nlp, sentence) for sentence in test_sentences]

"""
Generate tree for structural analysis (tree.py)
	import tree.py
"""
def generate_tree(sentence):
	s = tree.Tree(sentence)
	s.generateTreeStructure()
	return s

"""
Determine scope for negation/modifier
	import treefunctions
"""
def neg_scope_detector(sentence, method = "PARSE_TREE"):
	if(method == "PARSE_TREE"):
		sentence = treefunctions.traverse_tree(sentence, fn = "NEG_SCOPE")

def mod_scope_detector(sentence, method = "PARSE_TREE"):
	if(method == "PARSE_TREE"):
		sentence = treefunctions.traverse_tree(sentence, fn = "MOD_SCOPE")

"""
Compositionality Methods
	import compositionality
"""
def compose_valence(sentence, compose_method, neg_method):
	if(compose_method == "PARSE_TREE"):
		compositionality.parsed_average(sentence, neg_method)

if __name__ == '__main__':
	sentences =  get_sentences()
	for sentence in sentences:
		s = generate_tree(sentence)
		neg_scope_detector(s)
		mod_scope_detector(s)
		compose_valence(s, compose_method = "PARSE_TREE", neg_method = "shift_asym")
		print("Sentence:{}, Valence: {}".format(s.sentence, s.root.effective_valence))
