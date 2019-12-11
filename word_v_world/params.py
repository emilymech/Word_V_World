

param2requests = {'cwc_param_name': ['param_22', 'param_23', 'param_24', 'param_25', 'param_26', 'param_27'],
                  'num_machines': [6],
                  'article_coverage': [1.0],
                  }


param2default = {
    'cwc_param_name': 'param_22',
    'num_machines': 1,
    'article_coverage': 1.0,  # percent of articles used; 0.1 results in 1GB pickle file with window-size=7
    'max_num_characters': 10 * 1000,  # average number of chars in English wiki ~ 4k
}

param2debug = {
    'cwc_param_name': 'param_00',
    'num_machines': 1,
    'article_coverage': 1.0,

}


# some hard constraints specific to creating Wikipedia corpora on Ludwig
if len(param2requests['cwc_param_name']) != param2requests['num_machines'][0]:
    raise ValueError('"num_machines" must match length of "part".')

if len(param2requests['num_machines']) != 1:
    raise ValueError('It does not make sense to vary "num_machines" across jobs')


