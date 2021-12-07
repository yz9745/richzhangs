from datetime import *
from dash import *
import dash_daq as daq
from richzhangs import *
import datetime as dt
import pickle
import pandas as pd
import numpy as np
import json

app = dash.Dash(__name__)

universe1_close  = pickle.load(open("C:\\Users\\vcm\\Desktop\\richzhangs_DATA\\universe1_close.p", "rb"))
# included daily returns and volume for use later maybe :)
universe1_rtn    = np.log(universe1_close[1:]/universe1_close.shift(1)[1:])
universe1_volume = pickle.load(open("C:\\Users\\vcm\\Desktop\\richzhangs_DATA\\universe1_volume.p", "rb"))

app.layout = html.Div([
    html.H2("Rich Zhang, Minglun & Yajie"),
    html.P("This is a stock strategy analysis model that backtests effectiveness of the chosen strategy. "),
    html.Div([
        html.P("You can choose the date range to show the analysis results in a range"),
        dcc.DatePickerRange(
            id='date_ranger',
            min_date_allowed=date(2019, 1, 1),
            max_date_allowed=date(2021, 1, 1),
            # initial_visible_month=date(2021, 1, 1),
            start_date=date(2018, 1, 1),
            end_date=date(2021, 1, 1)
        )
    ],
        style={"margin-right": "15px"}
    ),
    html.Br(),
    html.Div([
        html.P("You can either choose buy strategy or sell strategy"),
        dcc.Dropdown(
            id='strategy',
            options=[
                {'label': 'Buy Signals', 'value': 'BUY'},
                {'label': 'Sell Signals', 'value': 'SELL'}
            ],
            value='BUY'
        ),
    ]),
    html.Br(),
    html.Div(html.Button('Run', id='submit-button', n_clicks=0)),
    html.Br(),
    html.Div([
        html.P("Return Table: this table shows the statistical results grouped by each industry. Win ratio represents the win rate of the chosen strategy to each industry. Average return period represents the in average how long will this stradegy bring 5% return to you"),
        dash_table.DataTable(id='report')
    ]),
    html.Br(),
    html.Div([
        html.P("Blotter: this table shows every single trading activities based on the chosen strategy"),
        dash_table.DataTable(id='blotter')
    ]),
    html.Br(),
    html.Div([
        html.P("Return: this table shows the overall daily return of the chosen strategy, assuming all the trading activities use same amount of capital"),
        dash_table.DataTable(id='ledger')
    ]),
    dcc.Input(
            id="n1",
            type="number",
            value=3,
    ),
    dcc.Input(
            id="N1",
            type="number",
            value=30,
    ),
    daq.NumericInput(
        label='Label',
        labelPosition='bottom',
        value=10,
    ),
    html.Div(
        id = 'short_term_sma',
        children = '',
        style = {'display': 'none'}
    ),
    html.Div(
        id = 'long_term_sma',
        children = '',
        style = {'display': 'none'}
    )
])

@app.callback(
    dependencies.Output('short_term_sma', 'children'),
    dependencies.Input('n1', 'value')
)
def update_small_sma(n1):
    return universe1_close.rolling(window=n1).mean().to_json()
    #fdsa = pd.read_json(asdf)

@app.callback(
    dependencies.Output('long_term_sma', 'children'),
    dependencies.Input('N1', 'value')
)
def update_long_sma(N1):
    return universe1_close.rolling(window=N1).mean().to_json()

@app.callback(
    dependencies.Output('crossovers', 'children'),
    [dependencies.Input('short_term_sma', 'children'), dependencies.Input('long_term_sma', 'children')]
)
def calculate_crossovers(st_sma, lt_sma):

    st_sma = universe1_close.rolling(window=3).mean().to_json()
    lt_sma = universe1_close.rolling(window=30).mean().to_json()
    st_sma = pd.read_json(st_sma)
    lt_sma = pd.read_json(lt_sma)


    #st = st_sma["ZTS"]
    #lt = lt_sma["ZTS"]
    # -2 if small crosses long
    # +2 if long crosses small
    # 0 otherwise



    xover = np.sign((lt_sma - st_sma).dropna()).diff()



    crossovers = .rolling(window=2).sum()



#


# @app.callback(
#     [dependencies.Output('report', 'data'),
#      dependencies.Output('report', 'columns'),
#      dependencies.Output('blotter', 'data'),
#      dependencies.Output('blotter', 'columns'),
#      dependencies.Output('ledger', 'data'),
#      dependencies.Output('ledger', 'columns')],
#     dependencies.Input('submit-button', 'n_clicks'),
#     [dependencies.State('date_ranger', 'start_date'),
#      dependencies.State('date_ranger', 'end_date'),
#      dependencies.State('strategy', 'value')],
#     prevent_initial_call=True
# )
# def showReport(n_clicks, start, end, strategy):
#     report = pd.DataFrame(None, columns=['Industry', 'Count', 'Win', 'Sum Period', 'Sum Company'])
#     blotter = None
#     ledger = None
#     if strategy == 'BUY':
#         blotter = pd.read_csv('../output/buy_blotter.csv')
#         ledger = pd.read_csv('../output/buy_ledger.csv')
#     elif strategy == 'SELL':
#         blotter = pd.read_csv('../output/sell_blotter.csv')
#         ledger = pd.read_csv('../output/sell_ledger.csv')
#     start_time = (pd.to_datetime(start) - dt.datetime(1970,1,1)).total_seconds()
#     end_time = (pd.to_datetime(end) - dt.datetime(1970,1,1)).total_seconds()
#     tickers = getTickers()
#     industries = tickers.Industry.unique()
#     for industry in industries:
#         report.loc[len(report.index)] = [industry, 0, 0, 0, 0]
#     for i in range(len(tickers)):
#         symbol = tickers.loc[i]['Symbol']
#         ticker_info = pd.read_csv("../stradegy_output/" + symbol + ".csv")
#         ticker_info = ticker_info.drop(ticker_info[ticker_info['Time'] < start_time].index)
#         ticker_info = ticker_info.drop(ticker_info[ticker_info['Time'] > end_time].index)
#         ticker_info = ticker_info.reset_index(drop=True)
#         tickers['Industry'] = tickers['Industry'].astype("string")
#         industry = tickers.loc[i]['Industry']
#         report.loc[report['Industry'] == industry, 'Sum Company'] = report.loc[report['Industry'] == industry, 'Sum Company'] + 1
#         if strategy == 'BUY':
#             active_list = ticker_info.loc[ticker_info['Long Signal'] == 'BUY']
#             active_list = active_list.reset_index(drop=True)
#             count = len(active_list)
#             report.loc[report['Industry'] == industry, 'Count'] = report.loc[report['Industry'] == industry, 'Count'] + count
#             win = len(ticker_info.loc[(ticker_info['Long Signal'] == 'BUY') & (ticker_info['Long Period'] > 0)])
#             report.loc[report['Industry'] == industry, 'Win'] = report.loc[report['Industry'] == industry, 'Win'] + win
#             sum_p = sum(ticker_info.loc[(ticker_info['Long Signal'] == 'BUY') & (ticker_info['Long Period'] > 0), 'Long Period'])
#             report.loc[report['Industry'] == industry, 'Sum Period'] = report.loc[report['Industry'] == industry, 'Sum Period'] + sum_p
#         elif strategy == 'SELL':
#             active_list = ticker_info.loc[ticker_info['Short Signal'] == 'SELL']
#             active_list = active_list.reset_index(drop=True)
#             count = len(active_list)
#             report.loc[report['Industry'] == industry, 'Count'] = report.loc[report['Industry'] == industry, 'Count'] + count
#             win = len(ticker_info.loc[(ticker_info['Short Signal'] == 'SELL') & (ticker_info['Short Period'] > 0)])
#             report.loc[report['Industry'] == industry, 'Win'] = report.loc[report['Industry'] == industry, 'Win'] + win
#             sum_p = sum(ticker_info.loc[(ticker_info['Short Signal'] == 'SELL') & (ticker_info['Short Period'] > 0), 'Short Period'])
#             report.loc[report['Industry'] == industry, 'Sum Period'] = report.loc[report['Industry'] == industry, 'Sum Period'] + sum_p
#     report = report.drop(report[report['Count'] == 0].index)
#     report['Win Ratio'] = report['Win'] / report['Count']
#     report['Ave Return Period'] = report['Sum Period'] / report['Win']
#     report = report.drop(['Count', 'Win', 'Sum Period', 'Sum Company'], axis=1)
#     report = report.astype({'Win Ratio': 'double', 'Ave Return Period': 'double'})
#     report = report.round({'Win Ratio': 2, 'Ave Return Period': 2})
#     report = report.sort_values(by=['Ave Return Period'])
#     report_columns = [{"name": i, "id": i} for i in report.columns]
#     report_data = report.to_dict('records')
#     blotter = blotter[(blotter['start_time'] > start_time) & (blotter['end_time'] < end_time)]
#     ledger = ledger[(ledger['Time'] > start_time) & (ledger['Time'] < end_time)]
#     blotter = blotter.drop(['start_time', 'end_time', 'Unnamed: 0'], axis=1)
#     blotter_columns = [{"name": i, "id": i} for i in blotter.columns]
#     blotter_data = blotter.to_dict('records')
#     ledger['Date'] = pd.to_datetime(ledger['Time'] * 1000000000).dt.date
#     ledger = ledger[['Date', 'PnL']]
#     ledger_columns = [{"name": i, "id": i} for i in ledger.columns]
#     ledger_data = ledger.to_dict('records')
#     return report_data, report_columns, blotter_data, blotter_columns, ledger_data, ledger_columns


if __name__ == '__main__':
    app.run_server(debug=True)
