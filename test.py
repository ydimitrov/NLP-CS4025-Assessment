from pycorenlp import StanfordCoreNLP
import pprint

pp = pprint.PrettyPrinter(indent=4)

nlp = StanfordCoreNLP('http://localhost:9000')

text = (
  'Pusheen and Smitha walked along the beach. '
  'Pusheen wanted to surf, but fell off the surfboard.')
output = nlp.annotate(text, properties={
  'annotators': 'tokenize,ssplit,pos,depparse,parse',
  'outputFormat': 'json'
  })


print(output['sentences'][0]['parse'])
pp.pprint(output)
