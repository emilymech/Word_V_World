import re
import math
import numpy as np
from datetime import datetime

from word_v_world import config


def get_word_freq():
    with (config.Dirs.root / 'data' / 'wf_pairs_20191114_11-29-38.txt').open('r') as file:
        before_comma = re.compile(r'[^,]+')
        after_comma = re.compile(r'(?<=\s).*')
        wf_dict = {}
        for line in file:
            word = re.search(before_comma, line).group(0)
            freq = re.search(after_comma, line).group(0)
            wf_dict.update({word: freq})
        return wf_dict


def get_pair_cf():
    with (config.Dirs.root / 'output' / 'curious_is_20191113_11-06-18.txt').open('r') as file:
        inner_re = re.compile("\('([^']+)', '([^']+)'\)")
        cf_dict = {}
        for line in file:
            m = inner_re.search(line)
            cf = re.search(r'.*\s*(\d+)', line).group(1)
            word_1 = m.group(1)
            word_2 = m.group(2)
            pair = (word_1, word_2)
            cf_dict.update({pair: cf})
        return cf_dict


def combine_wf_cf_dicts(wf_dict, cf_dict):
    wf_cf = {}
    for w, f in wf_dict.items():
        for pair, cf in cf_dict.items():
            f1 = 0
            f2 = 0
            if w == pair[0]:
                key = (pair[0], pair[1])
                f1 += float(f)
                wf_cf.setdefault(key, []).append((f1, float(cf)))
            elif w == pair[1]:
                key = (pair[0], pair[1])
                f2 += float(f)
                wf_cf.setdefault(key, []).append((f2, float(cf)))
    print(wf_cf)
    return wf_cf


def pmi(wf_cf, window_size):
    # pmi = math.log10(cf / (window_size * word_1 * word_2))
    pmi_form = 'pmi_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'output' / '{}.txt'.format(pmi_form)).open('w') as file:
        for k, v in wf_cf.items():
            print("word1:", k[0], "word2:", k[1], "word 1 freq:", v[0][0],
                  'word 2 freq:', v[1][0], "pair cooc:", v[0][1])
            if v[0][1] != 0:
                pmi = math.log10((v[0][1]) / (window_size * v[0][0] * v[1][0]))
                wf_cf.setdefault(k, []).append((pmi))
        for k, v in wf_cf.items():
            file.write('{0}, {1}\n'.format(k, v))
    return


def main():
    # get_word_freq()
    # get_pair_cf()
    # combine_wf_cf_dicts(get_word_freq(), get_pair_cf())
    pmi(combine_wf_cf_dicts(get_word_freq(), get_pair_cf()), 4)


main()
