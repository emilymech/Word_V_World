"""
tokenize wikipedia articles using a custom spacy tokenizer.
do not name this module tokenizer.py as this name is reserved for Python functionality.

make sure to  do this once:
python -m spacy download en_core_web_sm
"""

import spacy
from spacy.tokens import Doc

from word_v_world.articles import generate_articles


NUM_ARTICLES = 100


class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)


# make a custom tokenizer
nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = WhitespaceTokenizer(nlp.vocab)

# loop over articles, tokenizing each
for article in generate_articles(num_articles=NUM_ARTICLES):

    # tokenize article
    doc = nlp(article)  # tokenization, tagging, ner, etc...

    print([t.text for t in doc])
    print()