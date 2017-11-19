from pycorenlp import StanfordCoreNLP
import nltk

class Parser(object):
    """
    This class enables the interation with StanfordCoreNLP
    """

    def __init__(self, address="http://localhost:9000"):
        self.server = StanfordCoreNLP(address)

    def parse_tree(self, text):
        output = self.server.annotate(
            text=text,
            properties={
              'annotators': 'tokenize,ssplit,pos,depparse,parse',
              'outputFormat': 'json'
            }
        )

        if "CoreNLP request timed out" in output:
            print("CoreNLP request timed out. Your document may be too long.")
            exit(-1)

        return nltk.Tree.fromstring(output['sentences'][0]['parse'])
