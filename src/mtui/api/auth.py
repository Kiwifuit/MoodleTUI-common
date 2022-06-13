from requests import Session
from bs4 import BeautifulSoup
from pathurl import Query, URL

from ..types import Namespace
from .entities import _BeautifulSoupTag


def getLoginPage(sess: Session, page: str) -> dict:
    """
    Scrapes the login page and return the login form

    Parameters
    ----------
    sess : Session
        Session to use
    page : str
        _description_

    Returns
    -------
    dict
        Result along with misc. stats for logging
    """
    resp = sess.get(page)
    parser = BeautifulSoup(resp.text, "html.parser")

    return {
        "result": parser.find("form", {"id": "login"}),
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def buildPayload(html: _BeautifulSoupTag, username: str, password: str) -> dict:
    """
    Scrapes the login form and builds a payload

    Parameters
    ----------
    html : _BeautifulSoupTag
        Login form
    username : str
        Username to use
    password : str
        Password to use

    Returns
    -------
    dict
        Payload generated
    """
    res = {"anchor": "", "username": username, "password": password}

    res.update(
        logintoken=html.find("input", {"type": "hidden", "name": "logintoken"}).get(
            "value"
        )
    )

    return res


def getSesskey(sess: Session, config: Namespace) -> dict:
    """
    Grabs the session key

    Parameters
    ----------
    sess : Session
        Session to use
    config : Namespace
        Config namespace

    Returns
    -------
    dict
        Session key along with misc. stats for logging
    """
    url = config.URL.home
    resp = sess.get(url)
    parser = BeautifulSoup(resp.text, "html.parser")

    return {
        "result": parser.find("input", {"id": "sesskey", "type": "hidden"}).get("value"),
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def login(sess: Session, user: str, passwd: str, config: Namespace):
    """
    Log into the website

    Parameters
    ----------
    sess : Session
        Session to use
    user : str
        Username
    passwd : str
        Password
    config : Namespace
        Config namespace

    Returns
    -------
    dict
        Login page along with misc. stats for logging
    """
    url = config.URL.login
    page = getLoginPage(sess, url)
    payload = buildPayload(page.get("result"), user, passwd)

    resp = sess.post(url, data=payload)

    return {
        "getLoginPage": page.get("stats"),
        "login": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def logout(sess: Session, config: Namespace) -> dict:
    """
    Logs out of the website

    Parameters
    ----------
    sess : Session
        Session to use
    config : Namespace
        Config Namespace

    Returns
    -------
    dict
        Session key along with misc. stats for logging
    """
    url = URL(config.URL.logout)
    sessionKey = getSesskey(sess, config)
    payload = Query().add(sesskey=sessionKey.get("result"))
    url = url.replace(query=payload)

    resp = sess.get(url)
    return {
        "getSesskey": sessionKey.get("stats"),
        "logout": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }
