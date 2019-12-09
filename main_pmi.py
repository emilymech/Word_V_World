from word_v_world.calculate_pmi import make_pmi_data_frame, get_pair2cooc, get_word_freq, make_master_w2f
from word_v_world.params import param2requests


wiki_param_names = param2requests['cwc_param_name']

# get PMI
word_freq_dict = get_word_freq()
pair2cooc_dict = get_pair2cooc()
master_w2f = make_master_w2f(wiki_param_names)

make_pmi_data_frame(word_freq_dict, pair2cooc_dict, master_w2f)
