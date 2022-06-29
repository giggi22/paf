import types

import matplotlib.figure
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
import numexpr as ne
import os
from tabulate import tabulate
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import graphics


def read_data(
        path_to_data: str,
        rows_to_skip: int = 0
) -> np.ndarray:

    """
    Parameters
    ----------
    path_to_data (str): path to datafile
    rows_to_skip (int): number of rows to skip when the datafile is read

    Returns
    -------
    data (np.ndarray): matrix with the data

    Notes
    -----
    This function read <path_to_data> and returns the data contained in it.
    It skips the first <rows_to_skip> rows.
    The function can read .txt, .xlsx and .csv (with ";" as separator) files.
    """

    # reading data in <path_to_data> depending on its extension (.txt, .xlsx or .csv)
    if path_to_data.endswith(".txt"):
        data = np.loadtxt(path_to_data, skiprows=rows_to_skip)
    elif path_to_data.endswith(".xlsx"):
        data = pd.read_excel(path_to_data, header=None, skiprows=rows_to_skip).to_numpy()
    elif path_to_data.endswith(".csv"):
        data = np.genfromtxt(path_to_data, delimiter=";")
    else:
        # an error is raised if the extension is not between the one that can be read
        raise NameError("Could not read this file")
    return data


def plot_data(
        data: np.ndarray,
        x_label: str = " ",
        y_label: str = " "
) -> matplotlib.figure.Figure:

    """
    Parameters
    ----------
    data (np.ndarray): matrix with the data
    x_label (str): label for the x-axis of the plot
    y_label (str): label for the y-axis of the plot

    Returns
    -------
    fig (matplotlib.figure.Figure): figure containing the plot

    Notes
    -----
    This function plot <data>.
    The chart x-axis and y-axis labels are set as <x_label> and <y_label>.
    """

    fig, axs = plt.subplots(1)
    axs.tick_params(axis='both', labelsize=15)

    # The x values are given by the first column of <data>, all the other columns are plot as function of x
    x_values = data.T[0]
    for idx, y_values in enumerate(data.T[1:]):
        axs.plot(x_values, y_values, ".", markersize=10, label="column {}".format(idx))

    axs.set_xlabel(x_label, fontsize=15)
    axs.set_ylabel(y_label, fontsize=15)
    axs.legend(fontsize=15)
    fig.tight_layout()

    plt.show()
    return fig


def plot_data_verbose(

) -> matplotlib.figure.Figure:

    """
    Returns
    -------
    fig (matplotlib.figure.Figure): figure containing the plot

    Notes
    -----
    This function plot some data whose path is requested to the user.
    Other parameters are requested: number of rows to skip, index of x values,
    index of y values and labels of the chart axis.
    """

    path = input("Path to data to plot: ")
    # raise an error if the file does not exist
    if not os.path.exists(path):
        raise NameError("The file does not exist")
    rows_to_skip = int(input("Number of rows to skip: "))
    data = read_data(path, rows_to_skip)
    x_index = int(input("Index of x data: "))
    # selecting the columns to plot
    y_indexes = list(map(int, input("Indexes of y data: ").strip().split()))
    x_title = input("X axis title: ")
    y_title = input("Y axis title: ")

    # creating a np.ndarray with only the data to plot
    data_indexes = [x_index] + y_indexes
    data_to_plot = data.T[data_indexes].T

    return plot_data(data_to_plot, x_title, y_title)


def fit_data(
        data: np.ndarray,
        fitting_function: types.FunctionType,
        x_index: int = 0,
        y_index: int = 1,
        x_label: str = " ",
        y_label: str = " "
) -> [np.ndarray, np.ndarray, matplotlib.figure.Figure]:

    """
    Parameters
    ----------
    data (np.ndarray): matrix with all the data
    fitting_function (types.FunctionType): function to be used for the fit
    x_index (int): index of x values
    y_index (int): index of y values
    x_label (str): label for the x-axis of the plot
    y_label (str): label for the y-axis of the plot

    Returns
    -------
    popt (np.ndarray): values of the fitting parameters
    perr (np.ndarray): standard deviations of the fitting parameters
    fig (matplotlib.figure.Figure): figure containing the plot

    Notes
    -----
    This function fit a set of values in <data>, using <fitting_function> as fitting function and plot both of them.
    The values are selected using <x_index> and <y_index>.
    <x_label> and <y_label> are the labels of the chart axis.
    """

    # extracting the value for the fit
    x_values = data.T[x_index]
    y_values = data.T[y_index]

    # fitting procedure
    popt, pcov = curve_fit(fitting_function, x_values, y_values)
    perr = np.sqrt(np.diag(pcov))

    # printing the fitting parameters
    for idx, par in enumerate(popt):
        print("parameter {}: ".format(idx + 1), ufloat(par, perr[idx]))

    # plotting the data and the fitting curve
    fig, axs = plt.subplots(1)
    axs.tick_params(axis='both', labelsize=15)
    axs.plot(x_values, y_values, ".", markersize=10, label="data (col {})".format(y_index))
    axs.plot(x_values, fitting_function(x_values, *popt), "--", linewidth=2.1, label="fit")
    axs.set_xlabel(x_label, fontsize=15)
    axs.set_ylabel(y_label, fontsize=15)
    axs.legend(fontsize=15)
    fig.tight_layout()

    plt.show()
    return popt, perr, fig


def valid_function(
        str_funct: str  # fitting function written as string
) -> bool:  # True: the function is cn be used; False: the function can not be used

    """
    Parameters
    ----------
    str_funct (str): fitting function written as string

    Returns
    -------
    valid (bool): True if the function can be used, False otherwise

    Notes
    -----
    This function check if <str_funct> can be used as fitting function.
    The function is valid if contains mathematical operation that are included in the numpy module.
    Moreover, it can contain x as variable, and some parameter (var1 -> var5).

    Warnings
    --------
    This function will accept symbols as "pi" or "e" because they are
    included in numpy, even though they are not included in the constants file.
    """

    # creating a dictionary with all the constants
    constants = read_constants().to_numpy()
    dic = dict(zip(constants.T[0], constants.T[1]))

    # dictionary with all the allowed simbols/operations
    ALLOWED_NAMES = {
                        k: v for k, v in np.__dict__.items() if not k.startswith("__")
                    } | {
                        "x": "x", "var1": "var1", "var2": "var2", "var3": "var3", "var4": "var4", "var5": "var5"
                    } | dic

    # Compile the expression
    code = compile(str_funct, "<string>", "eval")

    valid = True

    # Check for not allowed names
    for name in code.co_names:
        if name not in ALLOWED_NAMES and valid:
            print("{} can not be used".format(name))
            valid = False

    return valid


def generate_fitting_function(str_funct, num_var):
    constants_to_globals()
    match num_var:
        case 1:
            def fitting_function(x, var1):
                return ne.evaluate(str_funct)
        case 2:
            def fitting_function(x, var1, var2):
                return ne.evaluate(str_funct)
        case 3:
            def fitting_function(x, var1, var2, var3):
                return ne.evaluate(str_funct)
        case 4:
            def fitting_function(x, var1, var2, var3, var4):
                return ne.evaluate(str_funct)
        case 5:
            def fitting_function(x, var1, var2, var3, var4, var5):
                return ne.evaluate(str_funct)
        case _:
            raise NameError("The number of parameters must range from 1 to 5")

    return fitting_function


def fitting_procedure():
    path = input("Path to data to plot: ")
    rows_to_skip = int(input("Number of rows to skip: "))
    data = read_data(path, rows_to_skip)
    x_index = int(input("Index of x data: "))
    y_index = int(input("Index of y data: "))
    num_var = int(input("Number of fitting parameters (max 5): "))

    stringa = ""
    for i in range(num_var):
        stringa += " var{}".format(i + 1)
    print("Write the fitting function. Use", end='')
    with graphics.highlighted_cyan_text():
        print(stringa, end='')
    print(" as fitting parameters.")
    str_fitting_function = input(">>>")

    if valid_function(str_fitting_function):
        fitting_function = generate_fitting_function(str_fitting_function, num_var)
        x_title = input("X axis title: ")
        y_title = input("Y axis title: ")
        return fit_data(data, fitting_function, x_index, y_index, x_title, y_title)


def initialize_constants():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plafi_constants.csv")
    if not os.path.exists(constants_file_path):
        save_constants(None)


def read_constants():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plafi_constants.csv")
    constants = pd.read_csv(constants_file_path, index_col=False, sep=";")

    return constants


def constants_to_globals():
    constants = read_constants().to_numpy()

    dic = dict(zip(constants.T[0], constants.T[1]))

    for key in dic.keys():
        if key not in globals():
            globals()[key] = dic[key]


def print_constants():
    constants = read_constants()

    # table creation
    table = tabulate(constants, headers=[str(constants.columns[0]), str(constants.columns[1])],
                     tablefmt="fancy_grid", showindex=False)

    # printing the plan in the table
    print(table)
    return table


def add_constant():
    constants = read_constants().to_numpy()
    name = input("New constant name: ")
    value = float(input("New constant value: "))
    if name in constants.T[0]:
        raise NameError("This name is already used")
    else:
        constants = np.vstack([constants, [name, value]])
        save_constants(constants)


def save_constants(constants):
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plafi_constants.csv")
    pd.DataFrame(constants, columns=["name", "value"]).to_csv(constants_file_path, index=False, sep=";")


def delete_constant():
    constants = read_constants()
    name = input("Constant name to delete: ")
    print(constants["name"])
    if not np.any(constants["name"].str.contains(name)):
        raise NameError("This name does not exist")
    else:
        constants = constants[constants["name"].str.contains(name) == False]
        constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plafi_constants.csv")
        constants.to_csv(constants_file_path, index=False, sep=";")
