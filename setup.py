from setuptools import setup

with open("README.md") as f:
    longDesc = f.read()

setup(
    name="MoodleTUI-common",
    version="0.0.2",
    author="CarbonFodder",
    author_email="mahkiwi123@gmail.com",
    description="Backend Library for the MoodleTUI project",
    long_description=longDesc,
    url="https://github.com/kiwifuit/MoodleTUI-common",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir="src",
    license="Apache License 2.0",
)
