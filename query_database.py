import sqlite3

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

    # example 1: get all entries where word 1 = 'zebra'
    word_1 = ('zebra',)
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


if __name__ == '__main__':
    main()
