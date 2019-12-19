import pickle

from word_v_world.word_count import get_word_freq, get_total_token_count
from word_v_world.get_all_pair_list import get_all_pair_list

# save word freq dict to pickle file
word_freq_dict = get_word_freq()
pickle.dump(word_freq_dict, open("/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/word_freq_dict.pkl", "wb"))

# save all pair list to pickle file
all_pair_list = get_all_pair_list()
pickle.dump(all_pair_list, open("/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/all_pair_list.pkl", "wb"))


# get total words in wiki
total_tokens = get_total_token_count(word_freq_dict)
pickle.dump(total_tokens, open("/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/total_tokens.pkl", "wb"))
