import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import types
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plafi import functions as fc


def test_read_data():
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.csv"))
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.xlsx"))
    with pytest.raises(NameError):
        fc.read_data("a_non_readable_file.pdf")


def test_valid_function():
    assert fc.valid_function("sin(x)+cos(x)") == True
    assert fc.valid_function("constant_that_does_not_exist*x") == False


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
    answers = iter([name, str(value), name, str(value)])

    # using lambda statement for mocking
    monkeypatch.setattr('builtins.input', lambda name: next(answers))
    fc.add_constant()
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name))

    with pytest.raises(NameError):
        fc.add_constant()


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
    assert np.any(constants["name"].str.contains(name)) == False

    with pytest.raises(NameError):
        monkeypatch.setattr('builtins.input', lambda _: name)
        fc.delete_constant()


def test_constants_to_globals():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    name1 = "pippo1"
    fc.save_constants([[name1, 3]])
    fc.constants_to_globals()
    constants = fc.read_constants()
    assert np.any("pippo1" in fc.__dict__)


def test_plot_data(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    x_title, y_title = "a random title", "a second random title"
    fig = fc.plot_data(fc.read_data("data1.csv"), x_title, y_title)
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_generate_fitting_function():
    func1 = fc.generate_fitting_function("var1*sin(x)", 1)
    func2 = fc.generate_fitting_function("var1*sin(x)+var2", 2)
    func3 = fc.generate_fitting_function("var1*sin(x)+var3", 3)
    func4 = fc.generate_fitting_function("var1*sin(x)+var4", 4)
    func5 = fc.generate_fitting_function("var1*sin(x)+var5", 5)
    assert func5(0, 0, 0, 0, 0, 0) == func4(0, 0, 0, 0, 0)
    assert func3(0, 0, 0, 0) == func2(0, 0, 0)
    assert isinstance(func1, types.FunctionType)
    assert isinstance(func2, types.FunctionType)
    assert isinstance(func3, types.FunctionType)
    assert isinstance(func4, types.FunctionType)
    assert isinstance(func5, types.FunctionType)
    with pytest.raises(NameError):
        fc.generate_fitting_function("var1*sin(x)", 6)


def test_fit_data(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)
    data = fc.read_data("data2.xlsx", rows_to_skip=0)
    fit_func = fc.generate_fitting_function("var1*sin(x)", 1)
    x_title, y_title = "title1", "title2"
    popt, perr, fig = fc.fit_data(data, fit_func, x_label=x_title, y_label=y_title)
    assert abs(popt - 1) < 0.001
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_fitting_procedure(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)

    path, rows_to_skip, x_index, y_index = "data2.xlsx", str(0), str(0), str(1)
    num_par, fit_func = str(2), "var1*cos(x+var2)"
    x_title, y_title = "a random title", "a second random title"
    answers = iter([path, rows_to_skip, x_index, y_index, num_par, fit_func, x_title, y_title])
    monkeypatch.setattr('builtins.input', lambda path: next(answers))

    popt, perr, fig = fc.fitting_procedure()

    assert abs(abs(popt[0]) - 1) < 0.001
    assert abs(abs(popt[1]) - np.pi / 2) < 0.001
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_plot_data_verbose(monkeypatch):
    monkeypatch.setattr(plt, 'show', lambda: None)

    path, rows_to_skip, x_index, y_index = "data1.csv", str(0), str(0), str(1)
    x_title, y_title = "a random title", "a second random title"
    wrong_path = "file_does_not_exist.txt"
    answers = iter([path, rows_to_skip, x_index, y_index, x_title, y_title, wrong_path])
    monkeypatch.setattr('builtins.input', lambda path: next(answers))

    fig = fc.plot_data_verbose()
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title
    with pytest.raises(NameError):
        fc.plot_data_verbose()


def test_print_constants():
    table = fc.print_constants()
    assert isinstance(table, str)
