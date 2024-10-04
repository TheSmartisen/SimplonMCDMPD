# Création d'un base de donnée

# Qui suis-je ?

- **Patrick HEM**  
  Étudiant en Développement IA | Formation Microsoft by Simplon | Disponible pour alternance dès février 2025.
  
- **LinkedIn** : [Patrick HEM](https://www.linkedin.com/in/patrick-hem-b758869a/)
  
- **Formation Simplon** : [En savoir plus sur Simplon](https://simplon.co/)
  
# Cloner le dépôt

Pour cloner ce dépôt, utilisez la commande suivante :

```bash
git clone https://github.com/TheSmartisen/SimplonMCDMPD.git
```

# Description du projet

Projet créé en adéquation du 6ème brief qui m'a été assigné sur Simplonline dans le but decréer une base de donnée avec Sqlite et python

# Fonctionnalités 

- **Python 3.x**

- **SQLlite** SQLite est une base de données relationnelle légère, embarquée et sans serveur, souvent utilisée pour des applications mobiles, des logiciels embarqués ou des tests.

# Prérequis

- Installer SQLite : https://www.sqlite.org/download.html

# Modalités pédagogiques

- Analyse des jeux de données.
  
- Élaboration d'un modèle conceptuel des données (MCD) :
  Se renseigner sur ce qu'est un MCD et utiliser un outil comme Draw.io pour le créer.

- Transformation du MCD en un modèle physique des données (MPD):
  S'aider du cahier des charges en ressources.
  
- Création et implémentation de la base de données :
  
- Implémenter la base sur un SGBD (SQLite, MySQL, PostgreSQL, etc.) et créer les tables.
  
- Programmation de l'import des données :
  
- Écrire un script Python pour importer les données dans la base de données en respectant les contraintes définies dans le MPD.
  
**Extraction les données demandées par requête SQL :**

- Les clients ayant consenti à recevoir des communications marketing.

- Les commandes d'un client spécifique.

- Le montant total des commandes du client avec ID n° 61 .

- Les clients ayant passé des commandes de plus de 100 euros.

- Les clients ayant passé des commandes après le 01/01/2023.
​
## Bonus :
Identification des données sensibles selon le RGPD et mise en place de solutions pour les protéger (chiffrement, pseudonymisation, etc.).

# Exécution des scripts

- Crée une base de donnée patoche.db, insère des jeu de donnée CSV dans le répertoire /data puis affiche le résultat SQL dans le terminal
```bash
python main.py
```

- Supprime la base de donnée patoche (si nécéssaire)
```bash
python reset.py
```

