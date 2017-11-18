from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES

pp = pprint.PrettyPrinter(indent=4)

nlp = StanfordCoreNLP('http://localhost:9000')

output = nlp.annotate(
<<<<<<< HEAD
    text="\n".join(InputReader(INPUT_FILES).read())[0],  # Use only the 1st
=======
    text=InputReader(INPUT_FILES).read()[0],  # Use only the 1st
>>>>>>> dc00abfd6cf30f3f4493c9669402ad67e04bdf66
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
