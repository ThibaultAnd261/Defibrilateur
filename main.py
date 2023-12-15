from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import read_file
import pandas as pd

FILENAME = "geodae.csv"
call_api = 'https://geo.api.gouv.fr/communes/56121?fields=nom,population&format=json&geometry=centre'
data = read_file(FILENAME)
df = pd.DataFrame(data)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dash_table.DataTable(data=df.to_dict('records'))
])

village = []
ville = []
ville_moyenne = []
grande_ville = []
metropole = []

for ville in ...:
    if ville['habitants'] < 5000:
        village.append(ville)
    elif ville['habitants'] < 20000:
        ville_moyenne.append(ville)
    elif ville['habitants'] < 50000:
        ville_moyenne.append(ville)
    elif ville['habitants'] < 200000:
        grande_ville.append(ville)
    else:
        metropole.append(ville)



if __name__ == '__main__':
    app.run(debug=True)