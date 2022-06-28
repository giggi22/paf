import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plafi import functions as fc


def test_read_data():
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.csv"))
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.xlsx"))


def test_valid_function():
    assert fc.valid_function("sin(x)+cos(x)") == True


def test_save_constants():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.save_constants(None)
    assert os.path.exists(constants_file_path)


def test_initialize_constants():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()
    assert os.path.exists(constants_file_path)


def test_read_constants():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    name1, name2 = "a random name", ""
    fc.save_constants([[name1, 3], [name2, np.nan]])
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name1))
    assert np.any(constants["name"].str.contains(name2))


def test_add_constant(monkeypatch):
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()
    # provided inputs
    name = 'value_name'
    value = 100

    # creating iterator object
    answers = iter([name, str(value)])

    # using lambda statement for mocking
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fc.add_constant()
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name))


def test_delete_constant(monkeypatch):
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()
    # provided inputs
    name = 'value_name'
    value = 100

    # creating iterator object
    answers = iter([name, str(value)])

    # using lambda statement for mocking
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fc.add_constant()

    monkeypatch.setattr('builtins.input', lambda _: name)
    fc.delete_constant()
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name))==False

def test_constants_to_globals():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    name1 = "pippo1"
    fc.save_constants([[name1, 3]])
    fc.constants_to_globals()
    constants = fc.read_constants()
    assert np.any("pippo1" in fc.__dict__)

