# ---------------------------------------------------------
# Importantion bibliothèques et fonctions
# ---------------------------------------------------------

import os
import requests
from datetime import datetime

# ---------------------------------------------------------
# Définition des variables
# ---------------------------------------------------------

# ---------------------------------------------------------
# Définition des fonctions
# ---------------------------------------------------------

def Connection_printer(ip, port):
    
    """
    Fonction : Permet de se connecter à l'imprimante
    Entrée : Adresse ip et port de l'imprimante
    Sortie : Booléen de connexion
    """

    print("Connexion imprimante simulée") 
    return True

def ZPLCreator_printer(id_bl, id_pal, operateur, client, poids, numero_colis):
    
    """
    Fonction : Permet de créer le fichier zpl pour l'étiquette d'expediiton pour chaque palette
    Entrée : id_bl, id_pal, operateur, client, poids, numero_colis
    Sortie : Fichier zpl correspondant
    """

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    zpl = f"""

^XA





^PW800
^LL800
^CI28

^CF0,150
^FO30,30^FD{client['dep_livre']}^FS

^CF0,35
^FO250,30^FD{client['contact']}^FS
^FO250,75^FD{client['adresse_livr']}^FS

^CF0,30
^FO30,200^FDHorodatage : {timestamp}^FS
^FO30,240^FDBL : {id_bl}^FS
^FO30,280^FDOpérateur : {operateur}^FS

^FO30,340^FDID AR : {client['id_AR']}^FS
^FO30,380^FDNb colis théorique : {client['nbr_colis_theo']}^FS
^FO30,420^FDNuméro colis/palette : {numero_colis}^FS

^FO30,480^FDPoids théorique net : {client['poids_theo_net']} kg^FS
^FO30,520^FDPoids mesuré : {poids} kg^FS



^FO30,650^XGATS.GRF,1,1^FS

^CF0,40
^FO50,600^FDATS Laser^FS
^FO50,635^FD6 Route de Campeyroux^FS
^FO50,670^FD12740 La Loubière^FS
^FO50,705^FD00 00 00 00 00^FS
^FO50,740^FDadresse.adresse@atslaser.fr^FS

^FO520,520^GFA,9380,9380,35,,:::::::::::::::J03iF,:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::J03hKF87SF,J03hIFEI01RF,J03TFEJ07IF801IFJ01FE003KFCI03QF,J03TFEJ03IF803IF8I01FF003JFK07QF,J03TFCJ03IF8T03IFCK03QF,J03TFDJ01IF8T03FFEM0QF,J03TFCJ01IF8T03FDCM019OF,J03TFEJ01IF8T03F9O047NF,J03TF8K0IF8T03F2O013NF,J03TFCK0IF8T03EQ01NF,J03TF4K07FF8T03CR0NF,J03TF8K07FF8T038R07MF,:J03TFL03FF8T03S0NF,J03TFL03FF8T03R01NF,J03TFL01FF8T03R03NF,J03SFEL01FF8T02J018K027NF,J03SFEM0FF801IF8I03FE002J077FCI04OF,J03SFCM0FF801IF8I01FEM0JF8409OF,J03SFCM0FF807IF8I01FEL01JFE61BOF,J03SF8M07MF8I07JFCI03KFB37OF,J03SF8L01MFE8I07JFCI03LFEPF,J03SFN0NF8I07JFCI03WF,J03SFN0NF8I07JFCI07WF,:J03RFEN07MF8I07JFCI03WF,J03RFEN07MF8I0KFCI03WF,J03RFCI018I03MF8I0KFCI03WF,J03RFCI018I03MF8I0KFCI01WF,J03RF8I01CI01MF8I0KFCJ0WF,J03RF8I03CI01MF8I0KFCJ033UF,J03RF8I03CI01MF8I0KFEK083TF,J03RFJ07EJ0MF8I0KFEM03SF,J03RFJ07EJ0MF8I0KFEN07RF,J03QFEJ0FFJ07LF8I0LFN01RF,J03QFEJ0FFJ07LF8I0LF8N07QF,J03QFCI01FF8I03LF8I0LF8N07QF,J03QFCI01FF8I03LF8I0LFCN07QF,J03QF8I03FFCI01LF8I0LFEN01QF,J03QF8I03FFCI01LF8I0MF2N077OF,J03QF80017FFCJ0BKF8I0MF9N03BOF,J03QFJ07FFEJ0LF8I0MFD8N09OF,J03QFI02IFEJ05KF8I0NFEN067NF,J03PFEI02JFJ05KF8I0OF8N03NF,J03PFEI04JFJ07KF8I0OFEN01NF,J03PFCI05JF8I02KF8I0PF8N0NF,J03PFCI0DJF8I037JF8I0QFN0NF,J03PF8I0BJFCI017JF8I0QF8M07MF,J03PF8001KFCI013JF8I0PFEN03MF,J03PFI01KFEJ0BJF8I0QFCM03MF,J03OFDI01KFEJ0BJF8I0RFM01MF,J03OFAI038I03EJ01JF8I0SFL01MF,J03OFEI07FI01FJ05JF8I0SFEK01MF,J03OFO01FK0JF8I0TF8K0MF,J03OF4O0F8I02JF8I0TFE6J0MF,J03NFE4O0F8J07IF8I0UFAJ0MF,J03NFEP07DJ07IF8I0VFJ0MF,J03NFC8O07CJ03IF8I0VFJ0MF,J03NFCP03E8I03IF8I0VFJ0MF,J03NF8P03E8I01IF8I0VFJ0MF,J03NF8P03FCI01IF8I0VFJ0MF,J03NF8P01F4J0IF8I0VFJ0MF,J03NFQ01FEJ0IF8I0NFCLFBJ0MF,J03NFR0FEJ07FF8I0NF87KF6I01MF,J03MFER0FFJ07FF8I0MF901JFE4I01MF,J03MFER07FJ07FF8I0MF20063FF08I01MF,J03MFCI01IFK07F8I03FF8I0LFE4I08M01MF,J03MFCI01FF8K03F8I03FF8I0LFCR03MF,J03MF8I03KF801FF8I01FF8I0LF8R03MF,J03MF8I03PFCI01FF8I0LFS07MF,J03MFJ07PFCJ0FF8I0KFES07MF,J03MFJ07PFEJ0FF8I0LFS0NF,J03MFJ07PFEJ07F8I0LF8R0NF,J03LFEJ0RFJ07F8I0LFCQ01NF,J03LFEJ0RFJ07F8I0MF2O013NF,J03LFCI01RFJ03F8I0MF98O07NF,J03LFCI01RF8I03E8I0MFEEN08OF,J03LF8I03RF8I01F8I0OFCL03BOF,J03LF8I03RFCI01FJ0PFL0QF,J03LFI07TFEI0F8I0QFJ07QF,J03LFI01SFEJ0EJ0PFEJ07QF,J03hJF8I07QF,J03hKFE0SF,J03iF,::::::J03gNFE0gPF,::::::J03gNFE0FFC0387FF03JF1IF0F0NF,J03gNFE0FFJ07F800IFI0FF080NF,J03gNFE0FCJ07FI07FEI07FI0NF,J03gNFE0F8J07EI03FCI03FI0NF,J03gNFE0F81F807C1F83F81F01F01OF,J03gNFE0F07FE07C1FE1F07FC1F03OF,J03gNFE0F0FFE07C1FE1F0FFE0F07OF,J03gNFE0E0IF07C1FE1E1IF0F07OF,J03gNFE0E0IF07E007DEK0F0PF,J03gNFE0E1IF87EI07EK0F0PF,J03JFEg01FFE0E1IF87F8003EK070PF,J03JFEgG0FFE0E1IF8786001EK070PF,J03JFEg01FFE0E0IF0787F81E1IF0F0PF,J03gNFE0F0IF0787FE1E1FFE0F0PF,J03gNFE0F07FE07C3FE1E0FFE0F0PF,J03gNFE0F03FC07C1FE1F07FC1F0PF,J03gNFE0F806007C0301F81F03F0PF,J03gNFE0FCJ07EI03F8I03F0PF,J03gNFE0FEJ07FI07FEI07F0PF,J03gNFE0FF80107FC00IF001FF0PF,J03iF,::::::::::::::::::::::::::::::::::::::::::::::::::::::::::,:::::::::^FS
^XZ

"""
    return zpl

def ZPLSend_printer(socket_printer, zpl):
       
    """
    Fonction : Envoi du fichier zpl
    Entrée : socket_printer, zpl
    Sortie : Bool
    """

    print("ZPL envoyé (simulation)")
    return True

def ZPL_to_PNG(zpl, output_path):
      
    """
    Fonction : Convertit l'étiquette ZPL en PNG
    Entrée : zpl, output_path
    Sortie : Vide (étiquette enregistrée)
    """

    url = "http://api.labelary.com/v1/printers/8dpmm/labels/4x4/0/"
    files = {'file': zpl.encode('utf-8')}
    print("Chemin absolu :", os.path.abspath(output_path))
    try:
        response = requests.post(url, files=files, stream=True)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print("PNG généré :", output_path)
        else:
            print("Erreur conversion PNG :", response.text)

    except Exception as e:
        print("Erreur API Labelary :", e)

def Close_printer(ack):
        
    """
    Fonction : Ferme le connexion avec l'imprimante
    Entrée : Vide
    Sortie : Booléen de fermeture
    """
        
    print("Déconnexion imprimante simulée") 
    return True
