import csv
import pandas as pd

FILENAME_DEFIBRILLATEUR = "geodae.csv"
FILENAME_COMMUNE_2019 = "communes.csv"
FILENAME_COMMUNE_2021 = "donnees_communes.csv"

# retourne le contenu du fichier sous forme de liste
def read_file (filename):
    with open (filename, mode = 'r', encoding= 'utf8') as f :
        reader = csv.DictReader(f , delimiter = ";")
        l = []
        for ligne in reader :
            l.append(ligne)
    
    return l

# fusionne les dataframes en une seule manipulable
def get_merged_dataframe():
    dataDefibrilateur = read_file(FILENAME_DEFIBRILLATEUR)
    dfDef = pd.DataFrame(dataDefibrilateur) # transformation de la data sur les défibrillateurs en dataframe 

    dataCommune2019 = read_file(FILENAME_COMMUNE_2019)
    dfCom1 = pd.DataFrame(dataCommune2019)
    dfCom1 = dfCom1.rename(columns={'DEPCOM': 'c_com_insee'}) # renommage de la colonne 'DEPCOM' par 'c_com_insee' pour faciliter le merge
    
    dataCommune2021 = read_file(FILENAME_COMMUNE_2021)
    dfCom2 = pd.DataFrame(dataCommune2021)
    dfCom2['c_com_insee'] = dfCom2['CODDEP'] + dfCom2['CODCOM'].astype(str) # obtenir une colonne 'c_com_insee' sur dfCom2 pour faciliter le merge

    merged_df = pd.merge(dfDef, dfCom1, on='c_com_insee', how='inner') # merge de df1 et df2 sur merged_df
    merged_df = pd.merge(merged_df, dfCom2[['c_com_insee', 'REG']], on='c_com_insee', how='left') # merge de merged_df et df3 sur merged_df

    merged_df['PTOT'] = pd.to_numeric(merged_df['PTOT']) # conversion en nombre
    merged_df = merged_df.drop(['REG_y'], axis=1)
    merged_df = merged_df.rename(columns={'REG_x' : 'REGION'})

    return merged_df


# def main():
#     dataDefibrilateur = read_file(FILENAME_DEFIBRILLATEUR)
#     dfDef = pd.DataFrame(dataDefibrilateur)

#     dataCommune = read_file(FILENAME_COMMUNE_2019)
#     dfCom = pd.DataFrame(dataCommune)
    
#     dataCommune2021 = read_file(FILENAME_COMMUNE_2021)
#     dfCom2 = pd.DataFrame(dataCommune2021)
#     dfCom2['c_com_insee'] = dfCom2['CODDEP'] + dfCom2['CODCOM'].astype(str)

#     dfCom = dfCom.rename(columns={'DEPCOM': 'c_com_insee'})
#     merged_df = pd.merge(dfDef, dfCom, on='c_com_insee', how='inner')

#     merged_df = pd.merge(merged_df, dfCom2[['c_com_insee', 'REG']], on='c_com_insee', how='left')

#     # merged_df['categoryVille'] = merged_df.apply(population_category, axis=1)
#     print(merged_df)
#     # print(dfCom2)

# main()