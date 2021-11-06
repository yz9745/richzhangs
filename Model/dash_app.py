from datetime import *
from dash import *
from rich_model import *
from dateutil import parser

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Rich Zhang, Minglun & Yajie"),
    html.P("This is a backtested model to test our stradegies. You can choose the start and end dates of the stradegies and choose one of the stradegies to see the out come"),
    html.Div([
        html.P("Ticker Data Range"),
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
        html.P("Choose the Strategy"),
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
        html.P("Return Table"),
        dash_table.DataTable(id='report')
    ]),
    html.Br(),
    html.Div([
        html.P("Ledger"),
        dash_table.DataTable(id='ledger')
    ]),
])


@app.callback(
    [dependencies.Output('report', 'data'),
     dependencies.Output('report', 'columns'),
     dependencies.Output('ledger', 'data'),
     dependencies.Output('ledger', 'columns')],
    dependencies.Input('submit-button', 'n_clicks'),
    [dependencies.State('date_ranger', 'start_date'),
     dependencies.State('date_ranger', 'end_date'),
     dependencies.State('strategy', 'value')],
    prevent_initial_call=True
)
def showReport(n_clicks, start, end, strategy):
    report = pd.DataFrame(None, columns=['Industry', 'Count', 'Win', 'Sum Period', 'Sum Company'])
    ledger = pd.DataFrame(None, columns=['id', 'time', 'symbol', 'strategy', 'price', 'win'])
    index = 1
    start_time = int(parser.parse(start).timestamp())
    end_time = int(parser.parse(end).timestamp())
    tickers = getTickers()
    industries = tickers.Industry.unique()
    for industry in industries:
        report.loc[len(report.index)] = [industry, 0, 0, 0, 0]
    for i in range(len(tickers)):
        symbol = tickers.loc[i]['Symbol']
        ticker_info = pd.read_csv("../stradegy_output/" + symbol + ".csv")
        ticker_info = ticker_info.drop(ticker_info[ticker_info['Time'] < start_time].index)
        ticker_info = ticker_info.drop(ticker_info[ticker_info['Time'] > end_time].index)
        ticker_info = ticker_info.reset_index(drop=True)
        tickers['Industry'] = tickers['Industry'].astype("string")
        industry = tickers.loc[i]['Industry']
        report.loc[report['Industry'] == industry, 'Sum Company'] = report.loc[report['Industry'] == industry, 'Sum Company'] + 1
        if strategy == 'BUY':
            active_list = ticker_info.loc[ticker_info['Long Signal'] == 'BUY']
            active_list = active_list.reset_index(drop=True)
            count = len(active_list)
            for j in range(count):
                operation = active_list.loc[j]
                id = str(index) + "A"
                time = operation['Time']
                price = operation['Low']
                win = True
                period = operation['Long Period']
                if period <= 0:
                    win = False
                ledger.loc[len(ledger.index)] = [id, time, symbol, "BUY", price, win]
                id = str(index) + "B"
                time = time + abs(period) * 86400
                if win:
                    price = price * win_ratio
                else:
                    price = price * loss_ratio
                ledger.loc[len(ledger.index)] = [id, time, symbol, "Liquidation", price, win]
                index = index + 1
            report.loc[report['Industry'] == industry, 'Count'] = report.loc[report['Industry'] == industry, 'Count'] + count
            win = len(ticker_info.loc[(ticker_info['Long Signal'] == 'BUY') & (ticker_info['Long Period'] > 0)])
            report.loc[report['Industry'] == industry, 'Win'] = report.loc[report['Industry'] == industry, 'Win'] + win
            sum_p = sum(ticker_info.loc[(ticker_info['Long Signal'] == 'BUY') & (ticker_info['Long Period'] > 0), 'Long Period'])
            report.loc[report['Industry'] == industry, 'Sum Period'] = report.loc[report['Industry'] == industry, 'Sum Period'] + sum_p
        elif strategy == 'SELL':
            active_list = ticker_info.loc[ticker_info['Short Signal'] == 'SELL']
            active_list = active_list.reset_index(drop=True)
            count = len(active_list)
            report.loc[report['Industry'] == industry, 'Count'] = report.loc[report['Industry'] == industry, 'Count'] + count
            win = len(ticker_info.loc[(ticker_info['Short Signal'] == 'SELL') & (ticker_info['Short Period'] > 0)])
            report.loc[report['Industry'] == industry, 'Win'] = report.loc[report['Industry'] == industry, 'Win'] + win
            sum_p = sum(ticker_info.loc[(ticker_info['Short Signal'] == 'SELL') & (ticker_info['Short Period'] > 0), 'Short Period'])
            report.loc[report['Industry'] == industry, 'Sum Period'] = report.loc[report['Industry'] == industry, 'Sum Period'] + sum_p
            for j in range(count):
                operation = active_list.loc[j]
                id = str(index) + "A"
                time = operation['Time']
                price = operation['Low']
                win = True
                period = operation['Short Period']
                if period <= 0:
                    win = False
                ledger.loc[len(ledger.index)] = [id, time, symbol, "SELL", price, win]
                id = str(index) + "B"
                time = time + abs(period) * 86400
                if win:
                    price = price * loss_ratio
                else:
                    price = price * win_ratio
                ledger.loc[len(ledger.index)] = [id, time, symbol, "Liquidation", price, win]
                index = index + 1
    report = report.drop(report[report['Count'] == 0].index)
    report['Win Ratio'] = report['Win'] / report['Count']
    report['Ave Return Period'] = report['Sum Period'] / report['Win']
    report = report.drop(['Count', 'Win', 'Sum Period', 'Sum Company'], axis=1)
    report = report.astype({'Win Ratio': 'double', 'Ave Return Period': 'double'})
    report = report.round({'Win Ratio': 2, 'Ave Return Period': 2})
    report = report.sort_values(by=['Ave Return Period'])
    report_columns = [{"name": i, "id": i} for i in report.columns]
    report_data = report.to_dict('records')
    ledger = ledger.sort_values(by=['time']).reset_index(drop=True)
    ledger['date'] = pd.to_datetime(ledger['time'] * 1000000000).dt.date
    ledger = ledger.drop(['time'], axis=1)
    ledger = ledger.round({'price': 2})
    ledger_columns = [{"name": i, "id": i} for i in ledger.columns]
    ledger_data = ledger.to_dict('records')
    return report_data, report_columns, ledger_data, ledger_columns


if __name__ == '__main__':
    app.run_server(debug=True)
