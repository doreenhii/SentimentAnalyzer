def idNegationScope(sentence, NSD_method):
	if(NSD_method == "parse_tree"):
		#parsed neg scope
		traverse_tree(sentence,fn = "NEG_SCOPE")

	elif(NSD_method == "neg_nn"):
		pass
	elif(NSD_method == "neg_tool"):
		pass

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
			if(node.parent.POS_tag == "ADVP"):
				negate_node = node.parent
			else:
				negate_node = node
			index = negate_node.parent.children.index(negate_node)
			if(index + 1 < len(negate_node.parent.children)):
				for sibling in negate_node.parent.children[index+1:]:
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

def isNegation(word):
	f = open('negators.txt', 'rb')
	negators = f.readlines()
	for neg in negators:
		if(word.lower() == neg.strip("\n")):
			return True
	return False

