from pathlib import Path
import sys
import os
import socket

if sys.platform == 'darwin':
    default_mnt_point = '/Volumes'
elif sys.platform == 'linux':
    default_mnt_point = '/media'
else:
    if not os.getenv('LUDWIG_MNT'):
        raise EnvironmentError('Missing LUDWIG_MNT environment variable')


class RemoteDirs:
    """
    remote directories are directories not hosted locally, but hosted on the Ludwig file server.
    the paths defined below are used:
    1. when jobs are run locally
    2. when jobs are run on Ludwig workers
    this means that the paths must be flexible depending on whether 1 or 2 is the case.
    on ludwig workers, research_data must always evaluate to /media/research_data.
    however, when run locally, research_data depends on where the file server is mounted.
    On MacOs for example, research_data evaluates to /Volumes/research_data.
    On a platform that is not Linux or MacOS, research_data is not automatically defined;
    Instead, the path to research_data must be manually specified in the environment variable LUDWIG_MNT.

    WARNING: never change the path definitions below.
    """
    mnt_point = os.getenv('LUDWIG_MNT', default_mnt_point)
    research_data = Path(mnt_point) / 'research_data'
    root = research_data / 'Word_V_World'
    runs = root / 'runs'


class LocalDirs:
    root = Path(__file__).parent.parent
    src = root / 'word_v_world'
    runs = root / '{}_runs'.format(src.name)

    # TODO this is a hack - use .env file and dot_env package to remedy

    if socket.gethostname() == 'wirelessprv-10-195-203-206.near.illinois.edu':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    elif socket.gethostname() == 'Emilys-MacBook-Pro.local':
        wiki = Path('/Volumes/GoogleDrive/My Drive/UIUC/PyCharm') / 'CreateWikiCorpus'
    else:
        wiki = Path('/home/ph/CreateWikiCorpus')


class Global:
    debug = False
