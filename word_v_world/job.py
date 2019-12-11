import pickle
from pathlib import Path

from word_v_world.dependencies import make_n2c2f
from word_v_world.articles import get_text_file_path


def main(param2val):  # param2val appears auto-magically via Ludwig

    # params
    cwc_param_name = param2val['cwc_param_name']
    article_coverage = param2val['article_coverage']
    max_num_characters = param2val['max_num_characters']
    project_path = Path(param2val['project_path'])  # added by Ludwig
    save_path = Path(param2val['save_path'])  # all data that is saved must be saved here

    # step 1
    print('Tokenizing and finding dependencies...', flush=True)
    param_path = project_path.parent / 'CreateWikiCorpus' / 'runs' / cwc_param_name
    bodies_path = get_text_file_path(param_path, 'bodies')
    titles_path = get_text_file_path(param_path, 'titles')
    num_docs = len(titles_path.read_text().split('\n')) - 1  # "wc -l" says there is 1 less line
    stop_doc = int(num_docs * article_coverage)
    print(f'Number of articles in text file={num_docs}')
    n2c2f = make_n2c2f(bodies_path, num_docs,
                       stop_doc=stop_doc,
                       max_num_characters=max_num_characters,
                       )  # this also lower-cases

    # step 3 - save the dictionary containing co-occurrence frequencies to Ludwig-supplied save_path
    print('Saving dictionary to disk...')
    n2n2f_path = save_path / 'n2n2f.pkl'
    if not n2n2f_path.parent.exists():
        n2n2f_path.parent.mkdir(parents=True)
    pickle.dump(n2c2f, n2n2f_path.open('wb'))

    print('Done with user-portion of job. Ludwig will now move data to server. Hold tight...')
    return []
