from word_v_world import config
from word_v_world.calculate_pmi import pmi, combine_wf_cf_dicts, get_pair_cf, get_word_freq

# TODO - need to loop through the all_pair_list?

# example 5: get PMI
pair_cooc_dict = get_pair_cf()
word_freq_dict = get_word_freq()
combined_dict = combine_wf_cf_dicts(word_freq_dict, pair_cooc_dict)
all_pair_list = [open(config.Dirs.root / 'output' / 'all_feature_concept_combos_20191121_10-04-04.txt')]
pmi(combined_dict, 4, all_pair_list)
