from requests import Session
from bs4 import BeautifulSoup
from threading import Thread
from itertools import islice
from re import compile

from ..types import Namespace
from .entities import (
    Course,
    CourseItem,
    Assignment,
    Lesson,
    Quiz,
    _BeautifulSoupTag,
    _CourseContents,
)

ID_PARSER = compile("\d{1,}$")


def getCourse(sess: Session, course: Course, config: Namespace) -> dict:
    """
    Gets a course to scrape

    Parameters
    ----------
    sess : Session
        Session to use
    course : Course
        Course to scrape
    config : Namespace
        Config namespace

    Returns
    -------
    dict
        Contents of the course along with misc. stats for logging
    """
    resp = sess.get(config.Formats.course % course.id)
    scraper = BeautifulSoup(resp.text, "html.parser")

    return {
        "result": iter(scraper.find_all("div", {"class": "activityinstance"})),
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


# Why does this exist?
def get(sess: Session, url: str, output: dict = None):
    output = output or {}
    resp = sess.get(url)

    output = {
        "result": resp.text,
        "stats": {
            "responseCode": (resp.status_code, resp.reason),
            "elapsed": resp.elapsed,
        },
    }


def determineType(url: str) -> CourseItem:
    """
    Determines the type of item in a course

    Parameters
    ----------
    url : str
        URL to guess

    Returns
    -------
    CourseItem
        What `url` is
    """
    if "quiz" in url:
        return CourseItem.QUIZ
    elif "page" in url:
        return CourseItem.LESSON
    elif "assign" in url:
        return CourseItem.ASSIGNMENT


def parseCourse(sess: Session, course: Course, config: Namespace) -> dict:
    """
    Parses a course and returns its children

    Parameters
    ----------
    sess : Session
        Session to use
    course : Course
        Course to scrape
    config : Namespace
        Config namespace

    Returns
    -------
    dict
        Course items along with misc. stats for logging
    """
    items = getCourse(sess, course, config)
    res: _CourseContents = []

    for tag in items.get("result"):
        # Type hinting
        tag: _BeautifulSoupTag = tag
        href = tag.find("a").get("href")

        itemID = ID_PARSER.search(href)
        itemID = int(str.join("", islice(itemID.string, *itemID.span())))

        cls = determineType(href).value

        res.append(cls(id=itemID))

    return {
        "result": res,
        "stats": items.get("stats"),
    }


# TODO
def getCourses(sess: Session, config: Namespace):
    resp = sess.get(config.URL.home)
