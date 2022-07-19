import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import types
import pytest
from hypothesis import given
import hypothesis.extra.numpy as hen

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
    The function check, once they are read, if they are the same.
    """
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.csv"))
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.xlsx"))
    assert np.all(fc.read_data("data1.txt") == [[-5., 0.], [0., 1.], [2., 3.], [3.1, 4.5], [4., 120.]])


def test_read_data_error_raised():
    """
    This function check if an error is raised correctly when a not readable is passed to fc.read_data().
    """
    with pytest.raises(NameError):
        fc.read_data("a_not_readable_file.pdf")


def test_valid_function_true():
    """
    This function will assert that fc.valid_function() can recognize a usable function.
    """

    # the constant file is deleted and initialized in order to have "pi" and use it for the testing
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()

    assert fc.valid_function("pi*sin(x)+cos(x)") == True


def test_valid_function_false():
    """
    This function will assert that fc.valid_function() can recognize a not usable function.
    """

    # the constant file is initialized in order to be sure that "constant_that_does_not_exist" does not exist
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()

    assert fc.valid_function("constant_that_does_not_exist*x") == False


def test_save_constants():
    """
    This function will check that fc.save_constants() works properly.
    It will delete the actual constants file and save a new empty one using the function under test.
    If the saved file exists and contains the correct constant, the test is passed.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.save_constants(np.array([["test_const", 1.]]))
    assert os.path.exists(constants_file_path)
    assert np.all(fc.read_constants().to_numpy() == np.array([["test_const", 1.]], dtype=object))


def test_initialize_constants():
    """
    This function will check that fc.initialize_constants() works properly.
    It will delete the actual constants file and initialize a new one using the function under test.
    If the file exists and contains the correct constants the test is passed.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()
    assert os.path.exists(constants_file_path)
    assert np.all(fc.read_constants().to_numpy() ==
                  np.array([["pi", np.pi], ["e", np.e], ["euler_gamma", np.euler_gamma]], dtype=object))


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
    assert not os.path.exists(constants_file_path)
    fc.save_constants(np.array([[name1, 3], [name2, np.nan]]))
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name1))
    assert np.any(constants["name"].str.contains(name2))


def test_add_constant(monkeypatch):
    """
    This function tests the correct behaviour of fc.add_constant().
    It will first delete the constants file and then initialize a new one.
    Monkeypatch is then set with the simulated input: it will insert a new constant and its value.
    The test is passed if the first constant is added correctly.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()

    # monkeypatch setting
    name = 'value_name'
    value = 100
    answers = iter([name, str(value)])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    fc.add_constant()
    constants = fc.read_constants()
    assert np.any(constants["name"].str.contains(name))


def test_add_constant_error_raised(monkeypatch):
    """
    This function tests the correct behaviour of fc.add_constant() when a wrong input is given.
    It will first delete the constants file and then create a new one with a constant.
    Monkeypatch is then set with the simulated input: it will insert an existing constant and its value.
    The test is passed if an error is raised.
    """
    # path to constants file
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)

    # monkeypatch setting
    name = 'value_name'
    value = 100
    answers = iter([name, str(value)])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    # saving the constant
    fc.save_constants(np.array([[name, value]]))

    with pytest.raises(NameError):
        fc.add_constant()


def test_delete_constant(monkeypatch):
    """
    This function tests the correct behaviour of fc.delete_constant().
    It will first delete the constants file and then create a new one with a constant.
    Monkeypatch is then set with the simulated input: it will try to eliminate that constant.
    The test is passed if the constant is deleted.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)

    # setting monkeypatch
    name = 'value_name'
    value = 100
    monkeypatch.setattr('builtins.input', lambda _: name)

    # saving a constant
    fc.save_constants(np.array([[name, value]]))

    fc.delete_constant()
    constants = fc.read_constants()

    assert np.any(constants["name"].str.contains(name)) == False


def test_delete_constant_error_raised(monkeypatch):
    """
    This function tests the correct behaviour of fc.delete_constant() when an error is raised.
    It will first delete the constants file and then create a new empty one.
    Monkeypatch is then set with the simulated input: it will try to eliminate a constant.
    The test is passed if an error is raised.
    """
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "plafi",
                                       "plafi_constants.csv")
    os.remove(constants_file_path)
    fc.initialize_constants()

    # setting monkeypatch
    name = 'value_name'  # this constant does not exist in the initialized constants file
    monkeypatch.setattr('builtins.input', lambda _: name)

    with pytest.raises(NameError):
        fc.delete_constant()


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


def test_generate_fitting_function_correct_type():
    """
    This function tests the correct behaviour of fc.generate_fitting_function().
    It will create five different fitting function with different numbers of parameters.
    The test is passed if all the functions are types.FunctionType.
    """
    func1 = fc.generate_fitting_function("var1*sin(x)+var1", 1)
    func2 = fc.generate_fitting_function("var1*sin(x)+var2", 2)
    func3 = fc.generate_fitting_function("var1*sin(x)+var3", 3)
    func4 = fc.generate_fitting_function("var1*sin(x)+var4", 4)
    func5 = fc.generate_fitting_function("var1*sin(x)+var5", 5)
    assert isinstance(func1, types.FunctionType)
    assert isinstance(func2, types.FunctionType)
    assert isinstance(func3, types.FunctionType)
    assert isinstance(func4, types.FunctionType)
    assert isinstance(func5, types.FunctionType)


@given(array=hen.arrays(dtype=float, shape=6))
def test_generate_fitting_function_correct_values(array):
    """
    This function tests the correct behaviour of fc.generate_fitting_function().
    It will create five different fitting function with different numbers of parameters.
    The test is passed if all the functions work properly.
    """
    func1 = fc.generate_fitting_function("var1*sin(x)+var1", 1)
    func2 = fc.generate_fitting_function("var1*sin(x)+var2", 2)
    func3 = fc.generate_fitting_function("var1*sin(x)+var3", 3)
    func4 = fc.generate_fitting_function("var1*sin(x)+var4", 4)
    func5 = fc.generate_fitting_function("var1*sin(x)+var5", 5)
    assert np.isclose(func1(*array[0:2]).item(0), (array[1]*np.sin(array[0])+array[1]).item(0), equal_nan=True)
    assert np.isclose(func2(*array[0:3]).item(0), (array[1]*np.sin(array[0])+array[2]).item(0), equal_nan=True)
    assert np.isclose(func3(*array[0:4]).item(0), (array[1]*np.sin(array[0])+array[3]).item(0), equal_nan=True)
    assert np.isclose(func4(*array[0:5]).item(0), (array[1]*np.sin(array[0])+array[4]).item(0), equal_nan=True)
    assert np.isclose(func5(*array).item(0), (array[1]*np.sin(array[0])+array[5]).item(0), equal_nan=True)


def test_generate_fitting_function_error_raised():
    """
    This function tests the correct behaviour of fc.generate_fitting_function() when a wrong input is given.
    The test is passed if an error is raised.
    """
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
    It will run fc.fitting_procedure() and check if the fitting values and the titles are correct.
    """
    # setting monkeypatch for not showing the plot
    monkeypatch.setattr(plt, 'show', lambda: None)

    # setting monkeypatch for the inputs
    path, rows_to_skip, x_index, y_index = "data2.xlsx", str(0), str(0), str(1)
    num_par, fit_func = str(2), "var1*cos(x+var2)"
    x_title, y_title = "a random title", "a second random title"
    answers = iter([path, rows_to_skip, x_index, y_index, num_par, fit_func, x_title, y_title])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    popt, perr, fig = fc.fitting_procedure()

    assert abs(abs(popt[0]) - 1) < 0.001
    assert abs(abs(popt[1]) - np.pi / 2) < 0.001
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_fitting_procedure_error_raised(monkeypatch):
    """
    This function tests the correct behaviour of fc.fitting_procedure() when a wrong input is given.
    Monkeypatch is used to simulate the input.
    It will run fc.fitting_procedure() and check if an error is raised when passing a wrong path.
    """
    # setting monkeypatch for the inputs
    wrong_path = "file_does_not_exist.txt"
    answers = iter([wrong_path])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    with pytest.raises(NameError):
        fc.fitting_procedure()


def test_plot_data_verbose(monkeypatch):
    """
    This function tests the correct behaviour of fc.plot_data_verbose().
    Monkeypatch is used to not show the plot window and so not freezing the testing procedure and simulate the inputs.
    It will run fc.fitting_procedure() and check if the titles are correct.
    """
    monkeypatch.setattr(plt, 'show', lambda: None)

    path, rows_to_skip, x_index, y_index = "data1.csv", str(0), str(0), str(1)
    x_title, y_title = "a random title", "a second random title"
    answers = iter([path, rows_to_skip, x_index, y_index, x_title, y_title])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    fig = fc.plot_data_verbose()
    assert fig.axes[0].xaxis.label._text == x_title
    assert fig.axes[0].yaxis.label._text == y_title


def test_plot_data_verbose_error_raised(monkeypatch):
    """
    This function tests the correct behaviour of fc.plot_data_verbose() when a wrong input is given.
    Monkeypatch is used to simulate the inputs.
    It will run fc.fitting_procedure() and check if an error is raised when passing a wrong path.
    """
    wrong_path = "file_does_not_exist.txt"
    answers = iter([wrong_path])
    monkeypatch.setattr('builtins.input', lambda _: next(answers))

    with pytest.raises(NameError):
        fc.plot_data_verbose()


def test_print_constants():
    """
    This function tests the correct behaviour of fc.print_constants().
    The test is passed if fc.print_constants() return a string.
    """
    table = fc.print_constants()
    assert isinstance(table, str)


def test_initialize_conf_file():
    """
    This function tests the correct behaviour of fc.initialize_test_conf().
    The test is passed if, when the function is called, the new configuration
    file is created and contains the correct values.
    """
    fc.initialize_conf_file()
    assert os.path.exists("fitting_parameters0.cfg")
    file_conf = open("fitting_parameters0.cfg", "r")
    assert file_conf.read() == "[fitting parameters]\npath = \nrows to skip = 0\nx data index = 0\n" \
                               "y data index = 1\nnumber fitting parameters = 1\nfitting function = var1+x\n" \
                               "x-axis title = x title\ny-axis title = y title"
    file_conf.close()
    os.remove("fitting_parameters0.cfg")
