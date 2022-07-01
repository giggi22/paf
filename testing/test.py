import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import types
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plafi import functions as fc

"""
These are the testing functions, which are focused on plafi/functions.py.
Note that for some functions, monkeypatch has been used.
Monkeypatch allows to 'simulate' the user input or avoid the blocking of the program
due to some operations, i.e. the function show() from the matplotlib library
create a window that will freeze the testing procedure, unless it is closed manually. 
"""

def test_read_data():
    """
    data1.txt, data1.csv and data1.xlsx are three handwritten file containing the same data.
    The function check if, once they are read they are the same, and if an error is raised
    when the file can not be read.
    """
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.csv"))
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.xlsx"))
    with pytest.raises(NameError):
        fc.read_data("a_non_readable_file.pdf")


def test_valid_function():
    """
    This function will assert that fc.valid_function() can
    recognize a usable function and a not valid one.
    """
    assert fc.valid_function("pi*sin(x)+cos(x)") == True
    assert fc.valid_function("constant_that_does_not_exist*x") == False


def test_save_constants():
    """
    This function will check that fc.save_constants() works properly.
    It will delete the actual constants file and save a new empty one using the function under test.
    If the file is saved correctly (so it exists) the test is passed.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.save_constants(None)
    assert os.path.exists(constants_file_path)


def test_initialize_constants():
    """
    This function will check that fc.initialize_constants() works properly.
    It will delete the actual constants file and initialize a new one using the function under test.
    If the file exists the test is passed.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()
    assert os.path.exists(constants_file_path)


def test_read_constants():
    """
    This function check the proper behaviour of fc.read_constants().
    The actual constants file will be deleted and a new one is created with two constants.
    The test is passed if when reading the constants, they exist.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    name1, name2 = "a random name", ""
    fc.save_constants([[name1, 3], [name2, np.nan]])
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name1))
    assert np.any(constants["name"].str.contains(name2))


def test_add_constant(monkeypatch):
    """
    This function tests the correct behaviour of fc.add_constant().
    It will first delete the constants file and then create a new empty one.
    Monkeypatch is then set with the simulated input: first it will insert a new constant
    and then will try to add an existing one to raise an error.
    The test is passed if the first constant is added correctly and the second one raise an error.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()

    # monkeypatch setting
    name = 'value_name'
    value = 100
    answers = iter([name, str(value), name, str(value)])  # name is inserted also the second time
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    fc.add_constant()
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name))

    with pytest.raises(NameError):
        fc.add_constant()


def test_delete_constant(monkeypatch):
    """
    This function tests the correct behaviour of fc.delete_constant().
    It will first delete the constants file and then create a new one with a constant.
    Monkeypatch is then set with the simulated input: it will try twice to eliminate that constant.
    The test is passed if the constant is deleted at the first try and an error occurs at the second one.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()

    # setting monkeypatch
    name = 'value_name'
    value = 100
    monkeypatch.setattr('builtins.input', lambda _: name)

    # saving a constant
    fc.save_constants([[name, value]])

    fc.delete_constant()
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name)) == False

    with pytest.raises(NameError):
        fc.delete_constant()


def test_constants_to_globals():
    """
    This function tests the correct behaviour of fc.constants_to_globals().
    It will first delete the constants file and then create a new one with a constant.
    The test is passed if the constant can be found in fc.__dict__
    so it is usable when calling fc.generate_fitting_function().
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)

    # saving a constant
    name1 = "pippo1"
    fc.save_constants([[name1, 3]])

    fc.constants_to_globals()
    assert np.any("pippo1" in fc.__dict__)


def test_plot_data(monkeypatch):
    """
    This function tests the correct behaviour of fc.plot_data().
    It will call plot_data() and check if the titles are the ones set.
    Monkeypatch is used to not show the plot window and so not freezing the testing procedure.
    """
    # setting monkeypatch
    monkeypatch.setattr(plt, 'show', lambda: None)

    x_title, y_title = "a random title", "a second random title"
    fig = fc.plot_data(fc.read_data("data1.csv"), x_title, y_title)
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_generate_fitting_function():
    """
    This function tests the correct behaviour of fc.generate_fitting_function().
    It will create five different fitting function with different numbers of parameters.
    The test is passed if all the functions are types.FunctionType.
    An assert about one point of the function is used in order to reach the 100% coverage of functions.py.
    """
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
    """
    This function tests the correct behaviour of fc.fit_data().
    Monkeypatch is used to not show the plot window and so not freezing the testing procedure and simulate the inputs.
    It will try to fit data2.xlsx, where there are simple data.
    The test is passed if the fit returns the correct fitting value and the plot titles are correct
    """
    # setting monkeypatch
    monkeypatch.setattr(plt, 'show', lambda: None)

    # fitting and plotting parameters
    data = fc.read_data("data2.xlsx", rows_to_skip=0)
    fit_func = fc.generate_fitting_function("var1*sin(x)", 1)
    x_title, y_title = "title1", "title2"

    popt, perr, fig = fc.fit_data(data, fit_func, x_label=x_title, y_label=y_title)
    assert abs(popt - 1) < 0.001
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_fitting_procedure(monkeypatch):
    """
    This function tests the correct behaviour of fc.fitting_procedure().
    Monkeypatch is used to not show the plot window and so not freezing the testing procedure and simulate the inputs.
    It will run fc.fitting_procedure() two times: the first time to check if the fitting values and the titles are
    correct; the second time to check if an error is raised when passing a wrong path.
    """
    # setting monkeypatch for not showing the plot
    monkeypatch.setattr(plt, 'show', lambda: None)

    # setting monkeypatch for the inputs
    path, rows_to_skip, x_index, y_index = "data2.xlsx", str(0), str(0), str(1)
    num_par, fit_func = str(2), "var1*cos(x+var2)"
    x_title, y_title = "a random title", "a second random title"
    wrong_path = "file_does_not_exist.txt"
    answers = iter([path, rows_to_skip, x_index, y_index, num_par, fit_func, x_title, y_title, wrong_path])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    popt, perr, fig = fc.fitting_procedure()

    assert abs(abs(popt[0]) - 1) < 0.001
    assert abs(abs(popt[1]) - np.pi / 2) < 0.001
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title
    with pytest.raises(NameError):
        fc.fitting_procedure()


def test_plot_data_verbose(monkeypatch):
    """
    This function tests the correct behaviour of fc.plot_data_verbose().
    Monkeypatch is used to not show the plot window and so not freezing the testing procedure and simulate the inputs.
    It will run fc.fitting_procedure() two times: the first time to check if the titles are
    correct; the second time to check if an error is raised when passing a wrong path.
    """
    monkeypatch.setattr(plt, 'show', lambda: None)

    path, rows_to_skip, x_index, y_index = "data1.csv", str(0), str(0), str(1)
    x_title, y_title = "a random title", "a second random title"
    wrong_path = "file_does_not_exist.txt"
    answers = iter([path, rows_to_skip, x_index, y_index, x_title, y_title, wrong_path])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    fig = fc.plot_data_verbose()
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title
    with pytest.raises(NameError):
        fc.plot_data_verbose()


def test_print_constants():
    """
    This function tests the correct behaviour of fc.print_constants().
    The test is passed if fc.print_constants() return a string.
    """
    table = fc.print_constants()
    assert isinstance(table, str)
