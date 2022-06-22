import numpy as np
import pandas as pd


def read_data(path):
    rows_to_skip = 0

    if path.endswith(".txt"):
        data = np.loadtxt(path, skiprows=rows_to_skip)
    elif path.endswith(".xlsx"):
        data = pd.read_excel(path, header=None, skiprows=rows_to_skip).to_numpy()
    elif path.endswith(".csv"):
        data = np.genfromtxt(path, delimiter=";")
    else:
        data = 0

    return data

