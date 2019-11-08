# TODO - add vocab name to keep track of which one to use

param2requests = {'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
                  'num_machines': [6],
                  'window_size': [7],
                  }


param2default = {
    'cwc_param_name': 'param_22',
    'num_machines': 1,
    'window_size': 1,
    'window_weight': 'flat',
    'window_type': 'forward',
    'vocab_name': 'default'
}

param2debug = {
    'cwc_param_name': 'param_0',
    'num_machines': 1,
    'window_size': 1,
    'window_weight': 'flat',
    'window_type': 'forward',
}


# some hard constraints specific to creating Wikipedia corpora on Ludwig
if len(param2requests['cwc_param_name']) != param2requests['num_machines'][0]:
    raise ValueError('"num_machines" must match length of "part".')

if len(param2requests['num_machines']) != 1:
    raise ValueError('It does not make sense to vary "num_machines" across jobs')