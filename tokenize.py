import spacy
from spacy.tokens import Doc

from word_v_world.articles import generate_articles


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
for article in generate_articles():

    # tokenize article
    doc = nlp(article)
    print([t.text for t in doc])
    raise SystemExit('Processed first article')