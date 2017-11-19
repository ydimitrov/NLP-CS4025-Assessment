from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES
with open('../Lexicons/positive-words.txt', 'r') as f:
    pos_words = [line.strip() for line in f]

with open('../Lexicons/negative-words.txt', 'r') as f:
    neg_words = [line.strip() for line in f]

np = ['NN', 'NNS', 'NNP', 'NNPS', 'WP', 'NP', 'PRP','S']
adj = ['JJ', 'JJR', 'JJS']
adv = ['RB', 'RBR', 'RBS', 'WRB']
det = ['DT', 'RPR$', 'WP$']
v = ['VB','VBD','VBG','VBN','VBP','VBZ','VP']
p = ['IN']

def applyRules(partOfSpeech1, sentiment1, partOfSpeech2, sentiment2, headPos, head, dependent):
    # print 'Will start applying the rules on: ', partOfSpeech1, " ", head, " ", sentiment1, ' and ', partOfSpeech2," ", dependent, " ", sentiment2
    print 'Will start applying the rules on: ', partOfSpeech1, sentiment1, ' and ', partOfSpeech2, sentiment2
    if sentiment1 == sentiment2:
        return sentiment1
    if sentiment1 == '=':
        return sentiment2
    if sentiment2 == '=':
        return sentiment1

    if partOfSpeech1 in np:
        partOfSpeech1 = 'NP'
    elif partOfSpeech1 in adj:
        partOfSpeech1 = 'ADJ'
    elif partOfSpeech1 in adv:
        partOfSpeech1 = 'ADV'
    elif partOfSpeech1 in det:
        partOfSpeech1 = 'DET'
    elif partOfSpeech1 in v:
        partOfSpeech1 = 'VP'
    elif partOfSpeech1 in p:
        partOfSpeech1 = 'PP'

    if partOfSpeech2 in np:
        partOfSpeech2 = 'NP'
    elif partOfSpeech2 in adj:
        partOfSpeech2 = 'ADJ'
    elif partOfSpeech2 in adv:
        partOfSpeech2 = 'ADV'
    elif partOfSpeech2 in det:
        partOfSpeech2 = 'DET'
    elif partOfSpeech2 in v:
        partOfSpeech2 = 'VP'
    elif partOfSpeech2 in p:
        partOfSpeech2 = 'PP'

    # print 'Will start applying the rules on: ', partOfSpeech1, sentiment1, ' and ', partOfSpeech2, sentiment2

    if headPos == 1: #partOfSpeech2 is head (post-head)
        if partOfSpeech2 == 'NP' and (partOfSpeech1 == 'ADJ' or partOfSpeech1 == 'VP'):
            return sentiment1
        if partOfSpeech2 == 'ADJ' and partOfSpeech1 == 'PP':
            return sentiment2
        if partOfSpeech2 == 'ADV' and partOfSpeech1 == 'PP':
            return sentiment2
        if partOfSpeech2 == 'PP' and (partOfSpeech1 == 'NP' or partOfSpeech1 == 'VP'):
            return sentiment2
        if partOfSpeech2 == 'NP' and (partOfSpeech1 == 'NP' or partOfSpeech1 == 'PP'):
            return sentiment2
    else: #partOfSpeech1 is head (pre-head)
         if (partOfSpeech2 == 'DET' or partOfSpeech2 == 'ADJ' or partOfSpeech2 == 'VP') and partOfSpeech1 == 'NP':
             return sentiment2
         if (partOfSpeech2 == 'DET' or partOfSpeech2 == 'PP' or partOfSpeech2 == 'ADV') and partOfSpeech1 == 'ADJ':
             return sentiment2
         if (partOfSpeech2 == 'DET' or partOfSpeech2 == 'ADV') and partOfSpeech1 == 'ADV':
             return sentiment2
         if (partOfSpeech2 == 'ADV' or partOfSpeech2 == 'NP') and partOfSpeech1 == 'PP':
             return sentiment2
         if (partOfSpeech2 == 'NP') and partOfSpeech1 == 'NP':
             return sentiment2
	# print "Applying the rules"

def getSentiment(sentence, dependencies, stype):
    # pp.pprint(sentence)
    if type(sentence) is str:
		if sentence in pos_words:
			sentiment = "+"
		elif sentence in neg_words:
			sentiment = "-"
		else:
			sentiment = "="
		return sentence, sentiment, stype

    n = ''
    t = '='

    for key in sentence:
        headKey = key
        for x in range(len(sentence[key])-1, -1, -1):
            m, e, key62  = getSentiment(sentence[key][x], dependencies, headKey)
            if n == '':
                n = m
                t = e
                headKey = key62
            else:
                for d in dependencies:
                    if d['governorGloss'] == n and d['dependentGloss'] == m:
                        m = n
                        e = applyRules(headKey, t, key62, e, 1,m,n)
                    if d['governorGloss'] == m and d['dependentGloss'] == n:
                        e = applyRules(headKey, t, key62, e, 0,n,m)
                        headKey = key62
        headKey = key
    return m, e, headKey





if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    nlp = StanfordCoreNLP('http://localhost:9000')

    output = nlp.annotate(
        # text=InputReader(INPUT_FILES).read()[0],  # Use only the 1st
        # text = 'Clinton defeated Dole',
        text = 'there is much which has been said in other reviews about the features of this phone , it is a great phone , mine worked without any problems right out of the box . '.lower(),
        # text = 'the senators supporting the leader failed to praise his hopeless HIV prevention program',
        properties={
          'annotators': 'tokenize,ssplit,pos,depparse,parse',
          'outputFormat': 'json'
        }
    )
    types = ''
    if "CoreNLP request timed out" in output:
        print("CoreNLP request timed out. Your document may be too long.")
    else:
        sampleTree = output['sentences'][0]['parse']
        # pp.pprint(output['sentences'][0]['parse'])
        # pp.pprint(output['sentences'][0]['basicDependencies'])
        finalTree = parseTree(sampleTree)
        pp.pprint(finalTree)
        head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], 'ROOT' )
        print head
        print 'final sentiment: ', e
        print types
