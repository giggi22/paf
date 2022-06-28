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

    Warnings
    --------
    This function must be updated everytime the columns of the plan are changed
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


def plot_data(data, x_label=" ", y_label=" "):
    fig, axs = plt.subplots(1)
    axs.tick_params(axis='both', labelsize=15)

    x_values = data.T[0]
    for idx, y_values in enumerate(data.T[1:]):
        axs.plot(x_values, y_values, ".", markersize=10, label="column {}".format(idx))

    axs.set_xlabel(x_label, fontsize=15)
    axs.set_ylabel(y_label, fontsize=15)
    axs.legend(fontsize=15)
    fig.tight_layout()

    plt.show()
    return fig


def plot_data_verbose():
    path = input("Path to data to plot: ")
    rows_to_skip = int(input("Number of rows to skip: "))
    data = read_data(path, rows_to_skip)
    x_index = int(input("Index of x data: "))
    y_indexes = list(map(int, input("Indexes of y data: ").strip().split()))
    x_title = input("X axis title: ")
    y_title = input("Y axis title: ")

    data_indexes = [x_index] + y_indexes
    data_to_plot = data.T[data_indexes].T
    return plot_data(data_to_plot, x_title, y_title)


def fit_data(data, fitting_function, x_index=0, y_index=1, x_label=" ", y_label=" "):
    x_values = data.T[x_index]
    y_values = data.T[y_index]

    popt, pcov = curve_fit(fitting_function, x_values, y_values)
    perr = np.sqrt(np.diag(pcov))

    for idx, par in enumerate(popt):
        print("parameter {}: ".format(idx + 1), ufloat(par, perr[idx]))

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


def valid_function(str_funct):
    constants = read_constants().to_numpy()
    dic = dict(zip(constants.T[0], constants.T[1]))

    ALLOWED_NAMES = {
                        k: v for k, v in np.__dict__.items() if not k.startswith("__")
                    } | {
                        "x": "x", "var1": "var1", "var2": "var2", "var3": "var3", "var4": "var4", "var5": "var5"
                    } | dic

    """Evaluate a math expression."""
    # Compile the expression
    code = compile(str_funct, "<string>", "eval")

    valid = True

    # Validate allowed names
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
