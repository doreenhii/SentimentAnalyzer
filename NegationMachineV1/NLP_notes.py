"""
#it's really not THAT good
#it's not really that good

#it's really not good
#it's not really good

#i do not think it's good
#i really do not think it's good
#i do not really think it's good

#it really wasn't exceptional truth: [not (exceptional +0.8)]
#it wasn't really exceptional


#negation is saying *something* is not... language is a way of thinking
	-you would think something is not to say the opposite is..
		-it really was [not exceptional] == it really was [antonymn(exceptional)] == it really was [normal]
		-not necessarily... it was not good is not the same as saying it was bad.

	-negation is placing boundaries for what is not.
	it is good ==> <----------------|----[  good  ]----------->
				sentiment value:  it is here ^
	it is not good ==> <------------|----[XXXXXXXX]----------->
				sentiment value:it is not here ^
				well a statement that something is not can also be interpreted as a statement that something is..
				it is on either side. But with language, it is assumed if it's not good, it's also not great, and etc, so you look at the other side.

	it is bad ==>  		<-------[   bad   ]----|------------------>
	it is not bad ==>	<-------[XXXXXXXXX]????|????[  good  ]-->
					if it isn't here^... then where?

		[the sentiment of "bad" really ranges from some negative X to 0... 
		[one can interpret not bad as there are no negatives, so it's either neutral or somewhat good
		[but another can interpret that not bad is a way of saying, "it's gotten worse, but it's not too much worse"]

		when is "it is not bad" a qualitatively a positive sentiment?
			-when you're referring to a subject that is usually bad, and the fact that it's not bad is a positive thing
		is a negative sentiment?
			-when you're referring to a subject that is usually good, but it's gotten worse somewhere somewhat closer to  "it's bad"


		-both are saying it is at least not bad, so it's in some what a good thing.. around "slightly good"



										   [		*        ] <--- the range of "good" (the padding**)
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0

	 		- the padding around the "true" value of the word depends on how general the word is...
	 				-the more neutral it is, the larger the padding?
	 				-the more extreme it is, the smaller the padding?



	 		 [							  ][		*        ] <--- the range of "good"
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0

		 		 					 [		Not Excellent	][	*  ] <--- the range of "excellent"
	<--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|-->
	 -1.0		    -0.5			0.0			   0.5            1.0


	 	-what kind of bounds can we set for not good? we know its something less than the bottom range of "good"...
	 		-how far back does it go?
	 		it is not good > it is bad[antonym(good)]
	 		it is not bad < it is good[antonym(bad)]
	 		it is not terrible < it is excellent[antonym(terrible)]

	 			- |(it is not bad) - (it is good)| < |(it is not terrible) < (it is excellent)|
	 				this means the closer the sentiment of word is to 0, the negated counterpart similar to the antonym
	 				while the more extreme the sentiment, the negated counterpart is very different from the antonym..

	 				--might this be because of how specific a word is? "bad" is a very general sense while "terrible" is more specific
	 					-not "terrible" is saying it's specifically not a small range of sentiment
	 					-not "bad" is saying it's generally not a large range of sentiment

	 					****
	 					-can we make the assumption that the more neutral the sentiment of word X is, the more general X is, so the negation(X) would be closer to the sentiment of antonym(X)
	 					-the more extreme the sentiment of X is, the less general X is, so the negation(X) would result in a sentiment just outside sentiment_range(X) in the opposite direction of the sign.
	 					****
	 		it is not decent ~= it is unsatisfactory[antonym(decent)]


#modifiers
	*modifiers act as weights. no modifiers has a weight of 1.
	-what's the difference between saying [it really was normal] and [it was normal]... they are both close to neutral sentiment values... but from a linguistic perspective, there would be a difference the influence it has for the context..

	p1[it really was normal...] <= (?) => p2[it seemed fun at first, but it quickly died down]
		-if p2 had a very negative sentiment, i would assume p1 would place a weight onto p2 more so than
	p1[it was normal...] <= (?) => p2[it seemed fun at first, but it quickly died down]

	should intensifiers and diminishers's effect be in the scope of the entire sentence and not just the phrase?
	could you use intensifiers and diminishers as weights for a weighted averaging of the sentiment values of phrases?
"""