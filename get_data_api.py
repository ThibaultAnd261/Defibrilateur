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

def main():
    dataDefibrilateur = read_file(FILENAME_DEFIBRILLATEUR)
    dfDef = pd.DataFrame(dataDefibrilateur)

    dataCommune = read_file(FILENAME_COMMUNE)
    dfCom = pd.DataFrame(dataCommune)

    dfCom = dfCom.rename(columns={'DEPCOM': 'c_com_insee'})
    merged_df = pd.merge(dfDef, dfCom, on='c_com_insee', how='inner')

    # print(merged_df)
    # print(merged_df.keys())

main()