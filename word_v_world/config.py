from pathlib import Path


class RemoteDirs:
    root = Path('/media/research_data') / 'Word_V_World'
    runs = root / 'runs'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)


class Global:
    debug = False