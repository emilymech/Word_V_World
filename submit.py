from pathlib import Path

from ludwigcluster.client import Client


# specify what parameters to use on each node
param2val_list = [{'part': 0}, {'part': 1}]

# submit
client = Client('Word_V_World')
client.submit(src_ps=[Path('src')],
              data_ps=[],
              param2val_list=param2val_list,
              reps=1,
              test=True,
              worker='bengio')