import time

from pycorenlp import StanfordCoreNLP

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

                    if d['dep'] == 'dobj' and (
                        (d['governorGloss'] == n
                            and d['dependentGloss'] == m)
                        or (d['governorGloss'] == m
                            and d['dependentGloss'] == n)):
                       directdep = 1

                    else:
                       directdep = 0
        headKey = key
    return m, t, headKey


if __name__ == "__main__":

    nlp = StanfordCoreNLP('http://localhost:9000')

    countNeg = 0
    countPos = 0
    total_count = 0

    for data_set in [nokia_neg, nokia_pos, rt_neg, rt_pos]:
        for sentence in data_set:
            total_count += 1

            output = nlp.annotate(
                text = sentence.lower(),
                properties={
                  'annotators': 'tokenize,ssplit,pos,depparse,parse',
                  'outputFormat': 'json'
                }
            )

            # Sleep for 2 seconds on server timeout
            while isinstance(output, str):
                time.sleep(1)
                output = nlp.annotate(
                    text = sentence.lower(),
                    properties={
                      'annotators': 'tokenize,ssplit,pos,depparse,parse',
                      'outputFormat': 'json'
                    }
                )

            finalTree = parseTree(output['sentences'][0]['parse'])

            head, e, types = getSentiment(
                finalTree,
                output['sentences'][0]['basicDependencies'],
                'ROOT'
            )

            if e == '-':
                countNeg += 1
            elif e == '+':
                countPos += 1

    print(
        "Negative correct:  {}\n"
        "Positive correct:  {}\n"
        "Negative reviews:  {}\n"
        "Positive reviews:  {}\n"
        "Percent n correct: {}\n"
        "Percent p correct: {}\n"
        "Pegative reviews:  {}\n"
        "Positive reviews:  {}\n"
        "Percent n correct: {}\n"
        "Percent p correct: {}\n".format(
            countNeg,
            countPos,
            len(rt_neg),
            len(rt_pos),
            float(countNeg/float(len(rt_neg))),
            float(countPos/float(len(rt_pos))),
            len(nokia_neg),
            len(nokia_pos),
            float(countNeg/float(len(nokia_neg))),
            float(countPos/float(len(nokia_pos))),
        )
    )
