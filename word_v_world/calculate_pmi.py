import re
import numpy as np
from datetime import datetime
import sqlite3

from word_v_world import config

total_words_in_wiki = 2112763117

# open connection to database
db_name = 'forward_ws4_isfeatures.sqlite'
conn = sqlite3.connect(db_name)
c = conn.cursor()


def get_word_freq():
    print("Getting word frequency...")
    with (config.Dirs.root / 'data' / 'wf_pairs_allwiki_20191118_15-54-35.txt').open('r') as file:
        before_comma = re.compile(r'[^,]+')
        after_comma = re.compile(r'(?<=\s).*')
        wf_dict = {}
        for line in file:
            word = re.search(before_comma, line).group(0)
            freq = re.search(after_comma, line).group(0)
            wf_dict.update({word: freq})
        return wf_dict


def get_pair_cf():
    print("Getting pair cf...")
    with (config.Dirs.root / 'output' / 'is_pairs_forward_20191120_09-00-20.txt').open('r') as file:
        inner_re = re.compile('\("([^"]+)", "([^"]+)"\)')
        cf_dict = {}
        for line in file:
            m = inner_re.search(line)
            cf = re.findall(r'\d+', line)
            word_1 = m.group(1)
            word_2 = m.group(2)
            pair = (word_1, word_2)
            cf_dict.update({pair: cf[0]})
    return cf_dict


def combine_wf_cf_dicts(wf_dict, cf_dict):
    wf_cf = {}
    print("Combining wf and cf dicts...")

    for w, f in wf_dict.items():
        for pair, cf in cf_dict.items():
            f1 = 0
            f2 = 0
            key = (pair[0], pair[1])
            if w == pair[0]:
                f1 += float(f)
                wf_cf.setdefault(key, []).append((f1, float(cf)))
            elif w == pair[1]:
                f2 += float(f)
                wf_cf.setdefault(key, []).append((f2, float(cf)))

    pop_wf_cf = {k: v for k, v in wf_cf.items() if len(v) == 2}

    print(pop_wf_cf)
    return pop_wf_cf


def pmi(pop_wf_cf, window_size, all_pair_list):
    # pmi = log(cf/(total_words_in_wiki* window_size) /
    # ((word_1)/(total_words_in_wiki* window_size) *
    # (word_2)/(total_words_in_wiki* window_size))

    print('Calculating pmi...')
    pmi_form = 'pmi_all_features_concepts_forward_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'output' / 'forward' / '{}.txt'.format(pmi_form)).open('w') as file:
        for k, v in pop_wf_cf.items():
            # print("    ", "word1:", k[0], "word2:", k[1], "word 1 freq:", v[0][0],
            #       'word 2 freq:', v[1][0], "pair cooc:", v[0][1])

            if v[0][1] == 0:
                pmi = 0

            else:
                prob_word1 = v[0][0] / (total_words_in_wiki * window_size)
                prob_word2 = v[1][0] / (total_words_in_wiki * window_size)
                prob_word1_word2 = v[0][1] / (total_words_in_wiki * window_size)
                print("     ", prob_word1, prob_word2, prob_word1_word2)
                pmi = np.log(prob_word1_word2 / (prob_word1 * prob_word2))

            pop_wf_cf[k].append(pmi)

        for k, v in pop_wf_cf.items():
            file.write('{0}, {1}\n'.format(k, v))
    return



