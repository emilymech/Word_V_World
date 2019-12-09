import numpy as np
import pandas as pd
import sqlite3

from word_v_world import config
from word_v_world.word_count import make_master_w2f
from data import adjective_list, concept_list

NUM_LUDWIG_WORKERS = 6


# open connection to database
db_name = 'noun_child_cooc.sqlite'
conn = sqlite3.connect(db_name)
c = conn.cursor()


def get_word_freq():
    # count all words
    # note: counting should use the same tokenizer used everywhere else in the project
    wiki_param_names = ['param_{}'.format(22 + i) for i in range(NUM_LUDWIG_WORKERS)]
    master_w2f = make_master_w2f(wiki_param_names)
    return master_w2f


def get_total_token_count(master_w2f):
    total_words_in_wiki = sum([master_w2f[k] for k in master_w2f])
    return total_words_in_wiki


def get_all_pair_list():
    full_concept_list = []
    full_adjective_list = []
    all_pair_list = []
    for line in concept_list.concept_list:
        concept = line.strip().strip('\n').strip()
        full_concept_list.append(concept)
    for line in adjective_list.adjective_list:
        adjective = line.strip().strip('\n').strip()
        full_adjective_list.append(adjective)
    for concept in full_concept_list:
        for adjective in full_adjective_list:
            all_pair_list.append((concept, adjective))
    return all_pair_list


def get_pair2cooc():
    command = 'select * from cfs where w1 = (?) and w2 = (?)'
    all_pair_list = get_all_pair_list()
    pair2cooc = {}
    for pair in all_pair_list:
        cooc = [row[2] for row in c.execute(command, pair).fetchall()]
        pair2cooc[pair] = cooc
    return pair2cooc


def make_pmi_data_frame(word_freq_dict, pair2cooc_dict,master_w2f):
    # pmi = log(cf/(total_words_in_wiki) /
    # ((word_1)/(total_words_in_wiki) *
    # (word_2)/(total_words_in_wiki))

    print('Calculating pmi...')
    total_tokens = get_total_token_count(master_w2f)
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    for pair in pair2cooc_dict:
        prob_word1_word2 = pair2cooc_dict[pair] / total_tokens

        w1, w2 = pair
        w1f = word_freq_dict[w1]
        w2f = word_freq_dict[w2]

        prob_word1 = w1f / total_tokens
        prob_word2 = w2f / total_tokens

        pmi = np.log(prob_word1_word2 / (prob_word1 * prob_word2))

        # collect the above into the columns
        col1.append(w1)
        col2.append(w2)
        col3.append(w1f)
        col4.append(w2f)
        col5.append(pair2cooc_dict[pair])
        col6.append(pmi)

    df = pd.DataFrame(data={
        'word1': col1,
        'word2': col2,
        'w1f': col3,
        'w2f': col4,
        'cf': col5,
        'pmi': col6
     })

    df.to_csv('pmi_dataframe.csv')
    return


