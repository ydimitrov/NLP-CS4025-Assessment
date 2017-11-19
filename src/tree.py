from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES
with open('../Lexicons/positive-words.txt', 'r') as f:
    pos_words = [line.strip() for line in f]

with open('../Lexicons/negative-words.txt', 'r') as f:
    neg_words = [line.strip() for line in f]

with open('../Lexicons/nokia-pos.txt', 'r') as f:
    nokia_pos = [line.strip() for line in f]

with open('../Lexicons/nokia-neg.txt', 'r') as f:
    nokia_neg = [line.strip() for line in f]

with open('../Lexicons/rt-polarity-pos.txt', 'r') as f:
    rt_pos = [line.strip().decode('utf-8','ignore').encode("utf-8") for line in f]

with open('../Lexicons/rt-polarity-neg.txt', 'r') as f:
    rt_neg = [line.strip().decode('utf-8','ignore').encode("utf-8") for line in f]

np = ['NN', 'NNS', 'NNP', 'NNPS', 'WP', 'NP', 'PRP','S','SBAR']
adj = ['JJ', 'JJR', 'JJS','ADJP']
adv = ['RB', 'RBR', 'RBS', 'WRB']
det = ['DT', 'RPR$', 'WP$']
v = ['VB','VBD','VBG','VBN','VBP','VBZ','VP']
p = ['IN','PP']

def applyRules(partOfSpeech1, sentiment1, partOfSpeech2, sentiment2, headPos):
    # print 'Will start applying the rules on: ', partOfSpeech1, " ", head, " ", sentiment1, ' and ', partOfSpeech2," ", dependent, " ", sentiment2
    print 'Will start applying the rules on: ', partOfSpeech1, sentiment1, ' and ', partOfSpeech2, sentiment2
    if sentiment1 == sentiment2:
        return sentiment1
    if sentiment1 == '=':
        print sentiment2
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

    if headPos == 'pre-head': #partOfSpeech2 is head (pre-head)
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
    else: #partOfSpeech1 is head (post-head)
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
                        t = applyRules(headKey, t, key62, e, 'pre-head')
                        print t
                    if d['governorGloss'] == m and d['dependentGloss'] == n:
                        t = applyRules(headKey, t, key62, e, 'post-head')
                        print t
                        headKey = key62
                    if ((d['governorGloss'] == n and d['dependentGloss'] == m) or (d['governorGloss'] == m and d['dependentGloss'] == n)) and d['dep'] == 'dobj':
                    	directdep = 1
                    else:
                    	directdep = 0
                    print directdep
        headKey = key
    return m, t, headKey





if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    nlp = StanfordCoreNLP('http://localhost:9000')

    # print len(nokia_neg)
    # print len(nokia_pos)

    # # print len(rt_neg)
    # # print len(rt_pos)

    # countNeg = 0
    # countPos = 0
    # count = 0

    # for x in nokia_neg:
    #     count += 1
    #     print "Sentence ", count
    #     output = nlp.annotate(
    #         text = x.lower(),
    #         properties={
    #           'annotators': 'tokenize,ssplit,pos,depparse,parse',
    #           'outputFormat': 'json'
    #         }
    #     )
    #     if "CoreNLP request timed out" in output:
    #         print("CoreNLP request timed out. Your document may be too long.")
    #     else:
    #         sampleTree = output['sentences'][0]['parse']
    #         finalTree = parseTree(sampleTree)
    #         # pp.pprint(finalTree)
    #         head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], 'ROOT' )
    #         # print head
    #         # print 'final sentiment: ', e
    #         if e == '-':
    #             countNeg += 1
    #         # print types

    # for x in nokia_pos:
    #     count += 1
    #     print "Sentence ", count
    #     output = nlp.annotate(
    #         text = x.lower(),
    #         properties={
    #           'annotators': 'tokenize,ssplit,pos,depparse,parse',
    #           'outputFormat': 'json'
    #         }
    #     )
    #     if "CoreNLP request timed out" in output:
    #         print("CoreNLP request timed out. Your document may be too long.")
    #     else:
    #         sampleTree = output['sentences'][0]['parse']
    #         finalTree = parseTree(sampleTree)
    #         # pp.pprint(finalTree)
    #         head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], 'ROOT' )
    #         # print head
    #         # print 'final sentiment: ', e
    #         if e == '+':
    #             countPos += 1

    # for x in rt_neg:
    # 	count += 1
    #     print "Sentence ", count
    #     output = nlp.annotate(
    #         text = x.lower(),
    #         properties={
    #           'annotators': 'tokenize,ssplit,pos,depparse,parse',
    #           'outputFormat': 'json'
    #         }
    #     )
    #     if "CoreNLP request timed out" in output:
    #         print("CoreNLP request timed out. Your document may be too long.")
    #     else:
    #         sampleTree = output['sentences'][0]['parse']
    #         finalTree = parseTree(sampleTree)
    #         # pp.pprint(finalTree)
    #         head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], 'ROOT' )
    #         # print head
    #         # print 'final sentiment: ', e
    #         if e == '-':
    #             countNeg += 1
    #         # print types
    #
    # for x in rt_pos:
    # 	count += 1
    #     print "Sentence ", count
    #     output = nlp.annotate(
    #         text = x.lower(),
    #         properties={
    #           'annotators': 'tokenize,ssplit,pos,depparse,parse',
    #           'outputFormat': 'json'
    #         }
    #     )
    #     if "CoreNLP request timed out" in output:
    #         print("CoreNLP request timed out. Your document may be too long.")
    #     else:
    #         sampleTree = output['sentences'][0]['parse']
    #         finalTree = parseTree(sampleTree)
    #         # pp.pprint(finalTree)
    #         head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], 'ROOT' )
    #         # print head
    #         # print 'final sentiment: ', e
    #         if e == '+':
    #             countPos += 1

    # print "negative correct", countNeg
    # print "positive correct", countPos
    # print 'negative reviews:  ', len(rt_neg)
    # print 'positive reviews:  ', len(rt_pos)
    # print 'percent n correct: ', float(countNeg/float(len(rt_neg)))
    # print 'percent p correct: ', float(countPos/float(len(rt_pos)))
    # print 'negative reviews:  ', len(nokia_neg)
    # print 'positive reviews:  ', len(nokia_pos)
    # print 'percent n correct: ', float(countNeg/float(len(nokia_neg)))
    # print 'percent p correct: ', float(countPos/float(len(nokia_pos)))

    output = nlp.annotate(
        # text=InputReader(INPUT_FILES).read()[0],  # Use only the 1st
        # text = 'Clinton defeated Dole',
        # text = 'this is one of the nicest phones nokia has made .'.lower(),
        text = 'Sam eats red meat.'.lower(),
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
        finalTree = parseTree(sampleTree)
        pp.pprint(finalTree)
        head,e, types = getSentiment(finalTree, output['sentences'][0]['basicDependencies'], 'ROOT' )
        print head
        print 'final sentiment: ', e
        print types
