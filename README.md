# TP – Introduction aux Technologies Web  
Master MSI M1 – 2025/2026  
Par : Laura DAGUET, Lina SAFI, Ashani GOBALASAMY, Eunice KOUASSI

## Objectif du projet
Développer un site web mono-page en HTML/CSS, intégrant :
- des données API (Open Data),
- une visualisation avec Flourish,
- un web scraping Python,
- un design cohérent (palette, typographies, images libres).

Le thème choisi : **La pâtisserie française**.

## Contenu du repository
- `TP-DAGUET-SAFI-KOUASSI-GOBALASAMY-TECHNO-WEB.pdf` : document PDF complet comprenant les réponses aux exercices.
- `/site-web` :  
  - `index.html` : page principale  
  - feuilles de style CSS  
  - pages CV individuelles  
  - illustrations libres de droits
- `/data` :  
  - `data.json` : données API brutes  
  - `data-modif.json` : données adaptées pour Flourish  
  - fichiers CSV obtenus via web scraping
- `/python` :  
  - script de web scraping commenté  
  - fichiers générés

## Thème & design
- Palette pastel (vanille, crème, rose tendre, caramel, amande…).  
- Images provenant de Canva, Pexels, Unsplash.

## Données & API
API utilisée :  
`https://recherche-entreprises.api.gouv.fr/search?q=patisserie&activite_principal=10.71D&page=1&per_page=25`  
(voir explication page 3 du PDF :contentReference[oaicite:4]{index=4})

Visualisation Flourish intégrée au site web (Exercice 4–5).

## Web scraping
Pages Wikipedia utilisées :  
- Liste de pâtisseries : https://fr.wikipedia.org/wiki/Liste_de_pâtisseries  
- Catégorie : pâtissiers français : https://fr.wikipedia.org/wiki/Catégorie:Pâtissier_français  
(voir justification et problèmes rencontrés pages 4–5 du PDF :contentReference[oaicite:5]{index=5})

## Licence
Usage académique.
