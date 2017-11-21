import time
import pprint

from pycorenlp import StanfordCoreNLP

pp = pprint.PrettyPrinter(indent=4)

with open('Lexicons/positive-words.txt', 'r') as f:
    pos_words = [line.strip() for line in f]

with open('Lexicons/negative-words.txt', 'r') as f:
    neg_words = [line.strip() for line in f]

with open('Lexicons/nokia-pos.txt', 'r') as f:
    nokia_pos = [line.strip().decode('utf-8','ignore').encode("utf-8") for line in f]

with open('Lexicons/nokia-neg.txt', 'r') as f:
    nokia_neg = [line.strip().decode('utf-8','ignore').encode("utf-8") for line in f]

with open('Lexicons/rt-polarity-pos.txt', 'r') as f:
    rt_pos = [line.strip().decode('utf-8','ignore').encode("utf-8") for line in f]

with open('Lexicons/rt-polarity-neg.txt', 'r') as f:
    rt_neg = [line.strip().decode('utf-8','ignore').encode("utf-8") for line in f]

def applyRules(partOfSpeech1, sentiment1, partOfSpeech2, sentiment2, headPos):

    poc = {
        'NP': ['NN', 'NNS', 'NNP', 'NNPS', 'WP', 'NP', 'PRP','S','SBAR'],
        'ADJ': ['JJ', 'JJR', 'JJS','ADJP'],
        'ADV': ['RB', 'RBR', 'RBS', 'WRB'],
        'DET': ['DT', 'RPR$', 'WP$'],
        'VP': ['VB','VBD','VBG','VBN','VBP','VBZ','VP'],
        'PP': ['IN','PP'],
    }

    if sentiment1 == sentiment2:
        return sentiment1

    if sentiment1 == '=':
        return sentiment2
    if sentiment2 == '=':
        return sentiment1

    for annotation in poc:
        if partOfSpeech2 in poc[annotation]:
            partOfSpeech1 = annotation
        if partOfSpeech2 in poc[annotation]:
            partOfSpeech2 = annotation

    if headPos == 'pre-head':
        if partOfSpeech2 == 'NP' and partOfSpeech1 in ['ADJ', 'VP']:
            return sentiment1
        if ( (partOfSpeech2 == 'ADJ' and partOfSpeech1 == 'PP')
                or (partOfSpeech2 == 'ADV' and partOfSpeech1 == 'PP')
                or (partOfSpeech2 == 'PP' and partOfSpeech1 in ['NP', 'VP'])
                or (partOfSpeech2 == 'NP' and partOfSpeech1 in ['NP', 'PP']) ):

            return sentiment2

    else:
        if ( (partOfSpeech1 == 'NP' and partOfSpeech2 in ['DET', 'ADJ', 'VP'])
                 or (partOfSpeech1 == 'ADJ' and partOfSpeech2 in ['DET', 'ADV', 'PP'])
                 or (partOfSpeech1 == 'PP' and partOfSpeech2 in ['ADV', 'NP'])
                 or (partOfSpeech2 == 'NP' and partOfSpeech1 == 'NP') ):

            return sentiment2


def parseTree(s):
    s = [x.strip() for x in s.replace('\r\n', ' ').split(' ')
        if x]

    new_s =''
    for word in s:
        if word.startswith('('):
            new_s += '{"' + word[1:] + '": ['
        else:
            new_s += '"' + word.replace(')','') + '"' + ']}, ' * word.count(')')

    tree = eval(new_s[:-2].replace(', }', '}'))
    return tree


def getSentiment(sentence, dependencies, stype):
    if isinstance(sentence, str):
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

                    if d['governorGloss'] == m and d['dependentGloss'] == n:
                        t = applyRules(headKey, t, key62, e, 'post-head')
                        headKey = key62
        headKey = key
    return m, t, headKey

def findPercentage(dataset, sentiment):
    total_count = 0
    correct = 0
    opposite = 0
    neutral = 0
    for sentence in dataset:
        total_count += 1
        output = nlp.annotate(
            text = sentence.lower(),
            properties={
              'annotators': 'tokenize,ssplit,pos,depparse,parse',
              'outputFormat': 'json'
            }
        )
        if "CoreNLP request timed out" in output:
            print("CoreNLP request timed out. Your document may be too long.")
        else:
            finalTree = parseTree(output['sentences'][0]['parse'])

            head, e, types = getSentiment(
                finalTree,
                output['sentences'][0]['basicDependencies'],
                'ROOT'
            )

            if sentiment == '+':
                if e == '+':
                    correct += 1
                elif e == '-':
                    opposite += 1
                else:
                    neutral += 1
            if sentiment == '-':
                if e == '-':
                    correct += 1
                elif e == '+':
                    opposite += 1
                else:
                    neutral += 1
    return correct, opposite, neutral


if __name__ == "__main__":

    nlp = StanfordCoreNLP('http://localhost:9000')

    nokiaTN, nokiaFP, nokiaNegNeutral= findPercentage(nokia_neg,'-')
    nokiaTP, nokiaFN, nokiaPosNeutral = findPercentage(nokia_pos,'+')
    rtTN, rtFP, rtNegNeutral = findPercentage(rt_neg,'-')
    rtTP, rtFN, rtPosNeutral = findPercentage(rt_pos,'+')

    totalFP = nokiaFP + rtFP
    totalFN = nokiaFN + rtFN
    totalTP = nokiaTP + rtTP
    totalTN = nokiaTN + rtTN
    total_neg = len(nokia_neg) + len(rt_neg)
    total_pos = len(nokia_pos) + len(rt_pos)
    totalNegNeutral = nokiaNegNeutral + rtNegNeutral
    totalPosNeutral = nokiaPosNeutral + rtPosNeutral

    nokiaAccuracy = float((nokiaTP + nokiaTN)/float((nokiaTP + nokiaFP + nokiaTN + nokiaFN)))
    nokiaPrecision = float(nokiaTP/float(nokiaTP + nokiaFP))
    nokiaRecall = float(nokiaTP/float(nokiaTP + nokiaFN))
    nokiaFScore = float((2*nokiaRecall*nokiaPrecision)/(nokiaRecall + nokiaPrecision))

    rtAccuracy = float((rtTP + rtTN)/float((rtTP + rtFP + rtTN + rtFN)))
    rtPrecision = float(rtTP/float(rtTP + rtFP))
    rtRecall = float(rtTP/float(rtTP + rtFN))
    rtFScore = float((2*rtRecall*rtPrecision)/(rtRecall + rtPrecision))

    totalAccuracy = float((totalTP + totalTN)/float((totalTP + totalFP + totalTN + totalFN)))
    totalPrecision = float(totalTP/float(totalTP + totalFP))
    totalRecall = float(totalTP/float(totalTP + totalFN))
    totalFScore = float((2*totalRecall*totalPrecision)/(totalRecall + totalPrecision))

    print "Nokia negative: ", len(nokia_neg)
    print "Nokia positive: ", len(nokia_pos)
    print "Nokia True Negative: ", nokiaTN
    print "Nokia True Positive: ", nokiaTP
    print "Nokia False Negative: ", nokiaFN
    print "Nokia False Positive: ", nokiaFP
    print "Nokia Negative - Neutral:", nokiaNegNeutral
    print "Nokia Positive - Neutral:", nokiaPosNeutral
    print "Accuracy: ", nokiaAccuracy
    print "Precision: ", nokiaPrecision
    print "Recall: ", nokiaRecall
    print "F-score: ", nokiaFScore
    print "Percent n correct: ", float(nokiaTN/float(len(nokia_neg)))
    print "Percent p correct: ", float(nokiaTP/float(len(nokia_pos)))
    print "======================================="
    print "RT negative: ", len(rt_neg)
    print "RT positive: ", len(rt_pos)
    print "RT True Negative: ", rtTN
    print "RT True Positive: ", rtTP
    print "RT False Negative: ", rtFN
    print "RT False Positive: ", rtFP
    print "RT Negative - Neutral:", rtNegNeutral
    print "RT Positive - Neutral:", rtPosNeutral
    print "Accuracy: ", rtAccuracy
    print "Precision: ", rtPrecision
    print "Recall: ", rtRecall
    print "F-score: ", rtFScore
    print "Percent n correct: ", float(rtTN/float(len(rt_neg)))
    print "Percent p correct: ", float(rtTP/float(len(rt_pos)))
    print "======================================="
    print "Total negative: ", total_neg
    print "Total positive: ", total_pos
    print "Total True Negative: ", totalTN
    print "Total True Positive: ", totalTP
    print "Total False Negative: ", totalFN
    print "Total False Positive: ", totalFP
    print "Total Negative - Neutral:", totalNegNeutral
    print "Total Positive - Neutral:", totalPosNeutral
    print "Accuracy: ", totalAccuracy
    print "Precision: ", totalPrecision
    print "Recall: ", totalRecall
    print "F-score: ", totalFScore
    print "Percent n correct: ", float(totalTN/float(total_neg))
    print "Percent p correct: ", float(totalTP/float(total_pos))
