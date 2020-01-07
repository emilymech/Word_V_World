import pickle

from word_v_world.pmi_calc import make_pmi_data_frame, get_pair2cooc, get_word_freq_dict

pickle_path = "/Volumes/GoogleDrive/My Drive/UIUC/PyCharm/Word_V_World/data/total_tokens.pkl"

with open(pickle_path, 'rb') as pickle_file:
    total_tokens = pickle.load(pickle_file)

# get word freq
word_freq_dict = get_word_freq_dict()

# get PMI
pair2cooc_dict = get_pair2cooc()

# make pmi data frame
make_pmi_data_frame(word_freq_dict, pair2cooc_dict, total_tokens)
