import numpy as np
import pandas as pd


window_size = 7
window_type = 'forward'
run_details = 'concept_feature_08.30.22'


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
    col9 = run_details

    for pair in pair2cooc_dict:
        if type(pair2cooc_dict[pair]) is list:
            pair2cooc_dict[pair] = int("".join(map(str, pair2cooc_dict[pair])))

        print("pair:", pair)
        print("cf:", pair2cooc_dict[pair])

        prob_word1_word2 = pair2cooc_dict[pair] / (total_tokens * window_size)

        w1, w2 = pair
        w1f = word_freq_dict[w1]
        w2f = word_freq_dict[w2]

        prob_word1 = w1f / (total_tokens * window_size)
        prob_word2 = w2f / (total_tokens * window_size)

        if prob_word2 == 0:
            pmi = "NA"
        elif prob_word1 == 0:
            pmi = "NA"
        elif prob_word1_word2 == 0:
            pmi = "NA"
        else:
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
        'window_type': col8,
        'run_details': col9
     })

    df.to_csv('08_30_22_pmi.csv')
    return