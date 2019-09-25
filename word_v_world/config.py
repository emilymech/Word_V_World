from pathlib import Path


class RemoteDirs:
    root = Path('/Volumes/research_data') / 'Word_V_World'
    runs = root / 'runs'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)


class Global:
    debug = False
    min_article_length = 1
    input = 'data/enwiki-20190920-pages-articles-multistream.xml.bz2'
    output = 'output'  # name of directory where output of wiki extractor script is saved
