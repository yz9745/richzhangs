# creates universe1_close.p and universe1_volume.p

import pandas as pd
from functools import reduce
import pickle

def fetch_data_to_list(data_col):

    df_list = []

    for index, row in pd.read_csv(
        "C:/Users/vcm/Desktop/richzhangs_DATA/pre_loaded_files/tickers_available.csv",
        usecols = ["Symbol", "Industry"]
    ).iterrows():
        print("Onboarding " + row['Symbol'] + ": " + str(row['Industry']))
        hist_data = pd.read_csv(
            "C:/Users/vcm/Desktop/richzhangs_DATA/tickers_history/" + row['Symbol'] + ".csv",
            usecols=["Date", data_col],
            parse_dates=["Date"]
        )
        hist_data.rename(columns={data_col:row['Symbol']}, inplace=True)
        df_list.append(hist_data)

    return df_list


print("reducing close prices...")

universe1_close = reduce(lambda x, y: pd.merge(x, y, on = 'Date'), fetch_data_to_list("Close"))
universe1_close.set_index("Date", inplace=True)

print("saving universe1_close.p...")
with open('C:\\Users\\vcm\\Desktop\\richzhangs_DATA\\universe1_close.p', 'wb') as handle:
    pickle.dump(universe1_close, handle, protocol=pickle.HIGHEST_PROTOCOL)

print("reducing close prices...")

universe1_volume = reduce(lambda x, y: pd.merge(x, y, on = 'Date'), fetch_data_to_list("Volume"))
universe1_volume.set_index("Date", inplace=True)

print("saving universe1_volume.p...")
with open('C:\\Users\\vcm\\Desktop\\richzhangs_DATA\\universe1_volume.p', 'wb') as handle:
    pickle.dump(universe1_volume, handle, protocol=pickle.HIGHEST_PROTOCOL)
