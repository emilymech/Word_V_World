import pickle
import sqlite3


MINIMAL = False
VERBOSE = True

pickle_path = "/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/word_freq_dict.p"

# create database
db_name = 'frequency.sqlite'
conn = sqlite3.connect(db_name)
c = conn.cursor()
try:
    c.execute('CREATE TABLE fs (w text, f integer)')  # changed this from cfs, make sure it's correct
except sqlite3.OperationalError:   # table already exists
    pass

# populate database
print("Loading word freq dict...")
f = pickle.load(open(pickle_path, "rb"))
try:
    wf_dict = pickle.load(f)
except MemoryError as e:
    raise MemoryError('Reached memory limit')
except KeyboardInterrupt:
    f.close()
    conn.close()
    raise KeyboardInterrupt

# add to database
print("Adding words and frequencies to database...")
for w, f in wf_dict.items():
    values = (w[0], f.item())  # f is numpy int32
    command = "INSERT INTO fs VALUES (?, ?)"
    if VERBOSE:
        print(values)
    c.execute(command, values)

conn.commit()  # save changes
conn.close()
print('Saved changes and closed database.')
