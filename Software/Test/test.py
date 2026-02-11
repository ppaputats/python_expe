# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

import pyodbc
import random

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------


# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------


def get_connection():

    """
    Fonction : Se connecte à la base de donnée MALAN_PESAGE
    Entrée :
    Sortie : Connexion
    """

    conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=SRVATS3-VM2;"
    r"DATABASE=MALAN_PESAGE;"
    r"UID=paulp;"
    r"PWD=1234;")
    print("Connexion ok")
    return conn

def insert_operateur(id_operateur, nom_operateur, droit_operateur, mdp_operateur):

    """
    Fonction : Insère un nouvel opérateur dans la table Operateur
    Entrée : id_operateur, nom_operateur, droit_operateur, mdp_operateur
    Sortie : True si insertion OK, False si déjà existant
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Vérifier si l'opérateur existe déjà
    cursor.execute(
        "SELECT 1 FROM Operateur WHERE id_operateur = ?",
        (id_operateur,)
    )
    if cursor.fetchone() is not None:
        print(f"L'opérateur {id_operateur} existe déjà.")
        conn.close()
        return False

    # Insertion
    cursor.execute(
        """
        INSERT INTO Operateur (id_operateur, nom_operateur, droit_operateur, mdp_operateur)
        VALUES (?, ?, ?, ?)
        """,
        (id_operateur, nom_operateur, droit_operateur, mdp_operateur)
    )

    conn.commit()
    conn.close()

    print(f"Opérateur ajouté : {id_operateur} / {nom_operateur} / {droit_operateur}")
    return True

"""insert_operateur(
    id_operateur=1234,
    nom_operateur="ppaput",
    droit_operateur="admin",
    mdp_operateur="1234"
)"""

def init_bl():
        
    """
    Fonction : Génère des BL de test dans la table BL
    Entrée : id_operateur, nom_operateur, droit_operateur, mdp_operateur
    Sortie : True si insertion OK, False si déjà existant
    """

    conn = get_connection()
    cursor = conn.cursor()

    for i in range(1, 11):
        cursor.execute(
            """
            INSERT INTO BL (
                id_BL,
                id_client,
                nbr_pal_colis_theo,
                poids_theo_brut,
                poids_theo_net,
                poids_reel,
                id_AR,
                erreur_poids
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                i,      # id_BL
                i,      # id_client
                i,      # nbr_pal_colis_theo
                1.0,    # poids_theo_brut
                1.0,    # poids_theo_net
                1.0,    # poids_réel
                1,      # id_AR
                0.0     # erreur_poids
            )
        )

    conn.commit()
    conn.close()
    print("10 BL créés (id_BL 1 à 10)")


#init_bl()


def insert_random_clients(n=10):
    
    """
    Fonction : Insère de nouveaux clients de test dans la table Client
    Entrée : nombre de clients
    Sortie : True si insertion OK, False si déjà existant
    """

    conn = get_connection()
    if conn is None:
        print("Impossible de se connecter à SQL Server")
        return

    cursor = conn.cursor()

    noms = [
        "Dupont", "Martin", "Bernard", "Durand", "Petit",
        "Robert", "Richard", "Moreau", "Simon", "Laurent"
    ]

    villes = [
        "Paris", "Lyon", "Marseille", "Toulouse", "Nice",
        "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille"
    ]

    try:
        # Récupérer le dernier id_client
        cursor.execute("SELECT ISNULL(MAX(id_client), 0) FROM Client")
        last_id = cursor.fetchone()[0]

        for i in range(n):
            new_id = last_id + i + 1
            nom = random.choice(noms)
            ville = random.choice(villes)
            dep = random.randint(1, 95)
            contact = f"{nom.lower()}@exemple.com"

            cursor.execute("""
                INSERT INTO Client (id_client, dep_livr, adresse_livr, contact)
                VALUES (?, ?, ?, ?)
            """, (new_id, dep, ville, contact))

        conn.commit()
        print(f"{n} clients aléatoires ont été insérés.")

    except Exception as e:
        print("Erreur lors de l'insertion des clients :", e)

    finally:
        conn.close()


#insert_random_clients(10)