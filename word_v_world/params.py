
# pass unique integers to each machine to allow unique start_id
# all the values must be in a list
param2requests = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'input_file_name': ['enwiki-20190920-pages-articles-multistream.xml.bz2']}

param2default = {'part': 0,
                 'num_machines': 7,
                 'input_file_name': 'dummy_input.xml'}