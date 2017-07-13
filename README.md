# SentimentAnalyzer: using various negation processes

SET UP:
	-clone https://github.com/dasmith/stanford-corenlp-python
	-LAUNCH CORENLP SERVER: 
		cd .../stanford-corenlp-python 
		python corenlp.py
	-load up sentences in main.py: get_sentences()
	-run main.py

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
