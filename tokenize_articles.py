"""
tokenize wikipedia articles using a custom spacy tokenizer.
do not name this module tokenizer.py as this name is reserved for Python functionality.

make sure to  do this once:
python -m spacy download en_core_web_sm
"""

import spacy
from spacy.tokens import Doc

from word_v_world.articles import generate_articles, generate_articles_from_slice, get_paths_to_articles

NUM_ARTICLES = 1

nlp = spacy.load("en_core_web_sm")


class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        spaces = [True] * len(words)
        # All tokens 'own' a subsequent space character in this tokenizer
        return Doc(self.vocab, words=words, spaces=spaces)



PARAM2REQUESTS = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'num_machines': [7],
                  'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}
# user can overwrite default by overwriting None
# TODO need to ask Phil about how to change this from "None" the right way ^


paths_to_articles = []
for p in get_paths_to_articles(param2requests=PARAM2REQUESTS):
    paths_to_articles.append(p)


# loop over articles, tokenizing each with built-in tokenizer
for article in generate_articles(paths_to_articles, num_articles=NUM_ARTICLES):

    # tokenize article
    doc = nlp(article)  # tokenization, tagging, ner, etc...

    tokens = [t.text.strip('.').strip(',').strip(')').strip('(').strip('/').lower() for t in doc]
    print(tokens)
    print(len(tokens))
    print()


# make a custom tokenizer
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)

# loop over articles, tokenizing each
for article in generate_articles(paths_to_articles, num_articles=NUM_ARTICLES):

    # tokenize article
    doc = nlp(article)  # tokenization, tagging, ner, etc...

    tokens = [t.text.strip('.').strip(',').strip(')').strip('(').strip('/').lower() for t in doc]
    print(tokens)
    print(len(tokens))
    print()


# retrieve a subset of articles using start and stop
for article in generate_articles_from_slice(paths_to_articles, start=2, stop=3):

    # tokenize article
    doc = nlp(article)  # tokenization, tagging, ner, etc...

    tokens = [t.text.strip('.').strip(',').strip(')').strip('(').strip('/').lower() for t in doc]
    print(tokens)
    print(len(tokens))
    print()