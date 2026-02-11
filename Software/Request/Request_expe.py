# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

import pyodbc
from PyQt6.QtWidgets import QMessageBox

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

def get_connection(): 

    """
    Fonction : Se connecte à la base SQL MALAN_PESAGE
    Entrée : Vide
    Sortie : Retourne la connexion si OK, sinon None
    """

    try: 
        conn = pyodbc.connect( r"DRIVER={ODBC Driver 17 for SQL Server};" 
                                r"SERVER=SRVATS3-VM2;"
                                r"DATABASE=MALAN_PESAGE;" 
                                r"UID=paulp;" 
                                r"PWD=1234;", 
                                timeout=3 ) 
        print("Connexion SQL OK")
        return conn 
    except pyodbc.InterfaceError as e: 
        QMessageBox.critical(None, "Erreur SQL", f"Impossible de se connecter au serveur SQL.\n\nDétail : {e}") 
        return None 
    except pyodbc.OperationalError as e:
        QMessageBox.critical(None, "Erreur SQL", f"Connexion refusée par SQL Server.\n\nDétail : {e}") 
        return None 
    except Exception as e: 
        QMessageBox.critical(None, "Erreur inconnue", f"Une erreur inattendue est survenue :\n{e}") 
    return None

def bl_exists(BL):

    """
    Fonction : Vérifie si le BL existe dans les pages de saisie de palette/colis
    Entrée : Numéro de BL
    Sortie : True si existe, False sinon 
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM BL WHERE id_BL = ?",
        (BL,)
    )

    result = cursor.fetchone()
    conn.close()
    return result is not None
  
def check_login(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_operateur, droit_operateur 
        FROM Operateur 
        WHERE nom_operateur = ? AND mdp_operateur = ?
    """, (username, password))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0], row[1]   # id, droit
    return False, None


def read_last_palettes(limit=10, id_bl_filter=None):
    
    """
    Fonction : Cherche les 10 dernières palettes saisies par ordre id_palette décroissant
    Entrée : Vide
    Sortie : Colonnes des valeurs
    """

    conn = get_connection()
    if conn is None:
        print("Connexion SQL impossible")
        return []

    cursor = conn.cursor()

    try:
        top_clause = f"TOP {limit}"

        query = f"""
            SELECT {top_clause}
                pc.id_BL,
                pc.id_pal_colis,
                c.adresse_livr AS nom_client,
                b.id_AR,
                o.nom_operateur,
                pc.horodatage
            FROM Pal_colis pc
            JOIN BL b ON pc.id_BL = b.id_BL
            JOIN Client c ON b.id_client = c.id_client
            JOIN Operateur o ON pc.id_operateur = o.id_operateur
        """

        params = []

        if id_bl_filter is not None:
            query += " WHERE pc.id_BL = ?"
            params.append(id_bl_filter)

        query += " ORDER BY pc.horodatage DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return rows

    except Exception as e:
        print("Erreur SQL read_last_palettes :", e)
        return []

    finally:
        conn.close()



def get_next_id_pal_colis():
    
    """
    Fonction : Calcule l'id_pal_colis
    Entrée : Vide
    Sortie : id_pal_colis
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(id_pal_colis) FROM Pal_colis")
    row = cursor.fetchone()
    conn.close()

    if row[0] is None:
        return 1
    return row[0] + 1

def insert_pal_colis(id_pal, id_bl, type_pal, tare_pal_colis, poids, id_operateur, url_etiquette,numero_colis):
    
    """
    Fonction : Enregistre dans la base MALAN_PESAGE la nouvelle saisie pour la table Pal_colis
    Entrée : infos de prise de mesure
    Sortie : Vide (MAJ de MALAN_PESAGE table Pal_colis)
    """

    conn = get_connection() 
    cursor = conn.cursor() 
    cursor.execute(""" INSERT INTO Pal_colis (id_pal_colis, id_bl, type_pal_colis, tare_pal_colis, poids_pal_colis, id_operateur, url_etiquette, horodatage, numero_pal_colis) VALUES (?, ?, ?, ?, ?, ?, ?,GETDATE(), ?) """, (id_pal, id_bl, type_pal, tare_pal_colis, poids, id_operateur, url_etiquette, numero_colis)) 
    conn.commit() 
    conn.close()

def insert_photo(id_pal, url1, url2):
    
    """
    Fonction : Enregistre dans la base MALAN_PESAGE la nouvelle saisie pour la table Photo
    Entrée : infos de prise de mesure
    Sortie : Vide (MAJ de MALAN_PESAGE table Photo)
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Photo (id_pal_colis, url_photo1, url_photo2)
        VALUES (?, ?, ?)
    """, (id_pal, url1, url2))

    conn.commit()
    conn.close()

def count_colis_for_bl(id_bl):
    
    """
    Fonction : Compte le numéro de la palette pour le Bl en particulier
    Entrée : Numéro de BL
    Sortie : Numéro de la palette
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Pal_colis WHERE id_bl = ?", (id_bl,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return 0
    return row[0]

def get_client_data(id_bl):
    
    """
    Fonction : Permet de connaître les infos clients
    Entrée : Numéro de BL
    Sortie : contact, adresse_livr, dep_livre, id_AR, nbr_colis_theo, poids_theo_net
    """

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT 
            c.contact,
            c.adresse_livr,
            c.dep_livr,
            b.id_AR,
            b.nbr_pal_colis_theo,
            b.poids_theo_net
        FROM BL b
        JOIN Client c ON b.id_client = c.id_client
        WHERE b.id_BL = ?
    """

    cursor.execute(sql, (id_bl,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "contact": row[0],
        "adresse_livr": row[1],
        "dep_livre": row[2],
        "id_AR": row[3],
        "nbr_colis_theo": row[4],
        "poids_theo_net": row[5],
    }

def get_pal_data(id_pal_colis):
    """
     Retourne (poids, numero_colis) pour un id_pal_colis donné.
    """
    try:
        conn = get_connection() 
        cursor = conn.cursor()

        cursor.execute("""
                SELECT poids_pal_colis, numero_pal_colis
                FROM pal_colis
                WHERE id_pal_colis = ?
            """, (id_pal_colis))

        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0], row[1]   # poids, numero_colis
        else:
            return None, None

    except Exception as e:
        print("Erreur SQL get_pal_data :", e)
        return None, None