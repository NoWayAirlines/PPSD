from food import Food
import argparse
import sys
import pylint
# On affiche un petit message de démarrage
print("--- Analyseur Nutritionnel ---")

# 1. Configuration de l'argparse
parser = argparse.ArgumentParser(description="Récupère les infos d'un aliment sur Infocalories")
# Le default est à None pour forcer l'utilisateur à saisir un aliment
parser.add_argument('-f', '--food', help="Nom de l'aliment (ex: 'riz cru')", default=None)

# 2. Extraction du nom de l'aliment
args = parser.parse_args()
target = args.food

# 3. Sécurité : si rien n'est saisi, on arrête le script proprement
if target is None:
    print("Erreur : Aucun aliment précisé.")
    print("Utilisation : python get_food.py -f \"nom de l'aliment\"")
    sys.exit(1)

# 4. Création de l'objet Food (le moteur)
my_food = Food()

try:
    # Récupération des données sur le site
    print(f"Connexion à Infocalories pour : {target}...")
    my_food.retrieve_food_infos(target)
    
    # Affichage du tableau de bord (ordre de l'image : Cal, Prot, Glu, Lip)
    my_food.display_food_infos()

    # Petit bonus : on utilise la méthode is_fat qu'on a testée tout à l'heure
    if my_food.is_fat():
        print("⚠️ Attention : Cet aliment est riche en lipides (> 20g) !")
    else:
        print("✅ Cet aliment est raisonnable en lipides.")

    # Sauvegarde automatique dans ton historique
    my_food.save_to_csv_file("historique_aliments.csv")
    print("\nDonnées sauvegardées dans 'historique_aliments.csv'")

except Exception as e:
    print(f"Désolé, une erreur est survenue : {e}")
    sys.exit(1)