"""
    Fichier utilisé pour une manipulation sur les données de la dataframe
"""
import csv
import pandas as pd

# fichiers manipulés
FILENAME_DEFIBRILLATEUR = "geodae.csv"
FILENAME_COMMUNE_2017 = "Communes.csv"
FILENAME_COMMUNE_2019 = "donnees_communes.csv"

def read_file (filename: str) -> []:
    """ retourne le contenu du fichier sous forme de liste de dictionnaires
    Args:
        filename (str): le nom du fichier de données (n lignes)
    
    Returns:
        l (list): n-1 dictionnaires dont les clés sont les champs de la première ligne du fichier
    """
    with open (filename, mode = 'r', encoding= 'utf8') as f :
        reader = csv.DictReader(f , delimiter = ";")
        l = []
        for ligne in reader :
            l.append(ligne)
    
    return l

def get_merged_dataframe() -> pd.DataFrame:
    """ fusionne les 3 dataframes en une seule manipulable
    
    Returns:
        merged_df (DataFrame): dataframe qui sera manipulé par l'application dash avec les colonnes mergées
    """
    dataDefibrilateur = read_file(FILENAME_DEFIBRILLATEUR)
    dfDef = pd.DataFrame(dataDefibrilateur) # transformation de la data sur les défibrillateurs en dataframe 

    dataCommune2019 = read_file(FILENAME_COMMUNE_2017)
    dfCom1 = pd.DataFrame(dataCommune2019)
    dfCom1 = dfCom1.rename(columns={'DEPCOM': 'c_com_insee'}) # renommage de la colonne 'DEPCOM' par 'c_com_insee' pour faciliter le merge
    
    dataCommune2021 = read_file(FILENAME_COMMUNE_2019)
    dfCom2 = pd.DataFrame(dataCommune2021)
    dfCom2['c_com_insee'] = dfCom2['CODDEP'] + dfCom2['CODCOM'].astype(str) # obtenir une colonne 'c_com_insee' sur dfCom2 pour faciliter le merge

    merged_df = pd.merge(dfDef, dfCom1, on='c_com_insee', how='inner') # merge de df1 et df2 sur merged_df
    merged_df = pd.merge(merged_df, dfCom2[['c_com_insee', 'REG']], on='c_com_insee', how='left') # merge de merged_df et df3 sur merged_df

    merged_df['PTOT'] = pd.to_numeric(merged_df['PTOT']) # conversion en nombre
    merged_df = merged_df.rename(columns={'REG' : 'REGION'})

    return merged_df

def get_horaires_dispo(horaire_values: pd.Series) -> set[str]:
    """ retourne les horaires possibles d'après la dataframe
    Args:
        horaire_values (pd.Series): les séries sur la colonne 'c_disp_h' de la dataframe mergée
    
    Returns:
        horaires_dispo (set): liste ordonnée contenant les différentes possibilités de tranche horaire, utilisée pour les filtres de l'application Dash
    """
    horaires_dispo = set()

    for value in horaire_values:
        obj_list = value.split(',')

        # itére sur les objets et ajoute les horaires au set()
        for obj in obj_list:
            obj = obj.strip('{}')
            horaires_dispo.add(obj)

    return horaires_dispo

def get_cities_with_arrondissement(city_values: pd.Series) -> set[str]:
    """ retourne les villes ayant 'Arrondissement' en nom d'après la dataframe
    Args:
        city_values (pd.Series): les séries sur la colonne 'COM' de la dataframe mergée
    
    Returns:
        cities_with_arrondissement (set): liste ordonnée contenant les différentes villes ayant des arrondissements, utilisée pour la prévention dans l'application Dash
    """
    cities_with_arrondissement = set()
    
    for city in city_values:
        if 'Arrondissement' in city:
            city = city.split()
            cities_with_arrondissement.add(city[0])
            
    return cities_with_arrondissement

# Tests pour les retours
# def main():
#     merged_df = get_merged_dataframe()
#     # print(merged_df.keys)
#     # get_disp_j(merged_df)
#     # print(merged_df['c_disp_h'].unique())
#     # print(len(merged_df['c_disp_h'].unique()))
#     # print("------")
#     # print(set(merged_df['c_disp_h'].unique()))
#     # print(len(set(merged_df['c_disp_h'].unique())))
#     # print("------")
#     # horaire = get_horaires_dispo(merged_df['c_disp_h'].unique())
#     # print(horaire)
#     # print(merged_df['COM'].unique())
#     cities_with_arr = get_cities_with_arrondissement(merged_df['COM'])
#     print(cities_with_arr)

# main()