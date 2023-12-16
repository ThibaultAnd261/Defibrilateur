import csv
import pandas as pd

FILENAME_DEFIBRILLATEUR = "geodae.csv"
FILENAME_COMMUNE = "communes.csv"

def read_file (filename):
    with open (filename, mode = 'r', encoding= 'utf8') as f :
        reader = csv.DictReader(f , delimiter = ";")
        l = []
        for ligne in reader :
            l.append(ligne)
    
    return l


def population_category(ville):
    if (int)(ville['PTOT']) < 5000:
        return 'Village (entre 0 et 5000)'
    elif (int)(ville['PTOT']) < 20000:
        return 'Ville (entre 5000 et 20000)'
    elif (int)(ville['PTOT']) < 50000:
        return 'Ville moyenne (entre 20000 et 50000)'
    elif (int)(ville['PTOT']) < 200000:
        return 'Grande ville (entre 50000 et 200000)'
    elif (int)(ville['PTOT']) >= 200000:
        return 'Metropole (au-dessus de 200000)'


def get_merged_dataframe():
    dataDefibrilateur = read_file(FILENAME_DEFIBRILLATEUR)
    dfDef = pd.DataFrame(dataDefibrilateur)

    dataCommune = read_file(FILENAME_COMMUNE)
    dfCom = pd.DataFrame(dataCommune)

    dfCom = dfCom.rename(columns={'DEPCOM': 'c_com_insee'})
    merged_df = pd.merge(dfDef, dfCom, on='c_com_insee', how='inner')

    # conversion en nombre
    merged_df['PTOT'] = pd.to_numeric(merged_df['PTOT'])
    merged_df['categoryVille'] = merged_df.apply(population_category, axis=1)
    
    return merged_df


# def main():
#     dataDefibrilateur = read_file(FILENAME_DEFIBRILLATEUR)
#     dfDef = pd.DataFrame(dataDefibrilateur)

#     dataCommune = read_file(FILENAME_COMMUNE)
#     dfCom = pd.DataFrame(dataCommune)

#     dfCom = dfCom.rename(columns={'DEPCOM': 'c_com_insee'})
#     merged_df = pd.merge(dfDef, dfCom, on='c_com_insee', how='inner')

#     merged_df['categoryVille'] = merged_df.apply(population_category, axis=1)
#     print(merged_df)

# main()