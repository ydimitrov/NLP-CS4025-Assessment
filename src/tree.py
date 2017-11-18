from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES

pp = pprint.PrettyPrinter(indent=4)

nlp = StanfordCoreNLP('http://localhost:9000')

output = nlp.annotate(
    text="\n".join(InputReader(INPUT_FILES).read())[0],  # Use only the 1st
    properties={
      'annotators': 'tokenize,ssplit,pos,depparse,parse',
      'outputFormat': 'json'
    }
)

if "CoreNLP request timed out" in output:
    print("CoreNLP request timed out. Your document may be too long.")
else:
    sampleTree = output['sentences'][0]['parse']
    print parseTree(sampleTree)
