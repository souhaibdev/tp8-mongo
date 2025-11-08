from pymongo import MongoClient
from datetime import datetime
client = MongoClient("mongodb://localhost:27017")
# I
db = client["e-commerceDB"]
produits=db["produits"]
clients=db["clients"]
commandes=db["commandes"]

# 1
def creer_commande():
    client_c = input("entrer le nom de client :")
    cliente = clients.find_one({"Nom":client_c})
    if not cliente:
        print("had client ra makayennch!")
        return  
    
    produit_list =[]
    montant = 0

    while True:
        produits_c = input("entrer le nom de produit :")
        
        p = produits.find_one({"Nom":produits_c})
        if not p:
            print("had produit ra makayennch!")
            continue
        
        quantite = int(input("entrer le quantite :"))
        if p["Stock"]< quantite:
            print("had quantite maeandnach!!")
            continue

        produits.update_one(
            {"Nom": p["Nom"]},
            {"$inc": {"Stock": -quantite}}
        )

        montant += p["prix"]*quantite

        produit_list.append({"produits":p["Nom"],"quantite":quantite})
        
        autre = input("bghiti tzid produit akhor? (ah/la) : ")
        if autre != "ah":
            break
    commandes.insert_one({"client":client_c,
                          "produits":produit_list,
                          "date_commande":datetime.now(),
                          "statut":"en cours",
                          "montant":montant})
    
    print("sf omor dazet bikher ")

# 2
def afficher_produits():
   for produit in produits.find():print(produit)

# 3
def recherche_commandeClient():
    nom_client = input("entrer le nom de client :").strip()
    for commande in commandes.find({"Client":nom_client}):print(commande) 

# 4
def recherche_commandeLivre():
    for commande in commandes.find({"Statut":"livrée"}):print(commande)

# 5
def modifier_produit():
    nom = input("entrer le nom de produits :")
    p = produits.find_one({"Nom":nom})
    if not p:
        print("had produit ra makayennch!")
        return

    categorie = input("nouveau categorie :")
    prix = float(input("nouveau prix :"))
    stock = int(input("nouveau stock :"))
    produits.update_one({"Nom":nom},{"$set":{"Catégorie":categorie,"Prix":prix,"Stock":stock}})

# 6
def ajouter_champ():
    produits.update_many({},{"$set":{"disponible":True}})

# 7
def supprimer_commande():
    nom_produits = input("entrer le nom de produits :")
    nom_client = input("entrer le nom de client :")
    p = produits.find_one({"Nom":nom_produits})
    if not p:
        print("had produit ra makayennch!")
        return
    c=clients.find_one({"Nom":nom_client})
    if not c:
        print("had client ra makayennch!")
        return
    
    commandes.delete_one({"Produits":nom_produits,"Client":nom_client})
    print("ra safi tmesah !")

# 8
def supprimer_commandeClient():
    nom_client = input("entrer le nom de client :")
    c=clients.find_one({"Nom":nom_client})
    if not c:
        print("had client ra makayennch!")
        return
    
    commandes.delete_many({"Client":nom_client})
    print("ra safi tmesah !")

# 9
def trier_commandesPardate():
    for commande in commandes.find().sort({"Date_commande",-1}):print(commande)

# 10
def afficher_produitsDisponible():
    for produit in produits.find({"disponible":True}):print(produit)   

# 11
def menu():
    while True:
        print(
            "+-----------+---------------------------------------+ \n"
            "|num |                     menu                     |\n"
            "+-----------+---------------------------------------+\n"
            "| 1  | Ajouter une commande                         |\n"
            "| 2  | Afficher tous les produits                   |\n"
            "| 3  | Afficher tous les produits disponibles 0     |\n"
            "| 4  | Rechercher une commande par client           |\n"
            "| 5  | Mettre à jour un produit                     |\n"
            "| 6  | supprimer une commande                       |\n"
            "| 7  | Supprimer les commandes d'un client donné    |\n"
            "| 8  | Afficher les produits disponibles            |\n"
            "| 9  | Trier les commandes par date de la commande  |\n"
            "| 10 | Quitter                                      |\n"
            "+-----------+---------------------------------------+\n")
        
        choix = int(input("khta mn 1 n 10 :"))
        if choix == 1:
            creer_commande()
        elif choix == 2:
            afficher_produits()
        elif choix == 3:
            recherche_commandeLivre()
        elif choix == 4:
            recherche_commandeClient()
        elif choix == 5:
            modifier_produit()
        elif choix == 6:
            supprimer_commande()
        elif choix == 7:
            supprimer_commandeClient()
        elif choix == 8:
            afficher_produitsDisponible()
        elif choix == 9:
            trier_commandesPardate()
        elif choix == 10:
            break
        else:
            print("raqem ralat (khta mn 1 n 10)")

menu()
        


 