from itertools import cycle
from contextlib import contextmanager

@contextmanager
def highlighted_text():
    print('\033[0;36m', end='')
    try:
        yield
    finally:
        print("\033[0;0m", end='')


def progress(iterator):
    cycling = cycle("⡇⣆⣤⣰⢸⠹⠛⠏")
    for element in iterator:
        print(next(cycling), end="\r")
        yield element
    print(" \r", end='')
