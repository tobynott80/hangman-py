# Hangman Assessment

Assessment 1 for Computational Thinking
Cardiff Uni Nov 2021 - CM6114 - Student No. 21048229

## Installation

In order to run Hangman in online mode (recommended), [Requests](https://pypi.org/project/requests/) library needs to be installed for communicating with the api. This can be done with:
`pip install requests`
Hangman also uses `os` and `random`, but these are included in the standard python library, so these don't need to be installed.

## Running

Run the main python file with:
`python .\c21048229_main.py`

## Online Mode

Hangman uses the [Random Words API](https://github.com/mcnaveen/Random-Words-API) (MIT License) to get a random word and its definition. However, if the API can't be reached (e.g the api is offline, the correct libraries aren't installed, client is offline, ect), the game will resort to a backup list of words and definitions stored locally.
