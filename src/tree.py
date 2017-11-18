from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES

def getSentiment(sentence, dependencies):
    pp.pprint(sentence)
    if type(sentence) is str:
        return sentence
    n = ''

    for key in sentence:
        for x in range(len(sentence[key]),0,-1):
            m = getSentiment(sentence[key][x-1], dependencies)
            if n == '':
                n = m
            else:
                for d in dependencies:
                    print d['governorGloss'], ' ?= ', n , d['dependentGloss'], ' ?= ', m
                    if d['governorGloss'] == n and d['dependentGloss'] == m:
                        m = n
            print '================================================='
    return m





if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    nlp = StanfordCoreNLP('http://localhost:9000')

    output = nlp.annotate(
        # text=InputReader(INPUT_FILES).read()[0],  # Use only the 1st
        # text = 'Clinton defeated Dole',
        text = 'The senators supporting the leader failed to praise his hopeless HIV prevention program',
        properties={
          'annotators': 'tokenize,ssplit,pos,depparse,parse',
          'outputFormat': 'json'
        }
    )

    if "CoreNLP request timed out" in output:
        print("CoreNLP request timed out. Your document may be too long.")
    else:
        sampleTree = output['sentences'][0]['parse']
        # pp.pprint(output['sentences'][0]['parse'])
        # pp.pprint(output['sentences'][0]['basicDependencies'])
        finalTree = parseTree(sampleTree)
        # pp.pprint(finalTree)
        head = getSentiment(finalTree, output['sentences'][0]['basicDependencies'])
        print head
