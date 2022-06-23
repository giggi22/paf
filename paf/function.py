import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *
from scipy.optimize import curve_fit
from uncertainties import ufloat
import numexpr as ne


def read_data(path, rows_to_skip=0):
    if path.endswith(".txt"):
        data = np.loadtxt(path, skiprows=rows_to_skip)
    elif path.endswith(".xlsx"):
        data = pd.read_excel(path, header=None, skiprows=rows_to_skip).to_numpy()
    elif path.endswith(".csv"):
        data = np.genfromtxt(path, delimiter=";")
    else:
        data = 0

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


def fit_data(data, fitting_function, index=1, x_label=" ", y_label=" "):
    fig, axs = plt.subplots(1)
    axs.tick_params(axis='both', labelsize=15)

    x_values = data.T[0]
    y_values = data.T[index]
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
    ALLOWED_NAMES = {
                        k: v for k, v in np.__dict__.items() if not k.startswith("__")
                    } | {"x": "x", "var1": "var1", "var2": "var2", "var3": "var3", "var4": "var4", "var5": "var5"}

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


data = read_data("C:\\Users\\giggi\\Desktop\\test.xlsx")
expr = "var1*cos(x+ var3) + var2"
if valid_function(expr):
    f = generate_fitting_function(expr, 3)
    fit_data(data, f)
