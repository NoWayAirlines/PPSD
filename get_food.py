from food import Food
import argparse
import sys

print("Running script...")

parser = argparse.ArgumentParser(description="Food Informations")
# Le default est maintenant à None (rien)
parser.add_argument('-f', '--food', help="votre aliment", default=None)

args = parser.parse_args()
food_name = args.food

# Sécurité : Si l'utilisateur n'a rien mis après -f ou n'a pas utilisé l'argument
if food_name is None:
    print("Erreur : Vous devez préciser un aliment avec l'argument -f.")
    print("Exemple : python get_food.py -f \"riz cru\"")
    sys.exit(1)

my_food = Food()

try:
    print(f"Recherche pour : {food_name}")
    my_food.retrieve_food_infos(food_name)
    my_food.display_food_infos()
    my_food.save_to_csv_file("food_data.csv")
    print("Données enregistrées.")

except Exception as e:
    print(f"Erreur : {e}")
    sys.exit(1)