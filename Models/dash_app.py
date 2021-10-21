import dash_app
import dash_table
import dash_core_components as dcc
import dash_html_components as html

app = dash_app.Dash(__name__)

if __name__ == '__main__':
    app.run_server(debug=True)
