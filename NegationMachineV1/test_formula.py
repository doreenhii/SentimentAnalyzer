import math
def interpretability(valence):
	return 1.0/(abs(abs(valence)-0.3)+0.5)

def getRange(valence):
	alpha = 0.3
	return alpha*interpretability(valence)

def neg(valence):
	#if asymmetrical, then signs are different.
	sign = 1.5 #positive values have a stronger negation effects
	if(valence < 0):
		sign = -0.5
	sign *= -math.log(min(abs(valence),1))
	return valence - (sign*getRange(valence))

def neg2(valence):
	multiplier = 1.5
	sign = 1
	if(valence < 0):
		multiplier = 0.75
	multiplier *= -math.log(min(abs(valence*0.75),1))
	return valence - sign*multiplier*1

def sigmoid(val):
	return 1.0/(1.0+math.exp(val))

def neg3(valence):
	magnitude = abs(valence)
	frequency = 0 #-1 not frequent, 1 very frequent
	multiplier_magnitude = sigmoid(magnitude)*5
	multiplier_frequency = sigmoid(-frequency)*5/2.5
	#print("mult_mag{} --- mult_freq{}".format(multiplier_magnitude,multiplier_frequency))
	return valence - sign(valence)*(multiplier_magnitude+multiplier_frequency)

def sign(val):
	if val <0:
		return -0.01
	else:
		return 1
def neg_these(valences):
	for valence in valences:
		print("valence: {}    negated_valence: {}".format(valence,neg3(valence)))

neg_these([-i/10.0 for i in reversed(range(10)[1:])])
neg_these([i/10.0 for i in range(10)[1:]])