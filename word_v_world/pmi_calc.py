import numpy as np
import pandas as pd
import sqlite3
import pickle

window_size = 4
window_type = 'forward'
all_pair_list = pickle.load(open("/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/all_pair_list.p", "rb"))

# open connection to cooc database
db_name = 'forward_ws4.sqlite'
conn = sqlite3.connect(db_name)
c = conn.cursor()

# open connection to wf database
db_name2 = 'frequency.sqlite'
conn2 = sqlite3.connect(db_name2)
c2 = conn2.cursor()


def get_word_freq_dict():
    command = 'select * from fs where w1 = (?)'
    word_freq = {}
    for pair in all_pair_list:
        print(pair)
        freq = [row[1] for row in c2.execute(command, pair).fetchall()]
        print(freq)
        word_freq[pair] = freq
    return word_freq


def get_pair2cooc():
    command = 'select * from cfs where w1 = (?) and w2 = (?)'
    pair2cooc = {}
    for pair in all_pair_list:
        cooc = [row[2] for row in c.execute(command, pair).fetchall()]
        pair2cooc[pair] = cooc
    return pair2cooc


def make_pmi_data_frame(word_freq_dict, pair2cooc_dict, total_tokens):
    # pmi = log(cf/(total_words_in_wiki) /
    # ((word_1)/(total_words_in_wiki) *
    # (word_2)/(total_words_in_wiki))

    print('Calculating pmi...')
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = window_size
    col8 = window_type

    for pair in pair2cooc_dict:
        print("pair:", pair)
        print("cf:", pair2cooc_dict[pair])

        prob_word1_word2 = pair2cooc_dict[pair] / (total_tokens * window_size)

        w1, w2 = pair
        w1f = word_freq_dict[w1]
        w2f = word_freq_dict[w2]

        prob_word1 = w1f / (total_tokens * window_size)
        prob_word2 = w2f / (total_tokens * window_size)

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
        'pmi': col6,
        'window_size': col7,
        'window_type': col8
     })

    df.to_csv('pmi_dataframe_f4.csv')
    return
