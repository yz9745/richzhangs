import pandas as pd
from executions import *
from filters import *

ledger, blotter = []
active_list = []

def initilization():
    blotter = pd.DataFrame(None, columns = ['ID', 'Date', 'Time', 'Ticker', 'Action', 'Price', 'Type', 'Status'])
    ledger = pd.DataFrame(None, columns = ['ID', 'Date', 'Time', 'Active Holdings', 'Cash', 'PnL'])
    active_list = pd.DataFrame(None, columns = ['ID','Ticker', 'Holding Status', 'Current Price', 'Holding price', 'Position', 'Target', 'Stop', 'PnL'])



def back_test(start_date, end_date):
    start = start_date.toInt()
    end = end_date.toInt()
    while start < end:
        if len(active_list) >= 10:
            pass
        else:
            list = myFilter(start)
            for stock_info in list:
                open_position()
    return


def main():
    initilization()
    back_test('2020-1-1', '2021-1-1')


if __name__ == "__main__":
    # execute only if run as a script
    main()






