# Sentiment Composition - NLP-CS4025-Assessment
Sentiment classification of gramatical constituents

## Setup
- Download [CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html)

    ```
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2017-06-09.zip
    ```

- Unzip

    ```
    unzip stanford-corenlp-full-2017-06-09.zip
    ```

- Enter the newly unzipped directory

    ```
    cd stanford-corenlp-full-2017-06-09
    ```

- Run the CoreNLP server

    ```
    java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
    ```


- Install [py-corenlp](https://github.com/smilli/py-corenlp) and [nltk](https://nltk.org)

    ```
    pip install pycorenlp
    pip install nltk
    ```

