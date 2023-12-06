import csv
from collections import defaultdict

FILENAME = "geodae.csv"

def read_file (filename):

    with open (filename, mode = 'r', encoding= 'utf8') as f :
        reader = csv.DictReader(f , delimiter = ";")
        l = []
        for ligne in reader :
            l.append(ligne)
    
        
    return l

    

def main():
    data = read_file(FILENAME)
    print (data)

main()