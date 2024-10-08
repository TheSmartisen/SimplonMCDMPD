import sqlite3, csv
from datetime import datetime
import os


def is_valid_date(text, date_format='%Y-%m-%d'):
    try:
        datetime.strptime(text, date_format)
        return True
    except ValueError:
        return False

def print_table(headers, rows):
    print(f"{' | '.join(headers)}")
    print("-" * (len(headers) * 20))  # Divider for header
    for row in rows:
        print(" | ".join(str(item) for item in row))


dbName = "patoche.db"

# Essayer de se connecter à la base de données
try:
    con = sqlite3.connect(dbName)
    cursor = con.cursor()
except sqlite3.Error as e:
    print(f"Erreur lors de la connexion à la base de données: {e}")
    exit()

# Création des tables dans un bloc try-except
try:
    # Créer la table Client
    cursor.execute('''CREATE TABLE IF NOT EXISTS Client
                     (Client_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                     Nom TEXT NOT NULL, 
                     Prenom TEXT NOT NULL, 
                     Email TEXT NOT NULL UNIQUE, 
                     Telephone TEXT, 
                     Date_Naissance TEXT,
                     Adresse TEXT,
                     Consentement_Marketing INTEGER NOT NULL CHECK (Consentement_Marketing IN (0, 1)) )''')

    # Créer la table Commande
    cursor.execute('''CREATE TABLE IF NOT EXISTS Commande
                     (Commande_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                     Date_Commande TEXT NOT NULL,
                     Montant_Commande REAL NOT NULL, 
                     Client_ID INTEGER,
                     FOREIGN KEY (Client_ID) REFERENCES Client (Client_ID))''')
except sqlite3.Error as e:
    print(f"Erreur lors de la création des tables : {e}")
    con.close()
    exit()

# Chemins des fichiers CSV
Client_file = 'data/jdd_clients.csv'
Commande_file = 'data/jdd_commande.csv'

# Vérifier si le fichier Client existe
if os.path.exists(Client_file):
    try:
        # Lire le fichier .CSV puis l'ajouter à la table Client
        with open(Client_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            # Skipper la première ligne si c'est une en-tête
            next(reader, None)

            nbinsert = 0
            # Boucle pour insérer les lignes du CSV dans la table SQLite
            for row in reader:
                nom = row[1]
                prenom = row[2]
                email = row[3]
                telephone = row[4]
                date_naissance = row[5]
                adresse = row[6]
                consentement_marketing = int(row[7])

                # Vérification avant insertion
                cursor.execute('''
                        SELECT COUNT(*)
                        FROM Client
                        WHERE Nom = ? 
                        AND Prenom = ? 
                        AND Email = ? 
                        AND Telephone = ? 
                        AND Date_Naissance = ? 
                        AND Adresse = ? 
                        AND Consentement_Marketing = ?
                    ''', (nom, prenom, email, telephone, date_naissance, adresse, consentement_marketing))
                exists = cursor.fetchone()[0]

                if exists == 0:
                    nbinsert += 1
                    if is_valid_date(date_naissance):
                        cursor.execute('''
                                     INSERT INTO 
                                        Client (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
                                     VALUES (?, ?, ?, ?, ?, ?, ?)
                                 ''', (nom, prenom, email, telephone, date_naissance, adresse, consentement_marketing))

            if nbinsert > 0:
                con.commit()
    except (sqlite3.Error, csv.Error) as e:
        print(f"Erreur lors du traitement du fichier Client : {e}")
else:
    print(f"Le fichier {Client_file} est introuvable. Veuillez vérifier son emplacement.")

# Vérifier si le fichier Commande existe
if os.path.exists(Commande_file):
    try:
        # Lire le fichier .CSV pour les Commande et l'ajouter à la table Commande
        with open(Commande_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            # Skipper la première ligne si c'est une en-tête
            next(reader, None)

            nbinsert = 0
            # Boucle pour insérer les lignes du CSV dans la table SQLite
            for row in reader:
                client_id = int(row[1])
                date_commande = row[2]
                montant_commande = float(row[3])

                # Vérifier si le client existe dans la table Client
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM Client
                    WHERE Client_ID = ?
                ''', (str(client_id),))
                client_existe = cursor.fetchone()[0]

                if client_existe > 0:
                    # Vérifier si la commande existe déjà pour éviter les doublons
                    cursor.execute('''
                        SELECT COUNT(*)
                        FROM Commande
                        WHERE Client_ID = ? 
                        AND Date_Commande = ? 
                        AND Montant_Commande = ?
                    ''', (client_id, date_commande, montant_commande))
                    commande_exists = cursor.fetchone()[0]

                    if commande_exists == 0:  # La commande n'existe pas, donc on peut l'insérer
                        if is_valid_date(date_commande):
                            cursor.execute('''
                                             INSERT INTO 
                                                Commande (Date_Commande, Montant_Commande, Client_ID)
                                             VALUES (?, ?, ?)
                                         ''', (date_commande, montant_commande, client_id))
                            nbinsert += 1
                    else:
                        print(f"Commande déjà existante pour le client {client_id} à la date {date_commande}")

            if nbinsert > 0:
                con.commit()
    except (sqlite3.Error, csv.Error) as e:
        print(f"Erreur lors du traitement du fichier Commande : {e}")
else:
    print(f"Le fichier {Commande_file} est introuvable. Veuillez vérifier son emplacement.")

### Ajout des requêtes demandées :

try:
    # 1. Client ayant consenti à recevoir des communications marketing
    print("\n--- Requête 1 : Client ayant consenti à recevoir des communications marketing ---")
    query_1 = '''
            SELECT Client_ID, Nom, Prenom, Email 
            FROM Client
            WHERE Consentement_Marketing = 1
        '''
    print(f"SQL:\n{query_1}\n")
    cursor.execute(query_1)
    Client_marketing = cursor.fetchall()

    if Client_marketing:
        print_table(['Client_ID', 'Nom', 'Prenom', 'Email'], Client_marketing)
    else:
        print("Aucun client n'a consenti à recevoir des communications marketing.")

    # 2. Commande d'un client spécifique (par exemple Client_ID = 61)
    print("\n--- Requête 2 : Commande d'un client spécifique (ID = 61) ---")
    client_id_specifique = 61
    query_2 = '''
            SELECT Commande_ID, Date_Commande, Montant_Commande
            FROM Commande
            WHERE Client_ID = ?
        '''
    print(f"SQL:\n{query_2}\n")
    cursor.execute(query_2, (client_id_specifique,))
    Commande_client_specifique = cursor.fetchall()

    if Commande_client_specifique:
        print_table(['Commande_ID', 'Date_Commande', 'Montant_Commande'], Commande_client_specifique)
    else:
        print(f"Aucune commande trouvée pour le client avec l'ID {client_id_specifique}.")

    # 3. Montant total des Commande du client avec ID n° 61
    print("\n--- Requête 3 : Montant total des Commande du client avec ID 61 ---")
    query_3 = '''
            SELECT SUM(Montant_Commande)
            FROM Commande
            WHERE Client_ID = ?
        '''
    print(f"SQL:\n{query_3}\n")
    cursor.execute(query_3, (client_id_specifique,))
    montant_total_61 = cursor.fetchone()[0]

    print(f"Montant total des Commande du client ID {client_id_specifique}: {montant_total_61} euros\n")

    # 4. Client ayant passé des Commande de plus de 100 euros
    print("\n--- Requête 4 : Client ayant passé des Commande de plus de 100 euros ---")
    query_4 = '''
            SELECT DISTINCT c.Client_ID, c.Nom, c.Prenom, c.Email
            FROM Client c
            JOIN Commande o ON c.Client_ID = o.Client_ID
            WHERE o.Montant_Commande > 100
        '''
    print(f"SQL:\n{query_4}\n")
    cursor.execute(query_4)
    Client_plus_100 = cursor.fetchall()

    if Client_plus_100:
        print_table(['Client_ID', 'Nom', 'Prenom', 'Email'], Client_plus_100)
    else:
        print("Aucun client n'a passé de commande de plus de 100 euros.")

    # 5. Client ayant passé des Commande après le 01/01/2023
    print("\n--- Requête 5 : Client ayant passé des Commande après le 01/01/2023 ---")
    query_5 = '''
            SELECT DISTINCT c.Client_ID, c.Nom, c.Prenom, c.Email
            FROM Client c
            JOIN Commande o ON c.Client_ID = o.Client_ID
            WHERE o.Date_Commande > '2023-01-01'
        '''
    print(f"SQL:\n{query_5}\n")
    cursor.execute(query_5)
    Client_apres_2023 = cursor.fetchall()

    if Client_apres_2023:
        print_table(['Client_ID', 'Nom', 'Prenom', 'Email'], Client_apres_2023)
    else:
        print("Aucun client n'a passé de commande après le 01/01/2023.")

except sqlite3.Error as e:
    print(f"Erreur lors de l'exécution des requêtes : {e}")

# Fermer la connexion
con.close()
