from contextlib import contextmanager


@contextmanager
def highlighted_cyan_text():
    print('\033[0;36m', end='')
    try:
        yield
    finally:
        print("\033[0;0m", end='')

