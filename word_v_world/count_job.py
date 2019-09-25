import operator

from word_v_world import count_config


class Args:
    input = count_config.Global.input
    output = count_config.Global.output


def get_bodies():
    bodies = count_config.RemoteDirs.wiki_count
    return bodies


def count_words_in_bodies(bodies):
    doc_dict = {}
    type_token_counts = [0, 0]

    for body in bodies:
        for doc in body:
            for words in doc:
                tokens = words.split(' ')

                length = len(tokens)

                for i in range(length):
                    tokens[i] = tokens[i].strip(',')
                    tokens[i] = tokens[i].strip('!')
                    tokens[i] = tokens[i].strip('?')
                    tokens[i] = tokens[i].strip('.')
                    tokens[i] = tokens[i].strip('"')
                    tokens[i] = tokens[i].strip(']')
                    tokens[i] = tokens[i].strip('[')
                    tokens[i] = tokens[i].strip('(')
                    tokens[i] = tokens[i].strip(')')
                    tokens[i] = tokens[i].strip(';')
                    tokens[i] = tokens[i].lower()

                    if tokens[i] not in doc_dict:
                        doc_dict[tokens[i]] = 1
                        type_token_counts[0] += 1
                    else:
                        doc_dict[tokens[i]] += 1

                    type_token_counts[1] += 1

    return doc_dict, type_token_counts


def sort_all_freqs_for_doc(doc_dict):
    sorted_freq_list = sorted(doc_dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_freq_list


def print_summary_info(bodies, doc_dict, type_token_count_dict):
    print("\nThis is the total number of docs, types, and tokens in the wiki output:")
    for i in range(len(bodies)):
        doc = bodies[i]
        num_docs = len(doc_dict[doc])
        current_type_token_counts = type_token_count_dict[doc]
        num_types = current_type_token_counts[0]
        num_tokens = current_type_token_counts[1]
        tt_ratio = num_types / num_tokens

        count_summary = [doc, num_docs, num_types, num_tokens, "{:0.3f}".format(tt_ratio)]
        print(count_summary)
    print()


def print_top_words(bodies, sorted_freq_list_dict, type_token_count_dict):
    print("\nHere are the top 10 words for each document:")
    for i in range(10):
        output_string = ""
        for j in range(len(bodies)):
            doc = bodies[j]
            sorted_freq_list = sorted_freq_list_dict[doc]
            freq_proportion = sorted_freq_list[i][1] / type_token_count_dict[doc][1]

            output_string += "{:16s} {:0.3f}    ".format(sorted_freq_list[i][0], freq_proportion)


def save_to_text(output_string, count_summary, param2val):
    param_p = count_config.RemoteDirs.wiki_count / param2val['param_name']
    if not param_p.is_dir():
        param_p.mkdir()
    out_counts_p = param_p / 'wiki_counts.txt'

    f1 = out_counts_p.open('w')

    for output_string, count_summary in zip(output_string, count_summary):
        f1.write(output_string + '\n' + count_summary)


def main(output_string, count_summary, param2val):  # param2val will be different on each machine

    part = param2val['part']
    num_machines = param2val['num_machines']
    print('Word_V_World: Starting counting with part={} and num_machines={}'.format(part, num_machines))

    # step 1
    print(output_string)

    # step 2

    # step 3: save to shared drive
    print('Word_V_World: saving counts to text...')
    save_to_text(output_string, count_summary)

    return []