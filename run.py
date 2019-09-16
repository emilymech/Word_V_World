from word_v_world.params import param2default

from word_v_world import job


param2val = param2default.copy()
param2val.update({'part': 0})
job.main(param2val)