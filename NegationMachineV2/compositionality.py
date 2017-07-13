import negation
"""
compositionality.py
	import negation

	parsed_average()
"""
def parsed_average(sentence, neg_method, node = None):
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
					scores.append(negation.negate(sum(neg_buffer[-1]),neg_method))

				#add value to the scores
				scores.append(node.children[i].base_valence * node.children[i].mod_value)
		else:

			#if child is not a word, check if it breaks a neg_scope
			if(neg_buffer_running):
				neg_buffer_running = False
				#negate the sum of scores of the neg_buffer
				scores.append(negation.negate(sum(neg_buffer[-1]),neg_method))

			#non-word nodes are subtrees: recursively compute the subtree
			parsed_average(sentence, neg_method, node = node.children[i])
			if(node.children[i].effective_valence != -999):
				scores.append(node.children[i].effective_valence)

	#check if it is the last child, if so then end neg_scope and add up the scores
	if(neg_buffer_running):
		neg_buffer_running = False
		scores.append(negation.negate(sum(neg_buffer[-1]),neg_method))

	if(len(scores) > 0):
		#this function is only called on non-word children
		if(node.isNegated):
			node.effective_valence = negation.negate(sum(scores)/len(scores), neg_method) * node.mod_value
		else:
			node.effective_valence = sum(scores)/len(scores) * node.mod_value
	print("Node POS: {}, Node Word: {}, Node Valence: {}".format(node.POS_tag, node.word, node.effective_valence))