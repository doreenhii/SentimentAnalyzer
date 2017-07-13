import os,csv
def negate(score, method):
	if(method == "invert"):
		return invert(score)
	elif(method == "shift_sym"):
		return shift_sym(score)
	elif(method == "shift_asym"):
		return shift_asym(score)
	else:
		return score

def invert(score):
	return -score

def shift_sym(score):
	shift_val = 0.5

	if score < 0:
		score += shift_val
	else:
		score -= shift_val

	return score
	
def shift_asym(score):

	if(score < 0):
		score = score/4.0
		#score += 1.5
	else:
		score = -score/4.0
		#score -= 2.5

	return score
