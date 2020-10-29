'''
To Update:
    1. Update vocab name
    2. Update window size
    3. Update window type
'''


param2requests = {'cwc_param_name': ['param_107', 'param_108', 'param_109', 'param_110', 'param_111', 'param_112'],
                  'num_machines': [6],
                  'window_size': [7],
                  'window_type': ['forward'],
                  'vocab_name': ['concept_feature_10.20.20'],
                  'article_coverage': [1.0],
                  }


param2default = {
    'cwc_param_name': 'param_22',
    'num_machines': 1,
    'window_size': 7,
    'window_weight': 'flat',
    'window_type': 'forward',
    'vocab_name': 'vocab',
    'article_coverage': 0.1,  # percent of articles used; 0.1 results in 1GB pickle file with window-size=7
}

param2debug = {
    'cwc_param_name': 'param_0',
    'num_machines': 1,
    'window_size': 2,
    'window_weight': 'flat',
    'window_type': 'forward',
    'vocab_name': 'debug',
    'article_coverage': 1.0,

}


# some hard constraints specific to creating Wikipedia corpora on Ludwig
if len(param2requests['cwc_param_name']) != param2requests['num_machines'][0]:
    raise ValueError('"num_machines" must match length of "part".')

if len(param2requests['num_machines']) != 1:
    raise ValueError('It does not make sense to vary "num_machines" across jobs')
