from pathlib import Path
import os


class LocalDirs:
    root = Path(__file__).parent.parent
    data = root / 'data'

    if not data.exists():
        data.mkdir()

    research_data = Path('/') / 'Volumes' / 'research_data'  # needed by ludwig Python API to retrieve results
    if 'LUDWIG_MNT' in os.environ:
        research_data = os.environ["LUDWIG_MNT"]