from pathlib import Path
import socket


class LocalDirs:
    root = Path(__file__).parent.parent

    # TODO this is a hack - use .env file and dot_env package to remedy

    if socket.gethostname() == 'wirelessprv-10-195-203-206.near.illinois.edu':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    elif socket.gethostname() == 'Emilys-MacBook-Pro.local':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    else:
        wiki = Path('/home/ph/CreateWikiCorpus')


class Global:
    debug = False
