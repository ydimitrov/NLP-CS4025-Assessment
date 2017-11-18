Sentiment Composition Lexicon for Negators, Modals, and Degree Adverbs (SCL-NMA)
Version 1.0
12 April 2016
Copyright (C) 2016 National Research Council Canada (NRC)
Contact: Saif Mohammad (saif.mohammad@nrc-cnrc.gc.ca)


***************************************
Terms of use
***************************************
1. This lexicon can be used freely for research purposes. 
2. The papers listed below provide details of the creation and use of the lexicon. If you use a lexicon, then please cite the associated papers.
3. If interested in commercial use of the lexicon, send email to the contact. 
4. If you use the lexicon in a product or application, then please credit the authors and NRC appropriately. Also, if you send us an email, we will be thrilled to know about how you have used the lexicon.
5. National Research Council Canada (NRC) disclaims any responsibility for the use of the lexicon and does not provide technical support. However, the contact listed above will be happy to respond to queries and clarifications.
6. Rather than redistributing the data, please direct interested parties to this page:
   http://www.saifmohammad.com/WebPages/SCL.html


Please feel free to send us an email:
- with feedback regarding the lexicon; 
- with information on how you have used the lexicon;
- if interested in having us analyze your data for sentiment, emotion, and other affectual information;
- if interested in a collaborative research project.


***************************************
General Description
***************************************

Sentiment Composition Lexicon for Negators, Modals, and Degree Adverbs (SCL-NMA) is a list of single words and multi-word phrases and their associations with positive and negative sentiment. Single words come from the list of positive and negative words collected by Osgood for his seminal study on word meaning, available in General Inquirer. The phrases are formed by combining an Osgood word and a modifier, where a modifier is a negator, an auxilary verb, a degree adverb, or a combination of those. The complete lists of negators, modals, and degree adverbs used in this lexicon are included into this distribution.

The sentiment associations were obtained manually through crowdsourcing using the Best-Worst Scaling annotation technique.


***************************************
SemEval-2016
***************************************

Parts of this lexicon were used as development and test sets for SemEval-2016 shared task on Determining Sentiment Intensity of English and Arabic Phrases (Task 7) -- General English Sentiment Modifiers Set (http://alt.qcri.org/semeval2016/task7/). All terms from SCL-NMA except the ones that were used in the previous competition (SemEval-2015 Task 10 Subtask E) were included into the SemEval-2016 dataset (2,999 terms). The sentiment association scores were converted into the range 0..1 for the SemEval competition. 



***************************************
File Format
***************************************

Each line in the file has the following format:

<term><tab><sentiment score>

where
<term> is a single word or a multi-word phrase; 
<sentiment score> is a real number between -1 and 1 indicating the degree of association of the term with positive sentiment.

There are 3,207 terms: 1,621 single words and 1,586 phrases.


***************************************
More Information
***************************************

Details on the process of creating the lexicon can be found in:

Svetlana Kiritchenko and Saif M. Mohammad (2016) The Effect of Negators, Modals, and Degree Adverbs on Sentiment Composition. Proceedings of the 7th Workshop on Computational Approaches to Subjectivity, Sentiment and Social Media Analysis (WASSA), San Diego, California, 2016.




