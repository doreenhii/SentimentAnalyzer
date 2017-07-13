
	""" "good" 
		-sentiment is 0.44
		-range("good") [0.2 <-> 0.65]
		-length of range: 0.65 - 0.2 = 0.45 OR 1-senti("good") == 1-0.44 = 0.56
		-v2 range: 0.5 / (|0.5 - (0.44)| + 0.5) = 0.5/(0.56) = 0.89 * alpha = 0.445
		-v3 range: range(0.5*alpha/(|0.5-|senti("good")|| + 0.5) | alpha = 0.75) = 0.67
			-lower bound = 0.44 - (0.67/2) = 0.105
			-upper bound = 0.44 + (0.67/2) = 0.775
	"""
	                          *         [         *         ]                         
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0

	""" "not good" 
		-senti("good") is 0.44
		-range("good") = 0.5*alpha/(|0.5-|senti("good")|| + 0.5) | alpha = 0.75 = 0.5*0.75 /[(0.5-0.44) + 0.5]
				- range("good") = 0.375 / [0.56] = 0.67
		-senti("not good") = senti("good") - range("good") = 0.44 -0.67 = -0.23
	"""
	                         [      *      ][      *      ]                         
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0



	""" "really good"
	 		-sentiment is 1.75*good = .77
	 		-range("really good") is 0.5*range("good")
	 		-v2 0.5/(|0.5 - (0.77)| + 0.5) = 0.5/(0.27+0.5) = 0.5/0.77 = 0.65 * 0.5 = 0.325 / 2 = 0.1625
	 		0.77 - 0.1625
	 """
	                                       			    [   *   ]                         
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0



	  """ "sufficient"
	 		-sentiment is 0.2
	 		-range("sufficient") = 0.5 - senti("sufficient") = 0.5 /|(0.5-|senti()|)| + 0.5 = 1/2
	 		0.5/(0.3+0.5) = 0.5/0.8 = 5/8 = 0.625 * 0.5 = 0.3125/2 = 0.15625
	 		senti("sufficient") - range("sufficient") = 0.2 - [0.3125] = -0.1125
	 		0.2 - 0.15625 = 0.04375
	 		0.2 + 0.15625 = 0.35625
	 		-  0.5 <--- the smaller the range....  the larger the range --->0.0
	 		0.5/(0.5-senti("sufficient")
	 			-0.
	 """
	                             *	  [    *    ]                         
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0
