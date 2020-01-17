from data import adjective_list, concept_list


def get_all_pair_list():
    full_concept_list = []
    full_adjective_list = []
    all_pair_list = []
    for line in concept_list.concept_list:
        concept = line.strip().strip('\n').strip()
        full_concept_list.append(concept)
    for line in adjective_list.adjective_list:
        adjective = line.strip().strip('\n').strip()
        full_adjective_list.append(adjective)
    for concept in full_concept_list:
        for adjective in full_adjective_list:
            all_pair_list.append((concept, adjective))
    return all_pair_list

