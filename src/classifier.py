#!/usr/bin/env python

import nltk


def plot_tree_to_file(tree, filename):
    """
    Plot parse tree to image file.

    Usage:
        plot_tree_to_file(tree, 'image_name')
    Convert to png with:
        convert <filename>.ps <filename>.png
    """
    cf = nltk.draw.util.CanvasFrame()
    tc = nltk.draw.TreeWidget(cf.canvas(),tree)

    tc['node_font'] = 'arial 14 bold'
    tc['leaf_font'] = 'arial 14'
    tc['node_color'] = '#005990'
    tc['leaf_color'] = '#3F8F57'
    tc['line_color'] = '#175252'

    cf.add_widget(tc, 10, 10) # (10,10) offsets
    cf.print_to_file('{}.ps'.format(filename))
    cf.destroy()


def polarity(**kwargs):
    """
    This function returns a number in the range [-1, 1] which indicates
    polarity of a sentence.
    """

    tree = kwargs['parser'].parse_tree(kwargs['sentence'])

    phrases = parse_phrases(
        tree,
        kwargs['positive_words'],
        kwargs['negative_words'],
        kwargs['negators']
    )

    polarities = calculate_polarity(
        phrases,
        kwargs['positive_words'],
        kwargs['negative_words'],
        kwargs['determiners']
    )

    polarities = composition_model(polarities)

    sentiments = [pol[1] for pol in polarities]

    return sum(sentiments)  # -1 <= Negative < 0 = Neutral < Positive <= 1


def parse_phrases(tree, positive_words, negative_words, negators):
    phrases = []
    labels = {}

    for leaf in tree.subtrees():
        label = leaf.label()

        if not labels.has_key(label):
            labels[label] = list()

        labels[label].append(str(leaf[0]))

    for leaf in tree.subtrees():
        inversion = False
        phrase = []

        if leaf.label() == 'NP':
            for word in leaf.leaves():
                phrase.append(word)

            if not phrases:
                phrases.append(['NP'] + phrase)
            else:
                for listed_phrase in phrases:
                    if set(phrase) < set(listed_phrase):
                        break
                else:
                    phrases.append(['NP'] + phrase)

        elif leaf.label() == 'CC':

            for word in leaf.leaves():
                if (word in labels.get('CC', [])) and (word in negators):
                    phrase.append(word + '~')
                    inversion = True
                else:
                    phrase.append(word)

            if not phrases:
                phrases.append(['CC'] + phrase)
            else:
                for listed_phrase in phrases:
                    if (set(phrase)
                            - set(labels.get('VBD', []))
                            - set(labels.get('VB', []))
                            - set(labels.get('ADJP', []))
                            - set(labels.get('CC', []))) < set(listed_phrase):
                        break
                else:
                    phrases.append(['CC'] + phrase)

        elif leaf.label() == 'ADVP':

            for word in leaf.leaves():
                if word in labels.get('CC', []) and word in negators:
                    phrase.append(word + '~')
                    inversion = True
                else:
                    phrase.append(word)

            if not phrases:
                phrases.append(['ADVP'] + phrase)
            else:
                for listed_phrase in phrases:
                    if (set(phrase)
                            - set(labels.get('VBD', []))
                            - set(labels.get('VB', []))
                            - set(labels.get('ADJP', []))
                            - set(labels.get('CC', [])) < set(listed_phrase)):
                        break
                else:
                    phrases.append(['ADVP'] + phrase)


        elif leaf.label() == 'VP':

            for word in leaf.leaves():
                if word in negators:
                    word += '~'
                    inversion = True

                elif ((inversion == True)
                        and word in (positive_words + negative_words)
                        and word in (labels.get('JJ', [])
                             + labels.get('RB', [])
                             + labels.get('VB', [])
                             + labels.get('ADJP', [])
                             + labels.get('VBD', []))):
                    word += ' [~]'
                    inversion = False

                phrase.append(word)

            if not phrases:
                phrases.append(['VP'] + phrase)
            else:
                for listed_phrase in phrases:
                    if (set(phrase)
                           - set(labels.get('VBD', []))
                           - set(labels.get('VB', []))
                           - set(labels.get('ADJP', [])) < set(listed_phrase)):
                        break
                else:
                    phrases.append(['VP'] + phrase)

    return phrases


def word_polarity(word, positive_words, negative_words, determiners):
    """
    Returns polarity of a word.

    Where: 0 is Neutral; 1 is Positive; -1 is Negative;
    """

    if word in positive_words:
        return 1
    elif word in negative_words:
        return -1
    elif word in determiners:
        return 0
    return None


def calculate_polarity(phrases, positive_words, negative_words, determiners):
    """
    Calculates the polarity of each word in a phrase.

    Where: 0 is Neutral; 1 is Positive; -1 is Negative;
    """
    phrs_polarity = []

    for i, phrase in enumerate(phrases):
        polarities = [phrase[0]]

        for word in phrase[1:]:
            if len(word) <= 1:
                pol = 0

            else:
                pol = word_polarity(word,
                                        positive_words,
                                        negative_words,
                                        determiners)
            if pol is None and word == 'but~':
                    pol = 0
                    for x in range(0, i):
                        for y in range(1, len(phrs_polarity[x])):
                            phrs_polarity[x][y] = 0

            elif word.endswith('~'):
                pol = word_polarity(word[:-1],
                                        positive_words,
                                        negative_words,
                                        determiners)

            if pol is None and '<~>' in word:
                    pol = word_polarity(word[:-4],
                                            positive_words,
                                            negative_words,
                                            determiners)

            if pol is None:
                pol = 0

            polarities.append(pol)

        phrs_polarity.append(polarities)

    return phrs_polarity


def not_minimal_composition(polarities):
    """
    Returns True if the polarities could be grouped further and False otherwise.
    """
    for phrase in polarities:
        if isinstance(phrase[1], tuple) or len(phrase) > 2:
            return True
    return False


def composition_model(polarities):
    """
    Calculates sentiment polarities of pairs analogous to the principle of
    compositionality.
    """
    while(not_minimal_composition(polarities)):
        new_polarities = []

        for phrase in polarities:
            revised_phrase = [phrase[0]]
            for i in range(1,len(phrase),2):
                if (i+1 == len(phrase)):
                    revised_phrase.append(phrase[i])
                else:
                    revised_phrase.append(int(phrase[i]) + int(phrase[i+1]))
            new_polarities.append(revised_phrase)

        polarities = new_polarities

    return polarities
