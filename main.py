from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import get_merged_dataframe
import plotly.express as px

df = get_merged_dataframe()

addition = df.groupby('categoryVille').size()
# villeName = df.groupby('categoryVille')['c_com_nom'].unique()
villeName = df.groupby('categoryVille')['c_com_nom'].nunique()

moyenne = addition / villeName

fig = px.bar(x=moyenne.index, y=moyenne.values, labels={'x': 'Nombre d\'habitants','y': 'Nombre moyen de défibrillateur'})

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Graph(figure=fig),
    dash_table.DataTable(data=df.to_dict('records'))
])

if __name__ == '__main__':
    app.run(debug=True)