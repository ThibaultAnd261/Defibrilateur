import requests
import zipfile
from io import BytesIO

# différents urls de téléchargement des fichiers (csv/zip)
urlDownloadDefibrillateur: str = "https://www.data.gouv.fr/fr/datasets/r/edb6a9e1-2f16-4bbf-99e7-c3eb6b90794c"
urlPopulation2017: str = "https://www.insee.fr/fr/statistiques/fichier/4265429/ensemble.zip"
urlPopulation2019: str = "https://www.insee.fr/fr/statistiques/fichier/6011070/ensemble.zip"

# fonction permettant le téléchargement d'un fichier
def download_file(url:str, nameFileDownloaded:str="", fileToExtract:str=""):
    res = requests.get(url)
    
    # dans le cas où un fichier est un .zip, vérification depuis les 'headers' de la réponse
    if 'Content-Type' in res.headers and 'zip' in res.headers['Content-Type']:
        with zipfile.ZipFile(BytesIO(res.content), 'r') as zipF:
            zipF.extract(fileToExtract, '.')
            print(f'Le fichier extrait {fileToExtract} est bien enregistré.')
    else:
        with open(nameFileDownloaded, "wb") as f:
            f.write(requests.get(url).content)
            print(f'Le fichier {f} a bien été enregistré.')

def main():
    download_file(urlDownloadDefibrillateur, nameFileDownloaded="geodae.csv")
    download_file(urlPopulation2017, fileToExtract="Communes.csv")
    download_file(urlPopulation2019, fileToExtract="donnees_communes.csv")
    
main()