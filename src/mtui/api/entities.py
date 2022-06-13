from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias
from bs4 import Tag, NavigableString

_BeautifulSoupTag: TypeAlias = Tag | NavigableString


@dataclass()
class Quiz:
    """
    Represents a quiz in the Moodle
    """

    id: int = None
    answered: bool = False
    score: tuple[int, int] = None


@dataclass()
class Lesson:
    """
    Represents a lesson in the Moodle
    """

    id: int = None
    content: list[str] = ...


@dataclass()
class Resource:
    """
    Represents a resource in the Moodle
    """

    id: int = None
    type: str = ...


@dataclass()
class Assignment:
    """
    Represents an assignment in the Moodle
    """

    id: int = None
    submissionStatus: str = ...
    gradingStatus: str = ...
    content: list[str] = ...


class CourseItem(Enum):
    """
    Items in the course
    """

    NULL = None
    QUIZ = Quiz
    LESSON = Lesson
    RESOURCE = Resource
    ASSIGNMENT = Assignment


_CourseContents: TypeAlias = list[Quiz | Lesson | Resource | Assignment]


@dataclass()
class Course:
    """
    Represents a course
    """

    id: int = None
    content: _CourseContents = ...
