import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
import numexpr as ne
import os
from tabulate import tabulate


def read_data(path_to_data, rows_to_skip=0):
    # aggiungere condizione sull'esistenza del file
    if path_to_data.endswith(".txt"):
        data = np.loadtxt(path_to_data, skiprows=rows_to_skip)
    elif path_to_data.endswith(".xlsx"):
        data = pd.read_excel(path_to_data, header=None, skiprows=rows_to_skip).to_numpy()
    elif path_to_data.endswith(".csv"):
        data = np.genfromtxt(path_to_data, delimiter=";")
    else:
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


def plot_data_verbose():
    path = input("Path to data to plot: ")
    rows_to_skip = int(input("Number of rows to skip: "))
    data = read_data(path, rows_to_skip)
    x_index = int(input("Index of x data: "))
    y_indexes = list(map(int, input("Indexes of y data: ").strip().split()))
    x_title = input("X axis title: ")
    y_title = input("Y axis title: ")

    fig, axs = plt.subplots(1)
    axs.tick_params(axis='both', labelsize=15)

    x_values = data.T[x_index]
    for idx in y_indexes:
        y_values = data.T[idx]
        axs.plot(x_values, y_values, ".", markersize=10, label="column {}".format(idx))

    axs.set_xlabel(x_title, fontsize=15)
    axs.set_ylabel(y_title, fontsize=15)
    axs.legend(fontsize=15)
    fig.tight_layout()

    plt.show()


def fit_data(data, fitting_function, x_index=0, y_index=1, x_label=" ", y_label=" "):
    fig, axs = plt.subplots(1)
    axs.tick_params(axis='both', labelsize=15)

    x_values = data.T[x_index]
    y_values = data.T[y_index]
    for idx, y_val in enumerate(data.T[1:]):
        axs.plot(x_values, y_val, ".", markersize=10, label="column {}".format(idx))

    popt, pcov = curve_fit(fitting_function, x_values, y_values)
    perr = np.sqrt(np.diag(pcov))
    axs.plot(x_values, fitting_function(x_values, *popt), "--", linewidth=2.1, label="fit")

    for idx, par in enumerate(popt):
        print("parameter {}: ".format(idx), ufloat(par, perr[idx]))

    axs.set_xlabel(x_label, fontsize=15)
    axs.set_ylabel(y_label, fontsize=15)
    axs.legend(fontsize=15)
    fig.tight_layout()

    plt.show()


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
    print("Write the fitting function. Use" + stringa + " as fitting parameters.")
    str_fitting_function = input()

    if valid_function(str_fitting_function):
        fitting_function = generate_fitting_function(str_fitting_function, num_var)
        x_title = input("X axis title: ")
        y_title = input("Y axis title: ")
        fit_data(data, fitting_function, x_index, y_index, x_title, y_title)


def initialize_constants():
    constants_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plafi_constants.csv")
    if not os.path.exists(constants_file_path):
        print("Created plafi_constants.csv")
        void_dataframe = pd.DataFrame(columns=["name", "value"])
        void_dataframe.to_csv(constants_file_path, index=False, sep=";")


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


def add_constant():
    constants = read_constants().to_numpy()
    name = input("New constant name: ")
    value = float(input("New constant value: "))
    if name in constants.T[0]:
        raise NameError("This name is already used")
    else:
        constants = np.vstack([constants, [name, value]])
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
