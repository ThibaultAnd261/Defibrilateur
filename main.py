from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import read_file
import pandas as pd

FILENAME = "geodae.csv"
data = read_file(FILENAME)
df = pd.DataFrame(data)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dash_table.DataTable(data=df.to_dict('records'))
])

if __name__ == '__main__':
    app.run(debug=True)