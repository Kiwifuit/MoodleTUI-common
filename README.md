# MoodleTUI Common Library
Backend Library for the MoodleTUI project

***This package is used to interact with [my school's LMS](https://basic-ed.cit.edu) and is not intended for general use***

# Why this project is on PyPi
I placed the project on PyPi so that...
- I can isolate [my main code](https://github.com/kiwifuit/moodletui) from the backend code
  - This is useful to me because I am actually developing both at roughly the same time
- Easy deployment & distribution
  - If need be, I can package my main program into a small archive and distribute *that* and tell whoever is gonna run that to execute `pip install MoodleTUI-Common`

So yeah, this isn't really a package for everyone, but you can check out the code and maybe make a PR if you want to improve something