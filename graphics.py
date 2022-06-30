from contextlib import contextmanager


@contextmanager
def highlighted_cyan_text():
    """
    Note
    ----
    This function will highlight an output written in the console
    """
    print('\033[0;36m', end='')
    try:
        yield
    finally:
        print("\033[0;0m", end='')

