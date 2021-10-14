import pandas as pd
import yfinance as yf
import numpy as np

start = "2019-01-01"
end = "2021-01-01"
short_term = 3
long_term_one = 30
long_term_two = 45
long_term_three = 60
default_nan = np.nan
day = 1
week = 5
month = 20

def getMovingAve(data, period):
    rtn = []
    for i in range(0, len(data)):
        if i < period - 1:
            rtn.append(default_nan)
        else:
            sum = 0.0
            for j in range(i - period + 1, i + 1):
                sum += data[j]
            rtn.append(sum/period)
    return rtn

def getDer(data, period):
    rtn = []
    for i in range(0, len(data)):
        if i < period:
            rtn.append(default_nan)
        elif not np.isnan(data[i]) and not np.isnan(data[i - period]) : 
            rtn.append((data[i] - data[i - period])/period)
        else:
            rtn.append(default_nan)
    return rtn

def generate_tickers(ticker_names):
    tickers = []
    for i in range(len(ticker_names)):
        ticker = yf.Ticker(ticker_names[i])
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
        tickers.append(hist)
    return tickers

def main():
    # grab the stock name list
    ticker_names = [] # some method to generate the list
    # for temp use
    ticker_names.append("X")
    
    # iterate the names to get all tickers info
    tickers = generate_tickers(ticker_names)

if __name__ == "__main__":
    # execute only if run as a script
    main()
