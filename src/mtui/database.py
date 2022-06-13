from contextlib import suppress
from sqlite3 import OperationalError, connect

from .auth import encodeUserPassword, decodeUserPassword


class CredentialsDatabase:
    def __init__(self, file: str = ":memory:") -> None:
        """
        Creates a database tailored for storing
        usernames and passwords

        NOTE: Usernames and passwords MUST be 32 characters
        long or shorter

        Parameters
        ----------
        file : str, optional
            File to store the database, by default ":memory:"
        """
        self.connection = connect(file)
        self.database = connect(file)

        with suppress(OperationalError):
            self.database.execute(
                "CREATE TABLE creds (%s varchar(32), %s varchar(32))" % self.columns
            )

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def __exit__(self, *err):
        del self

    def __enter__(self):
        return self.database

    def __contains__(self, key: object):
        return key in list(self.getUsers()) if isinstance(key, str) else False

    @property
    def columns(self):
        """
        Returns the columns of the database

        Returns
        -------
        Tuple of strings
            The columns of the database
        """
        return ("Username", "Password")

    def put(self, user: str, passwd: str):
        """
        Adds a new entry to the database

        Password will be encrypted during the process

        Parameters
        ----------
        user : str
            Username
        passwd : str
            Password
        """
        self.database.execute(
            "INSERT INTO creds VALUES (?, ?)", (user, encodeUserPassword(passwd))
        )

    def get(self, user: str) -> tuple[str, str]:
        """
        Gets the username and password of a user

        Password will be decrypted during the process

        Parameters
        ----------
        user : str
            Username

        Returns
        -------
        Tuple of strings
            Username and decrypted password
        """
        name, passwd = self.database.execute(
            "SELECT Username, Password FROM creds WHERE Username = ?", (user,)
        ).fetchone()

        return name, decodeUserPassword(passwd)

    def getAll(self):
        """
        Gets all the usernames and passwords stored in the database

        Passwords will be decrypted in the process

        Yields
        ------
        Tuple of strings
            Username and decrypted password
        """
        for name, passwd in self.database.execute("SELECT Username, Password FROM creds"):
            yield name, decodeUserPassword(passwd)

    def getUsers(self):
        """
        Gets all the users currently stored in the database

        Yields
        ------
        str
            Usernames that are stored in the database
        """
        yield from self.database.execute("SELECT Username FROM creds")
