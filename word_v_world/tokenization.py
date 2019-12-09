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
from typing import Generator, List, Optional

from word_v_world.articles import generate_articles


nlp = spacy.load('en_core_web_sm', disable = ['ner', 'tagger'])
custom_re = re.compile(r"[A-Za-z]+(-|')[A-Za-z\.]+")
tokenizer = English().Defaults.create_tokenizer(nlp)  # tokenizer must be created this way
tokenizer.token_match = custom_re.match
nlp.tokenizer = tokenizer


def gen_tokenized_articles(bodies_path: Path,
                           num_docs: Optional[int] = None,
                           ) -> Generator[List[str], None, None]:

    # loop over articles, tokenizing each with custom tokenizer
    n = 0
    for doc in nlp.pipe(generate_articles(bodies_path)):


        print(f'{n:>12,} / {num_docs:,}', flush=True) if n % 100 == 0 else None
        n += 1

        for noun_chunk in doc.noun_chunks:
            tokens = [t.lower_ for t in noun_chunk]
            yield tokens
