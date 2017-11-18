from pycorenlp import StanfordCoreNLP
import pprint

from parseTree import parseTree
from take_input import InputReader, INPUT_FILES

pp = pprint.PrettyPrinter(indent=4)

nlp = StanfordCoreNLP('http://localhost:9000')

# Available Annotators:
#     - tokenize: Splits the text into roughly “words”.
#     - cleanxml: Remove xml tokens.
#     - ssplit: Splits a sequence of tokens into sentences.
#     - pos: Labels tokens with their POS tag.
#     - lemma: Generates the word lemmas for all tokens in the corpus.
#     - ner: Recognizes named (PERSON, LOCATION, ORGANIZATION, MISC),
#           numerical (MONEY, NUMBER, ORDINAL, PERCENT), and temporal
#           (DATE, TIME, DURATION, SET) entities.
#     - regexner: Rule-based NER over token sequences using Java regular
#           expressions.
#     - sentiment: Socher et al’s sentiment model. Attaches a binarized tree of
#           the sentence to the sentence level CoreMap.
#     - truecase: Recognizes the true case of tokens in text where this
#           information was lost, e.g., all upper case text.
#     - parse: Full syntactic analysis, using both the constituent and the
#           dependency representations.
#     - depparse: Syntactic dependency parser.
#     - dcoref: Pronominal and nominal coreference resolution.
#     - relation: Relation extractor find relations between two entities.
#     - natlog: Marks quantifier scope and token polarity, according to
#           natural logic semantics.
#     - quote: Deterministically picks out quotes delimited
#           by " or ' from a text.

output = nlp.annotate(
    text=InputReader(INPUT_FILES).read()[0],  # Use only the 1st
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
