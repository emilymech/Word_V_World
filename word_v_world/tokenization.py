"""
tokenize wikipedia articles using a custom spacy tokenizer.
do not name this module tokenizer.py as this name is reserved for Python functionality.
make sure to  do this once:
python -m spacy download en_core_web_sm
"""

import re
import spacy
from pathlib import Path
from typing import Generator, List

from word_v_world.articles import generate_articles
from spacy.tokenizer import Tokenizer

custom_nlp = spacy.load("en_core_web_sm", disable=['tagger', 'ner'])


def gen_tokenized_articles(paths_to_articles: List[Path],
                           num_articles: int = None,
                           ) -> Generator[List[str], None, None]:

    hyphen_contraction_re = re.compile(r"[A-Za-z]+(-|')[A-Za-z\.]+")
    prefix_re = spacy.util.compile_prefix_regex(custom_nlp.Defaults.prefixes)
    infix_re = spacy.util.compile_infix_regex(custom_nlp.Defaults.infixes)
    suffix_re = spacy.util.compile_suffix_regex(custom_nlp.Defaults.suffixes)
    custom_nlp.tokenizer = Tokenizer(custom_nlp.vocab,
                                     prefix_search=prefix_re.search,
                                     infix_finditer=infix_re.finditer,
                                     suffix_search=suffix_re.search,
                                     token_match=hyphen_contraction_re.match)

    # loop over articles, tokenizing each with custom tokenizer
    for article in generate_articles(paths_to_articles, num_articles=num_articles):
        doc = custom_nlp(article)
        tokens = [t.text.lower() for t in doc]
        yield tokens
