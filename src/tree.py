from pycorenlp import StanfordCoreNLP
import pprint
from parseTree import parseTree

pp = pprint.PrettyPrinter(indent=4)

nlp = StanfordCoreNLP('http://localhost:9000')

sentences = open("../Lexicons/nokia-neg.txt", "r")
for line in sentences:
    print line.strip()
    text = (line)
    output = nlp.annotate(text, properties={
      'annotators': 'tokenize,ssplit,pos,depparse,parse',
      'outputFormat': 'json'
      })
    # print(output['sentences'][0]['parse'])
    # pp.pprint(output['sentences'])
    sampleTree = output['sentences'][0]['parse']
    print parseTree(sampleTree)

    # print "\n"

# text = (
#   'Pusheen and Smitha walked along the beach. '
#   'Pusheen wanted to surf, but fell off the surfboard.')
# output = nlp.annotate(text, properties={
#   'annotators': 'tokenize,ssplit,pos,depparse,parse',
#   'outputFormat': 'json'
#   })
#
#
# print(output['sentences'][0]['parse'])
# pp.pprint(output)
