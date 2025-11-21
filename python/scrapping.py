
import requests                     # (Vu, Diapo 6) Pour se connecter au site 
from bs4 import BeautifulSoup      # (Vu, Diapo 8) Pour analyser le HTML [
import csv                          # (Pas dans les slides) Pour écrire les fichiers CSV
import os                           # (Pas dans les slides) Pour créer des dossiers
import re                           # (Pas dans les slides) Pour nettoyer les noms de fichiers

# --- 1. CONFIGURATION (VU DANS LE COURS) ---

# L'URL de la page Wikipedia choisie (Exigence Exercice 7)
URL = "https://fr.wikipedia.org/wiki/Liste_de_p%C3%A2tisseries"

# Le User-Agent ( Diapo 8)
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
} 

# Dossier de sortie pour les CSV (Exigence Exercice 7)
# (Le script va le créer s'il n'existe pas)
DATA_DIR = "data"



# Une petite fonction pour nettoyer les titres (ex: "France [modifier]")
# et les transformer en noms de fichiers valides (ex: "patisseries_france.csv")

def nettoyer_nom_fichier(titre):
    """Transforme un titre en nom de fichier CSV propre."""
    # Enlève "[modifier]" que Wikipedia ajoute partout
    titre_propre = titre.replace('[modifier]', '').strip()
    # Met en minuscule et remplace les espaces par des underscores
    titre_propre = titre_propre.lower().replace(' ', '_')
    # Garde seulement les lettres, chiffres et underscores
    titre_propre = re.sub(r'[^a-z0-9_]', '', titre_propre)
    # Ajoute le préfixe et l'extension
    return f"patisseries_{titre_propre}.csv"


# --- 3. DÉBUT DU SCRIPT PRINCIPAL ---

print(f"Début du scraping de : {URL}")

# Créer le dossier 'data' s'il n'existe pas 
os.makedirs(DATA_DIR, exist_ok=True)

# Connexion à la page 
try:
    response = requests.get(URL, headers=HEADERS) 
    # Bonne pratique : vérifie si le serveur a répondu OK (200)
    response.raise_for_status() 
except requests.exceptions.RequestException as e:
    print(f"ERREUR : Impossible de se connecter à l'URL. {e}")
    exit() # Quitte le script si on ne peut pas se connecter

print("Connexion réussie. Analyse du HTML...")

# Création de la "Soupe" 
soup = BeautifulSoup(response.text, 'html.parser') 

# --- 4. RECHERCHE DES DONNÉES PERTINENTES  ---
# Nous cherchons les tableaux, car ce sont des données structurées.
# C'est bien plus "pertinent" que des titres h2.

# On trouve TOUS les tableaux 
# (La balise 'table' n'est pas dans les slides, mais la logique est la même)
tables = soup.find_all('table', class_='wikitable')

if not tables:
    print("ERREUR : Aucun tableau de classe 'wikitable' trouvé sur la page.")
    exit()

print(f"Trouvé {len(tables)} tableaux (données pertinentes) à traiter.")

# --- 5. TRAITEMENT ET SAUVEGARDE EN CSV ---

# On boucle sur chaque tableau trouvé
for i, table in enumerate(tables):
    
    # 5a. Trouver un titre "cohérent" pour le fichier
    titre_table = f"table_inconnue_{i+1}" 
    # On cherche le titre h2 ou h3 qui précède le tableau
    tag_titre_precedent = table.find_previous(['h2', 'h3'])
    if tag_titre_precedent:
        span_titre = tag_titre_precedent.find('span', class_='mw-headline')
        if span_titre:
            titre_table = span_titre.text
            
    # On crée le nom de fichier propre
    nom_fichier_csv = os.path.join(DATA_DIR, nettoyer_nom_fichier(titre_table))

    # 5b. Ouvrir le fichier CSV 
    try:
        with open(nom_fichier_csv, 'w', newline='', encoding='utf-8') as f:
            # On crée "l'écrivain" CSV
            writer = csv.writer(f)
            
            print(f"\nTraitement du tableau '{titre_table}'...")
            print(f"Sauvegarde dans '{nom_fichier_csv}'...")
            
            # 5c. Extraire les "en-têtes de colonnes cohérentes" (<th>)
           
            ligne_header = table.find('tr')
            if not ligne_header:
                continue # Saute ce tableau s'il est vide
                
            headers = [th.text.strip() for th in ligne_header.find_all('th')]
            
            # On écrit la ligne d'en-tête dans le CSV
            writer.writerow(headers)
            
            # 5d. Extraire les lignes de données (<tr> / <td>)
            
            lignes_data = table.find_all('tr')[1:] # On saute la ligne d'en-tête
            
            count = 0
            for ligne in lignes_data:
                cellules = [td.text.strip() for td in ligne.find_all('td')]
                # On vérifie que la ligne n'est pas vide et correspond aux en-têtes
                if len(cellules) == len(headers):
                    writer.writerow(cellules)
                    count += 1
            
            print(f"{count} lignes de données enregistrées pour '{titre_table}'.")

    except IOError as e:
        print(f"ERREUR : Impossible d'écrire dans le fichier {nom_fichier_csv}. {e}")

print("\n--- Scraping terminé. ---")