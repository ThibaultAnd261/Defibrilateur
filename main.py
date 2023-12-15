from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import get_merged_dataframe
import pandas as pd

df = get_merged_dataframe()
# print(data)
# df = pd.DataFrame(data)

moyenne = df.groupby('categoryVille')['PTOT'].mean() # done
#addition = df.groupby('categoryVille').size()
print(moyenne)
#print(addition)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Graph(),
    dash_table.DataTable(data=df.to_dict('records'))
])

village = []
ville = []
ville_moyenne = []
grande_ville = []
metropole = []


if __name__ == '__main__':
    app.run(debug=True)