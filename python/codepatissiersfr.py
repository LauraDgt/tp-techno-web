# Importation des bibliothèques nécessaires
import requests
from bs4 import BeautifulSoup
import csv             #pour créer et manipuler des fichiers CSV
import os

def scraper_patissiers_francais():
    """
    Scrape de la liste des pâtissiers français depuis Wikipedia
    """
    print("Scraping de la page des pâtissiers français...")
    
   # URL de la page Wikipedia des pâtissiers français à scraper
    url = "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:P%C3%A2tissier_fran%C3%A7ais"
    
    # Headers pour éviter le blocage par Wikipédia
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # Récupération de la page web avec envoi requête HTTP par GET
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parsing du HTML BeautifulSoup transforme le HTML en un objet manipulable
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Recherche de la div principale qui contient les pâtissiers
        # Sur Wikipedia, les catégories utilisent la classe 'mw-category'
        content_div = soup.find('div', {'class': 'mw-category'})
        # Liste pour stocker les données des pâtissiers
        patissiers_data = []
        
        if content_div:
            # Extraction de tous les liens (noms des pâtissiers)
            # On trouve les liens dans des balises <a> à l'intérieur de la div
            # Chaque lien représente un pâtissier
            links = content_div.find_all('a')
            
            for link in links:
                nom = link.get_text(strip=True)   # Strip=True pour enlever les espaces inutiles
                # Les href sont relatifs, on ajoute le domaine de Wikipedia
                lien_wikipedia = "https://fr.wikipedia.org" + link.get('href', '')

                if nom:  # Vérifie que le nom n'est pas vide + ajout de dictionnaire avec toutes les infos du pâtissier
                    patissiers_data.append({
                        'nom_patissier': nom,   # Nom scrapé depuis la page
                        'specialite': 'Pâtisserie française',    # info ajoutée manuellement
                        'nationalite': 'Française',    # info déduite du contexte
                        'lien_wikipedia': lien_wikipedia    # Lien vers la page détaillée
                    })

        # Affichage des résultats dans le terminal
        print(f"{len(patissiers_data)} pâtissiers trouvés !")
        
        # Affichage détaillé de la liste des pâtissiers
        print("\nListe des pâtissiers français trouvés :")
        for i, patissier in enumerate(patissiers_data):
            print(f"  {i+1}. {patissier['nom_patissier']}")
        
        # Tentative de sauvegarde des données dans un fichier CSV sur le Bureau
        try:
            # Construction du chemin vers le Bureau utilisateur
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            csv_path = os.path.join(desktop_path, 'patissiers_francais.csv')

            # Création et écriture du fichier CSV
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:

                # Définition des noms de colonnes
                fieldnames = ['nom_patissier', 'specialite', 'nationalite', 'lien_wikipedia']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Écriture de l'en-tête du CSV
                writer.writeheader()

                # Écriture de chaque ligne de données
                for patissier in patissiers_data:
                    writer.writerow(patissier)

            print(f"\nFichier sauvegardé sur le Bureau : 'patissiers_francais.csv'")
            
        except Exception as e:
            # En cas d'erreur lors de la sauvegarde, afficher les données formatées dans le terminal
            print(f"\nImpossible de sauvegarder le fichier, mais voici les données :")
            print("Copie-colle ceci dans un fichier CSV :")
            print("nom_patissier,specialite,nationalite,lien_wikipedia")
            for patissier in patissiers_data:
                print(f"{patissier['nom_patissier']},Pâtisserie française,Française,{patissier['lien_wikipedia']}")
        
        return True      # Indique que le scraping a réussi
        
    except Exception as e:
        # Gestion des erreurs lors de la requête ou du parsing
        print(f"ERREUR : {e}")
        return False       # Indique que le scraping a échoué

def main():
    """
    Fonction principale
    """
    print("=" * 60)
    print("SCRAPER WIKIPEDIA - PÂTISSIERS FRANÇAIS")
    print("=" * 60)

    # Appel de la fonction principale de scraping
    success = scraper_patissiers_francais()
    
    # Affichage du résultat final
    if success:
        print("\n" + "=" * 60)
        print("SCRAPING RÉUSSI !")
        print("Page source : https://fr.wikipedia.org/wiki/Catégorie:Pâtissier_français")
        print("=" * 60)
    else:
        print("\n Le scraping a échoué")

if __name__ == "__main__":
    main()