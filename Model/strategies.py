def longSignal(df):
    signals = []
    for i in range(len(df)):
        info = df.iloc[i]
        if info['Der weekly Long 1'] >= 0 and info['Der weekly Long 2'] >= 0 \
                and info['Der weekly Long 3'] >= 0 and info['Low'] < info['Ave Long 1']:
            signals.append("BUY")
        else:
            signals.append("")
    return signals


def longPeriod(df, win_ratio, loss_ratio):
    times = []
    for i in range(len(df)):
        info = df.iloc[i]
        win = info['Low'] * win_ratio
        loss = info['Low'] * loss_ratio
        if info['Long Signal'] == "BUY" and i != len(df) - 1:
            for j in range(i + 1, len(df)):
                temp = df.iloc[j]
                high = temp['High']
                low = temp['Low']
                if low <= win <= high:
                    times.append(j - i)
                    break
                elif low <= loss <= high:
                    times.append(i - j)
                    break
                elif j == len(df) - 1:
                    times.append(0)
                    break
        else:
            times.append(0)
    return times


def shortSignal(df):
    signals = []
    for i in range(len(df)):
        info = df.iloc[i]
        if info['Der weekly Long 1'] <= 0 and info['Der weekly Long 2'] <= 0 \
                and info['Der weekly Long 3'] <= 0 and info['High'] > info['Ave Long 1']:
            signals.append("SELL")
        else:
            signals.append("")
    return signals


def shortPeriod(df, win_ratio, loss_ratio):
    times = []
    for i in range(len(df)):
        info = df.iloc[i]
        loss = info['High'] * win_ratio
        win = info['High'] * loss_ratio
        if info['Short Signal'] == "SELL" and i != len(df) - 1:
            for j in range(i + 1, len(df)):
                temp = df.iloc[j]
                high = temp['High']
                low = temp['Low']
                if low <= win <= high:
                    times.append(j - i)
                    break
                elif low <= loss <= high:
                    times.append(i - j)
                    break
                elif j == len(df) - 1:
                    times.append(0)
                    break
        else:
            times.append(0)
    return times
