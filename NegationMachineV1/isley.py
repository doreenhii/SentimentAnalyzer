import nltk
import os
from nltk.parse import stanford
from nltk.corpus import wordnet
from nltk.tree import *

# execfile('C:\\Users\\Isley\\polarityparsing\\polarities.py')
anewDict = {'lost': -0.646, 'lonely': -0.7075, 'admired': 0.685, 'power': 0.385, 'not': -0.5}
warrinerDict = {'lost': -0.646, 'lonely': -0.7075, 'admired': 0.685, 'power': 0.385, 'not': -0.5}

# Test sentences
test0 = "Yesterday I met a girl that kept touching me on the arm without me wanting her to."
test1 = "She was lost and lonely despite being admired by most for her big awesome power."
test = "She was not admired."

demoTree = Tree('S', [Tree('NP', [Tree('PRP', ['She'])]), Tree('VP', [Tree('VBD', ['was']), Tree('VP', [Tree('VBN', ['lost']), Tree('CC', ['and']), Tree('VBN', ['lonely']), Tree('PP', [Tree('IN', ['despite']), Tree('S', [Tree('VP', [Tree('VBG', ['being']), Tree('VP', [Tree('VBD', ['admired']), Tree('PP', [Tree('IN', ['by']), Tree('NP', [Tree('NP', [Tree('JJS', ['most'])]), Tree('PP', [Tree('IN', ['for']), Tree('NP', [Tree('PRP$', ['her']), Tree('JJ', ['big']), Tree('JJ', ['awesome']), Tree('NN', ['power'])])])])])])])])])])]), Tree('.', ['.'])])

# Stanford NLP Parsers
os.environ['STANFORD_PARSER'] = 'C:\\Users\\Isley\\Anaconda\\Lib\\site-packages\\nltk\\parse\\jars'
os.environ['STANFORD_MODELS'] = 'C:\\Users\\Isley\\Anaconda\\Lib\\site-packages\\nltk\\parse\\jars'
java_path = "C:\\Program Files\\Java\\jdk1.8.0_60\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path

parser = stanford.StanfordParser(model_path='C:\\Users\\Isley\\Anaconda\\Lib\\site-packages\\nltk\\parse\\jars\\englishPCFG.ser.gz')
#sentences = parser.raw_parse_sents([test1, test2]) for parsing multiple sents

sentences = parser.raw_parse(test)
sentList = [list(i)[0] for i in sentences]

#sentList[0] is the tree object for the whole sentence
tree = sentList[0]
print(tree)
ptreeTEST1 = ParentedTree.convert(tree)
ptreeTEST = ParentedTree('S', [ParentedTree('NP', [ParentedTree('PRP', ['She'])]), ParentedTree('VP', [ParentedTree('VBD', ['was']), ParentedTree('RB', ['not']), ParentedTree('VP', [ParentedTree('VBD', ['admired'])])]), ParentedTree('.', ['.'])])


for i in range(len(sentList[0])):
    print(i, sentList[0][i])

from nltk import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
#wordnet_lemmatizer.lemmatize('creating','v')    # u'create'
#tokens = nltk.word_tokenize(test1)

def get_wordnet_pos(treebank_tag):
    if treebank_tag[0] == 'J':
        return wordnet.ADJ
    elif treebank_tag[0] == 'V':
        return wordnet.VERB
    elif treebank_tag[0] == 'N':
        return wordnet.NOUN
    elif treebank_tag == 'R':
        return wordnet.ADV
    else:
        return ''

def average(l):
    return float(sum(l))/len(l) if len(l) > 0 else float('nan')

def assignPolarity(ptree):
    '''Takes in a ParentedTree object that has no children and returns
    the polarity value of the lemmatized word token in it'''
    try:
        anew = anewDict[wordnet_lemmatizer.lemmatize(ptree[0], get_wordnet_pos(ptree.label()))]
        warriner = warrinerDict[wordnet_lemmatizer.lemmatize(ptree[0], get_wordnet_pos(ptree.label()))]
        polarity = average([anew, warriner])
        print('Found : ' + ptree[0])

    except KeyError:
        try:
            polarity = average([warrinerDict[ptree[0]], anewDict[ptree[0]]])
            print('Found : ' + ptree[0])
        except KeyError:
            polarity = 0
            print('Not found: ' + ptree[0])
            
    return polarity

def numOfSubtrees(tree):
    '''Takes in a ParentedTree object and returns the number of subtrees it has'''
    result = len(list(tree.subtrees()))
    return result
        
totals = []

def parseOne(subtree):
    subList = [] 

    #second loop for lengths that are counted the same
    if len(list(subtree.subtrees())) > 1:   
        word = subtree[0][0]
        label = subtree[0].label()
        subList.append((subtree[0][0], subtree[0].label(), assignPolarity(subtree[0])))
    else: #such as punctuation
        subList.append((subtree[0], subtree.label(), assignPolarity(subtree)))
    print('Sublist: ', subList)
    return subList

def parse(tree):
    if tree.__len__() == 1:
        parseOne(tree)
        subList = parseOne(tree)
        avgPol = combinePolarity(subList)
        totals.append(avgPol)
    else:
        for i in range((tree.__len__())-1,-1,-1):
            parse(tree[i])
                

##dimin/intensifiers -- > multiply
##neg --> if current pos, subtract 1, else add 1
            
def adjust(item1, item2):
    return item1+item2

def listAverage(itemList):
    num = 0
    for word in itemList:
        num += word[2]
    return ( num / float(len(itemList)))

def runningAverage(itemList, item2):
    return ((listAverage(itemList) + item2[2])/(len(itemList)+1))

modifiersList = ["without", "despite", "not"]

def hasModifiers(itemList):       
    for element in itemList:
        if element[0] in modifiersList:
            return True
    return False

def combinePolarity(itemList):
    #If the list has no modifiers in it, average together
    if not hasModifiers(itemList):
        return listAverage(itemList)
    else:
        for element in itemList:
            if element[0] in modifiersList:
                index = itemList.index(element[0])
    
                return listAverage(adjust(itemList[index], listAverage[index:]))
            else:
                return 0


'''
new list created for each subtree that has children (that don't have other children)
''' 

'''
TESTING TO SEE WHICH TOKENS ARE IN LEMLIST
for each in lemlist:
	if each in anewDict.keys():
		print(anewDict[each], each)
#Results from anewDict	
('-0.545', 'lost')
('-0.7075', 'lonely')
('0.685', 'admired')
('0.385', 'power')
TODO LATER
# SentiWordNet
from nltk.corpus import sentiwordnet as swn
##print(list(swn.senti_synsets('slow')))
happy = list(swn.senti_synsets('happy', 'a'))
##print(happy)
'''

if __name__ == "__main__":
    parse(ptreeTEST)
    print("---end---")