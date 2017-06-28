from negation_functions import*
def parsed_average(sentence, neg_method, node = None):
	#DOES NOT IMPLEMENT MODIFIERS HERE	
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

def parsed_average_bottom_up(sentence, neg_method, node = None):
	#base valence is -999 if is a subtree, is some value if word
	#effective valence is -999
	#isNegated is labeled for all nodes
	if(node == None):
		node = sentence.root

	scores = []
	neg_buffer_running = False
	neg_buffer = []
	
	for i in range(len(node.children)):
		if(node.children[i].base_valence != -999): 

			#if child is a word
			if(node.children[i].isNegated): 
				#if it is negated, check if it is part of a neg_scope

				if(neg_buffer_running):
					#if so, add to the last neg_scope
					neg_buffer[-1].append(node.children[i].base_valence * node.children[i].mod_value) 

				else:
					#if not, create new neg_scope in buffer
					neg_buffer.append([node.children[i].base_valence * node.children[i].mod_value])
					neg_buffer_running = True

			else:
				if(neg_buffer_running):
					#if it is not negated, then check if it marks the end of a negscope
					neg_buffer_running = False
					#negate the sum of scores of the neg_buffer
					scores.append(negate(sum(neg_buffer[-1]),neg_method))

				#add value to the scores
				scores.append(node.children[i].base_valence * node.children[i].mod_value)
		else:

			#if child is not a word, check if it breaks a neg_scope
			if(neg_buffer_running):
				neg_buffer_running = False
				#negate the sum of scores of the neg_buffer
				scores.append(negate(sum(neg_buffer[-1]),neg_method))

			#non-word nodes are subtrees: recursively compute the subtree
			parsed_average_bottom_up(sentence,neg_method,node = node.children[i])
			if(node.children[i].effective_valence != -999):
				scores.append(node.children[i].effective_valence)

	#check if it is the last child, if so then end neg_scope and add up the scores
	if(neg_buffer_running):
		neg_buffer_running = False
		scores.append(negate(sum(neg_buffer[-1]),neg_method))

	if(len(scores) > 0):
		#this function is only called on non-word children
		if(node.isNegated):
			node.effective_valence = negate(sum(scores)/len(scores), neg_method) * node.mod_value
		else:
			node.effective_valence = sum(scores)/len(scores) * node.mod_value


def flat_average(sentence):
		total_score = 0
		counter = 0
		for word in sentence.word_nodes_list:
			if(word.effective_valence != -999):
				total_score += word.effective_valence
				counter += 1
		total_score /= float(counter)
		return total_score
