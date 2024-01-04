from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import get_merged_dataframe, get_horaires_dispo
import plotly.express as px
import numpy as np
import folium

# Dataframe mergée 
df = get_merged_dataframe()

# Horaires disponibles
horaires_dispo = get_horaires_dispo(df['c_disp_h'].unique())

# création de l'histogramme par défaut
fig = px.histogram(
    data_frame=df,
    x='PTOT',
    labels={'PTOT': 'Nombre d\'habitants', 'count': 'Nombre de défibrillateurs'},
    color='REGION',
    nbins=60
)

# liste des différents moments de disponibilité d'un défibrillateur
jours_dispos = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', '\"jours fériés\"', 'événements', '7j/7']

app = Dash(__name__)

# layout de l'application
app.layout = html.Div([
    html.H1(children='Défibrillateur en France métropolitaine', style={'textAlign':'center'}),
    html.H2('Filtres de l\'histogramme:', style={'margin-top': '20px', 'font-weight': 'bold'}),

    html.Div([
        html.H3('Type de défibrillateur :'),
        dcc.RadioItems(['Aucun filtre', 'Défibrillateurs validés', 'Défibrillateurs en attente'], 'Aucun filtre', inline=True, id='radio-value')
    ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '20px'}),
    
    html.Div([
        html.H3('Disponibilité des défibrillateurs :', style={'margin-top': '10px'}),
        html.Div([
            html.H4('Plage journalière :'),
            dcc.Checklist(
                options=[{'label': jour_dispo.strip('\"').capitalize(), 'value': jour_dispo} for jour_dispo in jours_dispos],
                value=[],
                id='checkbox-jours',
                inline=True
            ),
        ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '10px'}),
        html.Div([
            html.H4('Plage horaire :'),
            dcc.Checklist(
                options=[{'label': horaire_dispo.strip('\"').capitalize(), 'value': horaire_dispo} for horaire_dispo in horaires_dispo],
                value=[],
                id='checkbox-horaires',
                inline=True
            )
        ], style={'display': 'flex', 'align-items': 'center', 'margin-top': '10px'}),
    ], style={'margin-top': '20px'}),
    dcc.Graph(figure=fig, id='graph-id'),
    dash_table.DataTable(data=df.to_dict('records'))
], style={'padding' : '25px'})

# fonction callback pour les affichages dynamiques
@callback(
    Output(component_id='graph-id', component_property='figure'),
    Input(component_id='radio-value', component_property='value'),
    Input(component_id='checkbox-jours', component_property='value'),
    Input(component_id='checkbox-horaires', component_property='value')
)
def update_graph(filter_selected, days_selected, hours_selected):
    # vérification sur le type de défibrillateur choisi
    if filter_selected == "Aucun filtre":
        filtered_df = df
    elif filter_selected == "Défibrillateurs validés":
        filtered_df = df[df['c_etat_valid'] == 'validées']
    else:
        filtered_df = df[df['c_etat_valid'] == 'en attente de validation']
    
    # vérification sur la/les disponibilité(s) du défibrillateur choisi
    if days_selected:
        filtered_df = filtered_df[filtered_df['c_disp_j'].apply(lambda x: any(jour_evenement in x for jour_evenement in days_selected))]

    # vérification sur les/l'heure(s) de disponibilité du défibrillateur
    if hours_selected:
        filtered_df = filtered_df[filtered_df['c_disp_h'].apply(lambda x: any(horaire in x for horaire in hours_selected))]

    # mise à jour de l'histogramme
    updated_fig = px.histogram(
        data_frame=filtered_df,
        x='PTOT',
        labels={'PTOT': 'Nombre d\'habitants', 'count': 'Nombre de défibrillateurs'},
        color='REGION',
        nbins=60
    )
    
    return updated_fig

if __name__ == '__main__':
    app.run(debug=True)