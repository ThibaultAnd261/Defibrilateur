import csv
import pandas as pd
import requests

FILENAME = "geodae.csv"

def read_file (filename):

    with open (filename, mode = 'r', encoding= 'utf8') as f :
        reader = csv.DictReader(f , delimiter = ";")
        l = []
        for ligne in reader :
            l.append(ligne)
    
        
    return l

def api_call(codeInsee):
    response = requests.get('https://geo.api.gouv.fr/communes/'+codeInsee+'?fields=nom,population&format=json&geometry=centre')
    # print('https://geo.api.gouv.fr/communes/'+codeInsee+'?fields=nom,population&format=json&geometry=centre') 
    print(response.json())
    

def main():
    data = read_file(FILENAME)
    # print (data)
    df = pd.DataFrame(data)
    # print(df)
    # print(df.keys())
    # print(df['c_com_insee'])

    # print(df['c_com_insee'][0])

    api_call(df['c_com_insee'][0])

    # for index, row in df.iterrows():
    #     print(row['c_com_insee'])

main()