from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES
with open('../Lexicons/positive-words.txt', 'r') as f:
    pos_words = [line.strip() for line in f]

with open('../Lexicons/negative-words.txt', 'r') as f:
    neg_words = [line.strip() for line in f]


def applyRules(partOfSpeech1, sentiment1, partOfSpeech2, sentiment2):

	print "Applying the rules"

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
        for x in range(len(sentence[key])-1, -1, -1):
            m, e, key62  = getSentiment(sentence[key][x], dependencies, key)
            print "m:       " + m
            # print "key:       " + key
            # print "stype:     " + stype
            print "key62:   " + key62
            # print "sentiment: " + e
            if n == '':
                n = m
                t = e
                headKey = key62
                print "headKey: " + headKey
            else:
                for d in dependencies:
                    print d['governorGloss'], ' ?= ', n , d['dependentGloss'], ' ?= ', m
                    if d['governorGloss'] == n and d['dependentGloss'] == m:
                        m = n
                        e = t
                        # headKey = 
                        # print "headKey: " + headKey
                        # print "headKey: " + headKey + " key62: " + key62
            print '================================================='
        headKey = key
        print "headKey: " + headKey + " key62: " + key62
    return m, e, headKey





if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    nlp = StanfordCoreNLP('http://localhost:9000')

    output = nlp.annotate(
        # text=InputReader(INPUT_FILES).read()[0],  # Use only the 1st
        # text = 'Clinton defeated Dole',
        # text = 'Sam eats red meat',
        text = 'the senators supporting the leader failed to praise his hopeless HIV prevention program',
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
        head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], types )
        print head
        print e
        print types
