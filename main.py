from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import get_merged_dataframe
import plotly.express as px
import numpy as np
import folium

# Dataframe mergée 
df = get_merged_dataframe()

# création de l'histogramme par défaut
fig = px.histogram(
    data_frame=df,
    x=df['PTOT'],
    labels={'PTOT': 'Nombre d\'habitants', 'count': 'Nombre de défibrillateurs'},
    color='REGION',
    nbins=60
)


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Défibrillateur en France métropolitaine', style={'textAlign':'center'}),
    dcc.RadioItems(['Aucun filtre', 'Défibrillateurs validés', 'Défibrillateurs en attente'], 'Aucun filtre', inline=True, id='radio-value'),
    # dcc.Graph(figure=fig),
    dcc.Graph(figure=fig, id='graph-id'),
    dash_table.DataTable(data=df.to_dict('records'))
])

# @callback(
#     Output(component_id='graph-id', component_property='figure'),
#     Input(component_id='radio-value', component_property='value')
# )
# def update_graph(filter_selected):
#     if filter_selected == "Aucun filtre":
#         filtered_df = df
#     elif filter_selected == "Défibrillateurs validés":
#         filtered_df = df[df['c_etat_valid'] == 'validées']
#     else:
#         filtered_df = df[df['c_etat_valid'] == 'en attente de validation']
    
#     addition_filtered = filtered_df.groupby('categoryVille').size()
#     villeName_filtered = filtered_df.groupby('categoryVille')['c_com_nom'].nunique()
#     moyenne_filtered = addition_filtered / villeName_filtered
    
#     # new_fig = px.bar(x=moyenne_filtered.index, y=moyenne_filtered.values, labels={'x': 'Nombre d\'habitants','y': 'Nombre moyen de défibrillateur'})
#     new_fig = px.histogram(x=moyenne_filtered.index, y=moyenne_filtered.values, labels={'x': 'Nombre d\'habitants','y': 'Nombre moyen de défibrillateur'})
#     return new_fig


if __name__ == '__main__':
    app.run(debug=True)