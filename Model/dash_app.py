from datetime import *
from dash import *
from rich_model import *

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Rich Zhang, Minglun & Yajie"),
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
])


@app.callback(
    [dependencies.Output('report', 'data'),
     dependencies.Output('report', 'columns')],
    dependencies.Input('submit-button', 'n_clicks'),
    [dependencies.State('date_ranger', 'start_date'),
     dependencies.State('date_ranger', 'end_date'),
     dependencies.State('strategy', 'value')],
    prevent_initial_call=True
)
def showReport(n_clicks, start, end, strategy):
    report = pd.DataFrame(None, columns=['Industry', 'Count', 'Win', 'Sum Period', 'Sum Company'])
    tickers = getTickers()
    for i in range(len(tickers)):
        ticker_info = pd.read_csv("../stradegy_output/" + tickers.loc[i]['Symbol'] + ".csv")
        industry = tickers.loc[i]['Industry']
        if not industry in report['Industry']:
            report.loc[len(report.index)] = [industry, 0, 0, 0, 0]
        report.loc[report['Industry'] == industry, 'Sum Company'] = report.loc[report['Industry'] == industry, 'Sum Company'] + 1
        if strategy == 'BUY':
            count = len(ticker_info.loc[ticker_info['Long Signal'] == 'BUY'])
            report.loc[report['Industry'] == industry, 'Count'] = report.loc[report['Industry'] == industry, 'Count'] + count
            win = len(ticker_info.loc[(ticker_info['Long Signal'] == 'BUY') & (ticker_info['Long Period'] > 0)])
            report.loc[report['Industry'] == industry, 'Win'] = report.loc[report['Industry'] == industry, 'Win'] + win
            sum_p = sum(ticker_info.loc[(ticker_info['Long Signal'] == 'BUY') & (ticker_info['Long Period'] > 0), 'Long Period'])
            report.loc[report['Industry'] == industry, 'Sum Period'] = report.loc[report['Industry'] == industry, 'Sum Period'] + sum_p
        elif strategy == 'SELL':
            count = len(ticker_info.loc[ticker_info['Short Signal'] == 'SELL'])
            report.loc[report['Industry'] == industry, 'Count'] = report.loc[report['Industry'] == industry, 'Count'] + count
            win = len(ticker_info.loc[(ticker_info['Short Signal'] == 'SELL') & (ticker_info['Short Period'] > 0)])
            report.loc[report['Industry'] == industry, 'Win'] = report.loc[report['Industry'] == industry, 'Win'] + win
            sum_p = sum(ticker_info.loc[(ticker_info['Short Signal'] == 'SELL') & (ticker_info['Short Period'] > 0), 'Short Period'])
            report.loc[report['Industry'] == industry, 'Sum Period'] = report.loc[report['Industry'] == industry, 'Sum Period'] + sum_p
    report = report.drop(report[report['Count'] == 0].index)
    report['Win Ratio'] = report['Win'] / report['Count']
    report['Ave Return Period'] = report['Sum Period'] / report['Win']
    report = report.drop(['Count', 'Win', 'Sum Period', 'Sum Company'], axis=1)
    report = report.sort_values(by=['Ave Return Period'])
    report = report.astype({'Win Ratio': 'double', 'Ave Return Period': 'double'})
    report = report.round({'Win Ratio': 2, 'Ave Return Period': 2})
    report_columns = [{"name": i, "id": i} for i in report.columns]
    report_data = report.to_dict('records')
    return report_data, report_columns


if __name__ == '__main__':
    app.run_server(debug=True)
