import pandas as pd

data = pd.read_csv("C:\\Users\\giggi\\Desktop\\const.csv", skiprows=0, header=None, delimiter=";").to_numpy()

dic = dict(zip(data.T[0], data.T[1]))

for key in dic.keys():
    if key not in globals():
        globals()[key] = dic[key]