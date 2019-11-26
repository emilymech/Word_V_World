from word_v_world.calculate_pmi import pmi, combine_wf_cf_dicts, get_pair_cf, get_word_freq

# get PMI
word_freq_dict = get_word_freq()
pair_cooc_dict = get_pair_cf()
combined_dict = combine_wf_cf_dicts(word_freq_dict, pair_cooc_dict)
pmi(combined_dict, 4)
