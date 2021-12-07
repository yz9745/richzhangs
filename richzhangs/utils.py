import pandas as pd
import yfinance as yf
import numpy as np
from strategies import *
import time

start = "2017-01-01"
end = "2021-01-01"
short_term = 3
long_term_one = 30
long_term_two = 45
long_term_three = 60
default_nan = np.nan
day = 1
week = 5
month = 20
win_ratio = 1.05
loss_ratio = 0.95


def getMovingAve(data, period):
    rtn = []
    for i in range(len(data)):
        if i < period - 1:
            rtn.append(default_nan)
        else:
            total = 0.0
            for j in range(i - period + 1, i + 1):
                total += data[j]
            rtn.append(total / period)
    return rtn


def getDer(data, period):
    rtn = []
    for i in range(len(data)):
        if i < period:
            rtn.append(default_nan)
        elif not np.isnan(data[i]) and not np.isnan(data[i - period]):
            rtn.append((data[i] - data[i - period]) / period)
        else:
            rtn.append(default_nan)
    return rtn

def getTickers():
    ticker_files = pd.read_csv("../pre_loaded_files/tickers_availables.csv")
    return ticker_files
