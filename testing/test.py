import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from plafi import functions as fc


def test_read_data():
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.csv"))
    assert np.all(fc.read_data("data1.txt") == fc.read_data("data1.xlsx"))
