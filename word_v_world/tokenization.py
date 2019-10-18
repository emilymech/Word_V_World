"""
tokenize wikipedia articles using a custom spacy tokenizer.
do not name this module tokenizer.py as this name is reserved for Python functionality.

make sure to  do this once:
python -m spacy download en_core_web_sm
"""

import re
import spacy


from word_v_world.articles import generate_articles, get_paths_to_articles
from word_v_world import config
from spacy.tokenizer import Tokenizer


def get_path(param2requests=config.Default.param2requests):
    paths_to_articles = []
    for p in get_paths_to_articles(param2requests):
        paths_to_articles.append(p)
    return paths_to_articles


def tokenize(n, paths_to_articles):
    all_tokens = []
    custom_nlp = spacy.load("en_core_web_sm")
    hyphen_contraction_re = re.compile(r"[A-Za-z]+(-|')[A-Za-z\.]+")
    prefix_re = spacy.util.compile_prefix_regex(custom_nlp.Defaults.prefixes)
    infix_re = spacy.util.compile_infix_regex(custom_nlp.Defaults.infixes)
    suffix_re = spacy.util.compile_suffix_regex(custom_nlp.Defaults.suffixes)
    custom_nlp.tokenizer = Tokenizer(custom_nlp.vocab,
                                     prefix_search=prefix_re.search,
                                     infix_finditer=infix_re.finditer,
                                     suffix_search=suffix_re.search,
                                     token_match=hyphen_contraction_re.match)

    # loop over articles, tokenizing each with built-in tokenizer
    i = 0  # for tracking print process
    for article in generate_articles(paths_to_articles, num_articles=n):

        # tokenize article
        doc = custom_nlp(article)  # tokenization, tagging, ner, etc...
        tokens = [t.text.lower() for t in doc]
        all_tokens += tokens

        # track print process
        i += 1
        if i % 100 == 0:
            print("Finished {} articles".format(i))

        # for debugging, print tokens in sample articles (only when num articles is small)
        # print(tokens)
        # print(len(tokens))
        # print()

    return all_tokens


# # retrieve a subset of articles using start and stop
# for article in generate_articles_from_slice(paths_to_articles, start=2, stop=3):
#
#     # tokenize article
#     doc = nlp(article)  # tokenization, tagging, ner, etc...
#
#     tokens = [t.text.lower() for t in doc]
#     print(tokens)
#     print(len(tokens))
#     print()
