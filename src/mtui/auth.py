from cryptography.fernet import Fernet, MultiFernet
from base64 import b85encode, b85decode
from pathlib import Path

from .types import Namespace
from .utils import buildDir


def genToken() -> tuple[Fernet, bytes]:
    """
    Generates a Fernet object and a token,
    and then returns both

    Yields
    ------
    tuple
        Tuple of a Fernet object and a token,
        in respective order
    """
    token = Fernet.generate_key()
    yield Fernet(token), token.decode()


def getMultiFernet(config: Namespace = None, fernets: int = 5) -> MultiFernet:
    """
    Grabs the fernet tokens stored in a file and tries to make
    a `MultiFernet`, since it has the ability to be rotated

    Generates Fernet and MultiFernet obejcts if the
    file does not exist

    Parameters
    ----------
    config : Namespace, optional
        Config namespace, by default None
    fernets : int, optional
        Amount of fernets to generate
        if the file doesnt exist, by default 5

    Returns
    -------
    MultiFernet
        Rotatable `Fernet` object
    """
    metadata = config.Meta
    fernetPath = buildDir(
        "auth/keys.txt", metadata.app, metadata.author, metadata.version
    )

    # Generates a set of Fernet keys if it doesn't exist, else just read the file specified
    return (
        genMultiFernetFromFile(fernetPath)
        if fernetPath.exists()
        else genMultiFernet(config, fernets)
    )


def genMultiFernet(config: Namespace, fernets: int = 5) -> MultiFernet:
    """
    Generates a `MultiFernet` and dumps its tokens to a file

    Parameters
    ----------
    config : Namespace
        Config Namespace
    fernets : int, optional
        Fernets to generate, by default 5

    Returns
    -------
    MultiFernet
        Rotatable Fernet
    """
    res = []

    for _ in range(fernets):
        (obj, token) = next(genToken())
        res.append(obj)
        dumpToken(token, config.Meta)

    return MultiFernet(res)


def genMultiFernetFromFile(file: Path) -> MultiFernet:
    """
    Reads a file and builds a MultiFernet from there

    Parameters
    ----------
    file : Path
        Path to token file

    Returns
    -------
    MultiFernet
        Rotatable Fernet
    """
    rawFernets = file.read_text().splitlines(False)
    return MultiFernet(map(lambda raw: Fernet(raw), rawFernets))


def dumpToken(token: str, metadata: Namespace):
    """
    Dumps a token to a file, which will be determined by the
    Metadata namespace

    Parameters
    ----------
    token : str
        Token to dump
    metadata : Namespace
        Meta namespace of the config file
    """
    with open(
        buildDir("auth/keys.txt", metadata.app, metadata.author, metadata.version),
        "a+",
    ) as f:
        content = f.readlines()
        content.append(token + "\n")

        f.writelines(content)


def encodeUserPassword(passwd: str | bytes | bytearray) -> str:
    """
    Encodes a password to Base85

    Parameters
    ----------
    passwd : str or bytes or bytearray
        Password to encode

    Returns
    -------
    str
        Base85-encoded password
    """
    passwd = passwd if isinstance(passwd, bytes | bytearray) else passwd.encode()
    return b85encode(passwd).decode()


def decodeUserPassword(passwd: str) -> str:
    """
    Decodes a Base85-encoded password

    Parameters
    ----------
    passwd : str
        Encoded password

    Returns
    -------
    str
        Decoded password
    """
    return b85decode(passwd.encode()).decode()
