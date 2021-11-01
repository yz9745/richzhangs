import pandas as pd
import yfinance as yf
import numpy as np
from strategies import *
import time

start = "2018-01-01"
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


def generate_tickers(ticker_names):
    tickers = []
    for i in range(len(ticker_names)):
        ticker = yf.Ticker(ticker_names.iloc[0]['Symbol'])
        hist = ticker.history(start=start, end=end)
        # Todo:
        # get more info about the company such as industry
        hist = hist.drop(columns=['Dividends', 'Stock Splits'])
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
        tickers.append(hist)
    return tickers


def getTickers():
    ticker_files = pd.read_csv("../pre_loaded_files/tickers.csv")
    # for test use
    # todo: change to a whole list
    ticker_files = ticker_files.loc[0:50]
    return ticker_files

def main():
    # grab the stock name list
    startT = time.time()
    ticker_files = getTickers()

    # WARNING:
    #   DIDNT CHECK THE LENGTH
    # iterate the names to get all tickers info
    tickers = generate_tickers(ticker_files)
    for i in range(len(ticker_files)):
        tickers[i].to_csv("../tickers_info_output/" + ticker_files.loc[i][0] + ".csv")
    endT = time.time()
    print(f"Runtime of the program is {endT - startT}")


if __name__ == "__main__":
    # execute only if run as a script
    main()
