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
                {'label': 'Buy Signals', 'value': 'buy'},
                {'label': 'Sell Signals', 'value': 'sell'}
            ],
            value='buy'
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


def showReport(n_clicks, start, end, strategy):
    report = pd.DataFrame(None, columns = ['Industry', 'Count', 'Win', 'Sum Period'])
    tickers = getTickers()
    for i in range(len(tickers)):


if __name__ == '__main__':
    app.run_server(debug=True)
