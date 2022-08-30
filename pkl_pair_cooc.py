import sqlite3
import pickle

from data import con_fe_sent

all_pair_list = con_fe_sent.con_fe_sent

# open connection to cooc database
db_name = 'sent_f7.sqlite'
conn = sqlite3.connect(db_name)
c = conn.cursor()


def get_pair2cooc():
    print("Getting pair2cooc...")
    command = 'select * from cfs where w1 = (?) and w2 = (?)'
    pair2cooc = {}
    for pair in all_pair_list:
        # print(pair)
        pair2cooc[pair] = sum([row[2] for row in c.execute(command, pair).fetchall()])
    print("cooc dict:", pair2cooc)
    pair2cooc[pair] = [pair2cooc[pair].append(0) if pair2cooc[pair] == [] in pair2cooc else pair2cooc[pair]]
    print("cooc dict:", pair2cooc)
    return pair2cooc


if __name__ == '__main__':
    cooc_dict = get_pair2cooc()
    pickle.dump(cooc_dict, open("/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/sentf7_cooc_08.14.22.pkl", "wb"))
