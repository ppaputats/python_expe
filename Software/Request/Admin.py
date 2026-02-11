# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

import pyodbc

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

def insert_BL(id_BL, id_client, nbr_pal_colis_theo, poids_theo_brut, poids_theo_net, poids):
        
    """
    Fonction : Génère des BL de test dans la table BL
    Entrée : id_operateur, nom_operateur, droit_operateur, mdp_operateur
    Sortie : True
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Vérifier si le BL existe déjà
    cursor.execute(
        "SELECT 1 FROM BL WHERE id_BL = ?",
        (id_BL,)
    )
    if cursor.fetchone() is not None:
        print(f"Le BL {id_BL} existe déjà.")
        conn.close()
        return False
    
    try :
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
                (id_BL, id_client, nbr_pal_colis_theo, poids_theo_brut, poids_theo_net, poids)
            )

        conn.commit()

    except Exception as e:
        print("Erreur lors de l'insertion du BL :", e)

    finally:
        conn.close()
        print(f"BL ajouté : {id_BL}")   
    
    return True

def insert_client(id_client, dep_livr, adresse_livr, contact):
    
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

    # Vérifier si le client existe déjà
    cursor.execute(
        "SELECT 1 FROM Client WHERE id_client = ?",
        (id_client,)
    )
    if cursor.fetchone() is not None:
        print(f"Le client {id_client} existe déjà.")
        conn.close()
        return False

    try:
        cursor.execute("""
                INSERT INTO Client (id_client, dep_livr, adresse_livr, contact)
                VALUES (?, ?, ?, ?)
            """, 
            (id_client, dep_livr, adresse_livr, contact))
        
        conn.commit()

    except Exception as e:
        print("Erreur lors de l'insertion des clients :", e)

    finally:
        conn.close()
        print(f"Client ajouté : {id_client} ")
    return True

def insert_Affaire(id_affaire, id_produit_client, poids_affaire):

    """
    Fonction : Insère une nouvelle affaire dans la table Affaire
    Entrée : id_affaire, id_produit_client, poids_affaire
    Sortie : True si insertion OK, False si déjà existant
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Vérifier si l'affaire existe déjà
    cursor.execute(
        "SELECT 1 FROM Affaire WHERE id_affaire = ?",
        (id_affaire,)
    )
    if cursor.fetchone() is not None:
        print(f"L'affaire {id_affaire} existe déjà.")
        conn.close()
        return False

    try:
        cursor.execute(
            """
            INSERT INTO Affaire (id_affaire, id_produit_client, poids_affaire)
            VALUES (?, ?, ?)
            """,
            (id_affaire, id_produit_client, poids_affaire)
        )
        conn.commit()

    except Exception as e:
        print("Erreur lors de l'insertion de l'affaire :", e)
        conn.close()
        return False

    finally:
        print(f"Affaire ajoutée : Affaire={id_affaire}")
        conn.close()

    return True

def insert_Affaire_BL(id_BL, id_affaire, quantite):

    """
    Fonction : Insère une ligne dans Affaire_BL 
    Entrée : id_BL, id_affaire, quantite
    Sortie : True si insertion OK, False si BL ou affaire inexistante
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Vérifier si le BL existe
    cursor.execute(
        "SELECT 1 FROM BL WHERE id_BL = ?",
        (id_BL,)
    )
    if cursor.fetchone() is None:
        print(f"Le BL {id_BL} n'existe pas.")
        conn.close()
        return False

    # Vérifier si l'affaire existe
    cursor.execute(
        "SELECT 1 FROM Affaire WHERE id_affaire = ?",
        (id_affaire,)
    )
    if cursor.fetchone() is None:
        print(f"L'affaire {id_affaire} n'existe pas.")
        conn.close()
        return False

    try:
        cursor.execute(
            """
            INSERT INTO Affaire_BL (id_BL, id_affaire, quantite)
            VALUES (?, ?, ?)
            """,
            (id_BL, id_affaire, quantite)
        )
        conn.commit()

    except Exception as e:
        print("Erreur lors de l'insertion dans Affaire_BL :", e)
        conn.close()
        return False

    finally:
        print(f"Affaire_BL ajoutée : BL={id_BL}")
        conn.close()

    return True
