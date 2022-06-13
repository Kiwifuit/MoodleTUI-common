from cryptography.fernet import MultiFernet


def encodePassword(key: MultiFernet, password: str) -> str:
    """
    Encrypts a password

    Parameters
    ----------
    key : MultiFernet
        Encryption key to use
    password : str
        Password

    Returns
    -------
    str
        Encrypted password
    """
    return key.encrypt(password.encode()).decode()


def decodePassword(key: MultiFernet, password: str) -> str:
    """
    Decrypts a password

    Parameters
    ----------
    key : MultiFernet
        Decryption key to use
    password : str
        Password

    Returns
    -------
    str
        Decrypted password
    """
    return key.decrypt(password.encode()).decode()
