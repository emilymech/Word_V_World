from pathlib import Path
import os


class Dirs:
    root = Path(__file__).parent.parent
    data = root / 'data'

    if not data.exists():
        data.mkdir()

    if 'LUDWIG_MNT' in os.environ:
        mnt_path = Path(os.environ["LUDWIG_MNT"])
    else:
        mnt_path = Path('/') / 'Volumes'

    print(f'Setting mount path to {mnt_path}')

    research_data = mnt_path / 'ludwig_data'  # needed by ludwig Python API to retrieve results
