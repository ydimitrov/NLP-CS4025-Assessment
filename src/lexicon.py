#!/usr/bin/env python

import os
import re


POSITIVE_WORDS = '../Lexicons/positive-words.txt'
NEGATIVE_WORDS = '../Lexicons/negative-words.txt'
NEGATORS = '../Lexicons/negators.txt'
DETERMINERS = '../Lexicons/negators.txt'

NEGATIVE_SENTENCES = [
    "../Lexicons/nokia-neg.txt"
]

POSITIVE_SENTENCES = [
    "../Lexicons/nokia-pos.txt"
]


def positive_sentences():
    """
    Returns a list of positive sentences.
    """
    return parse_text_files(POSITIVE_SENTENCES)


def negative_sentences():
    """
    Returns a list of negative sentences.
    """
    return parse_text_files(NEGATIVE_SENTENCES)


def positive_words():
    """
    Returns a list of positive words.
    """
    return parse_words(POSITIVE_WORDS)


def negative_words():
    """
    Returns a list of negative words.
    """
    return parse_words(NEGATIVE_WORDS)


def negators():
    """
    Returns a list of negations.
    """
    return parse_words(NEGATORS)

def determiners():
    """
    Returns a list of determiners.
    """
    return parse_words(DETERMINERS)


def parse_words(filename):
    """
    Read text file and returns a list with words.
    """
    with open(filename, 'r') as f_obj:
        data = f_obj.read()
    return re.findall(r"[A-z\-]+", data)


def parse_text_files(files_list):

    data = list()

    for filename in files_list:
        if not os.path.isfile(filename):
            print("Error: {} does not exist.".format(filename))

        with open(filename, 'r') as file_obj:
            text = file_obj.read()

        text = ' '.join(text.split(' '))  # Remove unnececary white space
        data += [x.strip() for x in text.split('\n') if x]

    return data
