
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
