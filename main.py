"""
Fichier utilisé pour le rendu de l'application
"""
from dash import Dash, html, dcc, callback, Output, Input, dash_table
from get_data_api import get_merged_dataframe, get_horaires_dispo, get_cities_with_arrondissement
import plotly.express as px
import folium

# Dataframe mergée 
df = get_merged_dataframe()

# Horaires disponibles
horaires_dispo = get_horaires_dispo(df['c_disp_h'].unique())

# Villes ayant des arrondissements
cities_with_arrondissement = get_cities_with_arrondissement(df['COM'].unique())

# coordonnées de la France
coordsFrance = (46.539758, 2.430331)
map = folium.Map(location=coordsFrance, tiles='OpenStreetMap', zoom_start=6)

# histogramme
hist = px.histogram(
    data_frame=df,
    x='PTOT',
    labels={'PTOT': 'Nombre d\'habitants', 'count': 'Nombre de défibrillateurs'},
    color='REGION',
    nbins=60,
)
hist.update_layout(
    title='Répartition du nombre de défibrillateurs en fonction du nombre d\'habitants',
    xaxis_title='Nombre d\'habitants',
    yaxis_title='Nombre de défibrillateur'
)
hist.update_yaxes(title_text='Nombre de défibrillateurs')

# map de la France
fig_map = px.scatter_mapbox(
    df,
    lat='c_lat_coor1',
    lon='c_long_coor1',
    zoom=3,
    center={'lat': coordsFrance[0], 'lon': coordsFrance[1]},
    mapbox_style="open-street-map",
)
fig_map.update_traces(marker_size=4, selector=dict(mode='markers'))
fig_map.update_layout(
    title='Localisation des défibrillateurs en France'
)

# liste des différents moments de disponibilité d'un défibrillateur
jours_dispos = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', '\"jours fériés\"', 'événements', '7j/7']

app = Dash(__name__)

# layout de l'application
app.layout = html.Div([
    html.H1(children='Défibrillateur en France métropolitaine', style={'textAlign':'center'}),
    html.Div([
        html.H2("Présentation", style={'color': 'darkblue'}),
        html.P("Bienvenue sur notre dashboard qui fournit des données sur le nombre de défibrillateurs en France métropolitaine.", 
            style={'fontSize': '18px', 'marginBottom': '10px'}),
        html.P("Utilisez les fonctionnalités de l'application pour explorer les informations sur les emplacements des défibrillateurs ainsi que l'histogramme recensant le nombre de défibrillateur par habitants.", 
            style={'fontSize': '18px', 'marginBottom': '10px'}),
        html.P("Utilisez les filtres proposés pour sélectionner les données spécifiques que vous souhaitez visualiser.", 
            style={'fontSize': '18px', 'marginBottom': '10px'})
    ], style={'margin': '20px', 'padding': '15px', 'borderBottom': '2px solid darkblue'}),
    
    html.Div([
        html.H2('Filtres pour l\'histogramme et la carte française :', style={'marginTop': '20px', 'fontWeight': 'bold'}),

        html.Div([
            html.H3('Type de défibrillateur :'),
            dcc.RadioItems(['Aucun filtre', 'Défibrillateurs validés', 'Défibrillateurs en attente'], 'Aucun filtre', inline=True, id='radio-value')
        ], style={'display': 'flex', 'alignItems': 'center', 'marginTop': '20px'}),
        
        html.Div([
            html.H3('Disponibilité des défibrillateurs :', style={'marginTop': '10px'}),
            html.Div([
                html.H4('Plage journalière :'),
                dcc.Checklist(
                    options=[{'label': jour_dispo.strip('\"').capitalize(), 'value': jour_dispo} for jour_dispo in jours_dispos],
                    value=[],
                    id='checkbox-jours',
                    inline=True
                ),
            ], style={'display': 'flex', 'alignItems': 'center', 'marginTop': '10px'}),
            html.Div([
                html.H4('Plage horaire :'),
                dcc.Checklist(
                    options=[{'label': horaire_dispo.strip('\"').capitalize(), 'value': horaire_dispo} for horaire_dispo in horaires_dispo],
                    value=[],
                    id='checkbox-horaires',
                    inline=True
                )
            ], style={'display': 'flex', 'alignItems': 'center', 'marginTop': '10px'}),
            html.Div([
                html.P([
                    html.B('Attention', style={'textDecoration' : 'underline'}),
                    ' : les villes ci-dessous ne sont pas stockées en tant que ville unique mais gardées en tant qu\'arrondissement :',
                ], style={'color': 'white', 'fontSize': '16px', 'padding': '4px'}),
                html.Ul([
                    *[html.Li(city, style={'color': 'white', 'fontSize': '16px', 'marginTop': '5px'}) for city in cities_with_arrondissement]
                ])
            ], style={'marginTop': '20px', 'marginBottom': '20px', 'padding': '8px', 'backgroundColor': '#ff8c00', 'borderRadius': '6px'})
        ], style={'marginTop': '20px'}),
        dcc.Graph(figure=hist, id='graph-id'),
        dcc.Graph(figure=fig_map, id="map-id")
    ], style={'margin': '20px', 'padding': '15px'})
], style={'padding' : '25px',})

# fonction callback pour les affichages dynamiques
@callback(
    Output(component_id='graph-id', component_property='figure'),
    Output(component_id='map-id', component_property='figure'),
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
    updated_hist = px.histogram(
        data_frame=filtered_df,
        x='PTOT',
        labels={'PTOT': 'Nombre d\'habitants', 'count': 'Nombre de défibrillateurs'},
        color='REGION',
        nbins=60,
    )
    updated_hist.update_layout(
        title='Répartition du nombre de défibrillateurs en fonction du nombre d\'habitants',
        xaxis_title='Nombre d\'habitants',
        yaxis_title='Nombre de défibrillateur'
    )
    
    # mise à jour de la carte
    updated_map = px.scatter_mapbox(
        filtered_df,
        lat='c_lat_coor1',
        lon='c_long_coor1',
        zoom=3,
        center={'lat': coordsFrance[0], 'lon': coordsFrance[1]},
        mapbox_style="open-street-map"
    )
    updated_map.update_traces(marker_size=4, selector=dict(mode='markers'))
    updated_map.update_layout(
        title='Localisation des défibrillateurs en France'
    )
    
    return updated_hist, updated_map

if __name__ == '__main__':
    app.run(debug=True)