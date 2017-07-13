import lexicons

def traverse_tree(sentence, node = None, fn = "PRINT"):
	"""
		import lexicons.py:
			isNegation()
			get_modifier_value()
	"""
	if(node == None):
		node = sentence.root

	if(fn == "PRINT"):
		"""
		PRINTS TREE
		#print(node.word)
		"""
		
		children_string = "["
		for c in node.children:
			children_string += " **POS:[\""+str(c.POS_tag)+"\"] Word:[\""+str(c.word)+"\"]** "
		#print main details of node
		print("\nNODE: POS_Tag:[{}] Word:[{}] EffectiveV:[{}] BaseV:[{}]".format(node.POS_tag, node.word, node.effective_valence, node.base_valence))
		#print parent node
		if(node.parent):
			print("\tParent: [" + node.parent.POS_tag + "]")
		#print children node(s)
		print("\tChildren:" + children_string + "]")

	elif(fn == "NEG_SCOPE"):

		"""
		DETERMINES NEGATION SCOPE via PARSE TREE
		"""	

		#if current node word is a negation word, negate all consecutive siblings
		if(lexicons.isNegation(node.word)):

			#if it is ADVP, go up one parent
			if(node.parent.POS_tag == "ADVP"):
				negate_node = node.parent
			else:
				negate_node = node

			#for each sibling after modifier, negate
			index = negate_node.parent.children.index(negate_node)
			if(index + 1 < len(negate_node.parent.children)):
				for sibling in negate_node.parent.children[index+1:]:
					sibling.isNegated = not sibling.isNegated

	elif(fn == "MOD_SCOPE"):

		"""
		DETERMINES INTENSIFIER/DIMINISHER SCOPE via PARSE TREE
		"""

		#if current node word is a intensifier/diminisher word, modify all consecutive siblings
		mod_value = lexicons.get_modifier_value(node.word)

		if(mod_value != 1.0):

			#if it is ADVP, go up one parent
			if(node.parent.POS_tag == "ADVP"):
				mod_node = node.parent
			else:
				mod_node = node

			#for each sibling after modifier, add modifier value
			index = mod_node.parent.children.index(mod_node)
			if(index + 1 < len(mod_node.parent.children)):
				for sibling in mod_node.parent.children[index+1:]:
					sibling.mod_value *= mod_value

	#traverse children
	for c in node.children:
		if(c):
			traverse_tree(sentence, c, fn)