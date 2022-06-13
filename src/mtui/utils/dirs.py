from pathlib import Path
from platformdirs import user_data_path


def buildDir(dir: str, app: str, author: str, version: str) -> Path:
    """
    Builds the directory where the program's data should be stored

    Would be somewhere in `~/.local/share/MoodleTUI/<version>/`
    on Linux, `%AppData%/MoodleTUI/<version>/` on Windows

    Every parameter here should be controled by the config

    Parameters
    ----------
    dir : str
        Directory to generate
    app : str
        App Name
    author : str
        Author
    version : str
        App Version

    Returns
    -------
    Path
        Path generated
    """
    base = user_data_path(app, author, version)
    res = base / dir

    for folder in res.parents[::-1]:
        if not folder.exists():
            folder.mkdir()

    return res
