import sqlite3
from datetime import datetime

from data.pairs import act_pairs, adj_pairs, ass_pairs, curious_pairs, part_pairs
from word_v_world import config
from word_v_world.calculate_pmi import pmi, combine_wf_cf_dicts, get_word_freq, get_pair_cf

"""
WARNING:
A database is not like a dictionary.
A dictionary has a unique key and a value associated with that key.
A database on the other hand, simply consists of rows.
This means there can be multiple rows, each with the same content. 
That is okay. 
In our case, this means that the word-pair co-occurred the same number of times in one bodies.txt file
as it does in another bodies.txt file.
This must be considered when querying a single word-pair,
 because in many cases multiple rows exist for the same word-pair.

"""


def main():

    # open connection to database
    db_name = 'test.sqlite'  # TODO use multiple databases?
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # example 1: get all entries where word 1 = 'airplane'
    word_1 = ('airplane',)
    command = 'select * from cfs where w1 = (?)'
    for row in c.execute(command, word_1).fetchall():
        print(row)

    # example 2: get all entries where co-occurrence f = 2
    cf = (2,)
    command = 'select * from cfs where cf = (?)'
    for row in c.execute(command, cf).fetchall():
        print(row)

    # example 3: get mean co-occurrence frequency
    cf_sum = 0
    num_entries = 0
    command = 'select cf from cfs'
    for row in c.execute(command).fetchall():
        cf_sum += row[0]
        num_entries += 1
    print(f'mean co-occurrence frequency={cf_sum / num_entries:.2f}')

    # example 4: get co-occurrence frequency for a specific pair

    command = 'select * from cfs where w1 = (?) and w2 = (?)'
    filename = 'curious_is_' + datetime.now().strftime('%Y%m%d_%H-%M-%S')
    with (config.Dirs.root / 'output' / '{}.txt'.format(filename)).open('w') as f:
        for word_pair in curious_pairs.curious_is_query:
            cfs = [row[2] for row in c.execute(command, word_pair).fetchall()]
            pair_cooc = str(f'{word_pair}, {sum(cfs)}')
            print(f'Word-pair={word_pair} co-occur {sum(cfs)} times')

            # write the co-occurrence values to text file
            f.write(pair_cooc + '\n')

    # example 5: get PMI
    # change pmi_form in calculate_pmi to save more specific filename
    pmi(combine_wf_cf_dicts(get_word_freq(), get_pair_cf()), 4)


if __name__ == '__main__':
    main()
