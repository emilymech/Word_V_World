"""
tokenize wikipedia articles using a custom spacy tokenizer.
do not name this module tokenizer.py as this name is reserved for Python functionality.
make sure to  do this once:
python -m spacy download en_core_web_sm
"""

import re
from spacy.lang.en import English
import spacy
from pathlib import Path
from typing import Dict, Optional

from word_v_world.articles import generate_articles


nlp = spacy.load('en_core_web_sm', disable = ['ner'])
# custom_re = re.compile(r'''[A-Za-z]+([-'])[A-Za-z.]+''')
# tokenizer = English().Defaults.create_tokenizer(nlp)  # tokenizer must be created this way
# tokenizer.token_match = custom_re.match
# nlp.tokenizer = tokenizer


def make_n2c2f(bodies_path: Path,
               num_docs: Optional[int] = None,
               stop_doc: Optional[int] = None
               ) -> Dict[str, Dict[str, int]]:

    # loop over articles, tokenizing each with custom tokenizer
    n = 0
    res = {}   # noun -> Dict[child, f]
    for doc in nlp.pipe(generate_articles(bodies_path)):
        nouns = [t for t in doc if t.pos_ == "NOUN"]  # list of spacy tokens
        for noun in nouns:
            for child in noun.children:
                if child.dep_ == 'amod':

                    # print
                    print(noun, child)

                    child2f = res.setdefault(noun.lower_, {})  # convert spacy token to string
                    if child not in child2f:
                        child2f[child.lower_] = 1  # convert spacy token to string
                    else:
                        child2f[child.lower_] += 1  # convert spacy token to string

        print(f'{n:>12,} / {num_docs:,}', flush=True) if n % 100 == 0 else None
        n += 1

        if stop_doc is not None:
            if n > stop_doc:
                break

    return res
