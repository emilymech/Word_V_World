import pickle

from word_v_world.pmi_calc import make_pmi_data_frame

token_path = "/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/total_tokens.pkl"
freq_path = "/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/word_freq_dict.pkl"
cooc_path = "/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/b4_pair_cooc.pkl"

with open(token_path, 'rb') as pickle_file:
    total_tokens = pickle.load(pickle_file)

with open(freq_path, 'rb') as pickle_file2:
    word_freq_dict = pickle.load(pickle_file2)

with open(cooc_path, 'rb') as pickle_file3:
    pair2cooc_dict = pickle.load(pickle_file3)

# make pmi data frame
make_pmi_data_frame(word_freq_dict, pair2cooc_dict, total_tokens)
