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


def apply_stradegies(symbols):
    for symbol in symbols:
        hist = pd.read_csv("../tickers_history/" + symbol + ".csv")
        hist['Ave Short'] = getMovingAve(hist['Close'], short_term)
        hist['Ave Long 1'] = getMovingAve(hist['Close'], long_term_one)
        hist['Ave Long 2'] = getMovingAve(hist['Close'], long_term_two)
        hist['Ave Long 3'] = getMovingAve(hist['Close'], long_term_three)
        hist['Der Daily Short'] = getDer(hist['Ave Short'], day)
        hist['Der Daily Long 1'] = getDer(hist['Ave Long 1'], day)
        hist['Der Daily Long 2'] = getDer(hist['Ave Long 2'], day)
        hist['Der Daily Long 3'] = getDer(hist['Ave Long 3'], day)
        hist['Der weekly Short'] = getDer(hist['Ave Short'], week)
        hist['Der weekly Long 1'] = getDer(hist['Ave Long 1'], week)
        hist['Der weekly Long 2'] = getDer(hist['Ave Long 2'], week)
        hist['Der weekly Long 3'] = getDer(hist['Ave Long 3'], week)
        hist = hist.dropna()
        hist['Long Signal'] = longSignal(hist)
        hist['Long Period'] = longPeriod(hist, win_ratio, loss_ratio)
        hist['Short Signal'] = shortSignal(hist)
        hist['Short Period'] = shortPeriod(hist, win_ratio, loss_ratio)
        hist = hist.round(2)
        hist.to_csv("../stradegy_output/"+ symbol + ".csv")
    return


def getTickers():
    ticker_files = pd.read_csv("../pre_loaded_files/tickers_availables.csv")
    return ticker_files

def main():
    # grab the stock name list
    ticker_names = getTickers()
    apply_stradegies(ticker_names['Symbol'].to_list())


if __name__ == "__main__":
    # execute only if run as a script
    main()

