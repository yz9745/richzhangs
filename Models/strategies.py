def tradeByTrend(tickerHis):
    for i in range(0, len(tickerHis)):
        daily_info = tickerHis.loc(i)
        no_nan = True
        for j in range(0, len(daily_info.columns)):
            if np.isnan(daily_info[i]):
                no_nan = False
                break
        if no_nan:
            # do sth            
    return np.nan
            
            