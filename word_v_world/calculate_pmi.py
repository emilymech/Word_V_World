import re
import numpy as np
from datetime import datetime
import sqlite3

from word_v_world import config

total_words_in_wiki = 2112763117


# open connection to database
db_name = 'summed_ws4_isfeatures.sqlite'  # TODO use multiple databases?
conn = sqlite3.connect(db_name)
c = conn.cursor()


def get_word_freq():
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
    command = 'select w1, w2, cf from cfs'
    cf_dict = {}
    print("Getting co-occurrences from database...")
    for row in c.execute(command).fetchall():
        w1 = row[0]
        w2 = row[1]
        cf = row[2]
        # print("w1:", w1, "w2:", w2, "cf:", cf)

        key = (w1, w2)
        # print("key:", key)

        cf_dict.setdefault(key, []).append(float(cf))
    print(cf_dict)
    return cf_dict


def sum_cf(cf_dict):
    for pair, cf in cf_dict.items():
        cf_dict[pair] = sum(cf)
        # print("summed cf:", cf_dict[pair])
    summed_cf_dict = cf_dict
    return summed_cf_dict


def combine_wf_cf_dicts(wf_dict, summed_cf_dict): # TODO: speed this up
    wf_cf = {}
    print("Combining wf and cf dicts...")

    for w, f in wf_dict.items():
        for pair, cf in summed_cf_dict.items():
            f1 = 0
            f2 = 0
            # print("cf:", cf)
            # print(pair[0], pair[1], cf)
            if w == pair[0]:
                key = (pair[0], pair[1])
                f1 += float(f)
                wf_cf.setdefault(key, []).append((f1, cf))
            elif w == pair[1]:
                key = (pair[0], pair[1])
                f2 += float(f)
                wf_cf.setdefault(key, []).append((f2, cf))

    print(wf_cf)
    return wf_cf


def pmi(wf_cf, window_size):
    # pmi = math.log10(cf / (window_size * word_1 * word_2))
    print('Calculating pmi...')
    pmi_form = 'pmi_ass_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'output' / '{}.txt'.format(pmi_form)).open('w') as file:
        for k, v in wf_cf.items():
            print(k, v)
            print("    ", "word1:", k[0], "word2:", k[1], "word 1 freq:", v[0][0],
                  'word 2 freq:', v[1][0], "pair cooc:", v[0][1])

            if v[0][1] == 0:
                pmi = 0
            else:
                prob_word1 = v[0][0] / total_words_in_wiki * window_size
                prob_word2 = v[1][0] / total_words_in_wiki * window_size
                prob_word1_word2 = v[0][1] / total_words_in_wiki * window_size
                print("     ", prob_word1, prob_word2, prob_word1_word2)
                pmi = np.log(prob_word1_word2 / (prob_word1 * prob_word2))
            wf_cf[k].append(pmi)

        for k, v in wf_cf.items():
            file.write('{0}, {1}\n'.format(k, v))
    return



