from pathlib import Path


class RemoteDirs:
    root = Path('/Volumes/research_data') / 'Word_V_World' / 'runs'
    wiki_count = root / 'Wiki_Heads_Bodies' / 'counts'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    wiki_count = root / '{}_count'.format(src.name)


class Global:
    debug = False
    min_article_length = 10
    input = 'body_5655.txt'
    output = 'counts'  # name of directory where output of count script is stored
