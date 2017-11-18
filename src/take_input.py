#!/usr/bin/env python

import os

class InputReader( object ):
    """This class reads sentences from input text files."""

    def __init__(self, input_files):
        """
        files - Path to input file(s).
        """

        # If only string is given - assume to be the path to single input file
        if isinstance(input_files, str):
            input_files = [input_files]

        self.input_files = input_files

    def read(self, input_files=None):
        """Read input files and return a list of all sentences"""

        data = list()

        if input_files is None:
            input_files = self.input_files

        for filename in input_files:
            if not os.path.isfile(filename):
                print("Erro: {} does not exist.".format(filename))

            with open(filename, 'r') as file_obj:
                data = file_obj.read()

            data = [x.strip().replace(' .', '.') for x in data.split('\n')]

        return data

if __name__ == "__main__":

    input_files = [
        "../Lexicons/nokia-neg.txt",
        "../Lexicons/nokia-pos.txt"
    ]

    # Print all sentences
    for line in InputReader(input_files).read():
        print(line)
