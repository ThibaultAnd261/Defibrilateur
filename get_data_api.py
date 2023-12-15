import csv
import pandas as pd
import requests

FILENAME = "geodae.csv"

# liste_pop = [{}]
liste_pop = dict()

def read_file (filename):

    with open (filename, mode = 'r', encoding= 'utf8') as f :
        reader = csv.DictReader(f , delimiter = ";")
        l = []
        for ligne in reader :
            l.append(ligne)
    
        
    return l

def api_call(codeInsee):
    response = requests.get('https://geo.api.gouv.fr/communes/'+codeInsee+'?fields=nom,population&format=json&geometry=centre')
    resJson = response.json()
    nom = resJson['nom']
    population = resJson['population']
    liste_pop[nom] = population
    

def main():
    data = read_file(FILENAME)
    df = pd.DataFrame(data)

    for index, row in df.iterrows():
        if index == 10:
            break
        api_call(row['c_com_insee'])

    print(liste_pop)

main()