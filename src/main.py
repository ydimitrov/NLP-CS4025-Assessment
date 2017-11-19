#!/usr/bin/env python
"""
Sentiment classification system based on sentiment composition.
"""
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import lexicon
import classifier
import parser


def analyse_sentence(**kwargs):
    """
    Prints the result of sentement analys for sentence.
    """
    polarity = classifier.polarity(**kwargs)

    if polarity > 0:
        result = "Positive"
    elif polarity < 0:
        result = "Negative"
    else:
        result = "Neutral"

    print("\n\nSentence:\n{}\n"
          "\nResult:   {}"
          "\nNLTK Analyzer: {}".format(
            kwargs['sentence'], result,
            nltk_analyser.polarity_scores(sentence))
    )


if __name__ == "__main__":

    # Connect to CoreNLP
    print("Connecting to parser...")
    prsr = parser.Parser()
    positive_words = lexicon.positive_words()
    negative_words = lexicon.negative_words()
    negators = lexicon.negators()
    determiners = lexicon.determiners()

    nltk.download('vader_lexicon', quiet=True)
    nltk_analyser = SentimentIntensityAnalyzer()

    test_cases = {
        'positive': lexicon.positive_sentences,
        'negative': lexicon.negative_sentences
    }

    for case in test_cases:
        print("{1}\nAnalysing {0} sentences\n{1}".format(case, '=' * 30))
        for sentence in test_cases[case]():
            analyse_sentence(
                sentence=sentence,
                parser=prsr,
                positive_words=positive_words,
                negative_words=negative_words,
                negators=negators,
                determiners=determiners,
                nltk_analyser=nltk_analyser,
            )
