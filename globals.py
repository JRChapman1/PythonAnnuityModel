import pandas as pd
import pathlib


def init():
    global curve_data
    curve_data = pd.read_csv(str(pathlib.Path().absolute()) + '/assumptions/KVPairs.csv', index_col='Curve Name')