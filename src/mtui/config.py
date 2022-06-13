from configparser import ConfigParser
from pathlib import Path
from .types import Namespace


def load(file: Path):
    """
    Loads a .ini (or a file of a similar format)
    file into a namespace

    Parameters
    ----------
    file : Path
        Path to config file

    Returns
    -------
    Namespace
        The `file` represented in a namespace
    """
    config = ConfigParser()

    config.read(file)

    return Namespace(
        **{
            section: Namespace(
                **{
                    header: toInt(config.get(section, header).strip('"'))
                    for header in config[section]
                }
            )
            for section in config.sections()
        }
    )


def toInt(num: str) -> int:
    """
    Tries to convert a string to an
    integer

    NOTE: Will return itself when the
    string cannot be converted

    Parameters
    ----------
    num : str
        String to cast

    Returns
    -------
    int
        `num` but its an integer
    """
    try:
        return int(num)
    except ValueError:
        return num
