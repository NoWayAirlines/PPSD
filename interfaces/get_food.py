"""
Script de commande pour récupérer les informations nutritionnelles.

Ce script utilise la classe Food pour extraire des données depuis Infocalories
via des arguments en ligne de commande.
"""

import argparse
import sys
from food import Food


def main() -> None:
    """
    Fonction principale gérant les arguments et l'exécution du programme.
    """
    # Configuration de l'analyseur d'arguments
    parser = argparse.ArgumentParser(
        description="Récupère les informations nutritionnelles d'un aliment."
    )
    parser.add_argument(
        '-f', '--food',
        help="Nom de l'aliment à rechercher (ex: 'riz cru')",
        default=None
    )

    args = parser.parse_args()
    food_name = args.food

    # Vérification de la présence d'un argument
    if food_name is None:
        print("Erreur : Aucun aliment précisé. Utilisez -f.")
        sys.exit(1)

    print(f"--- Analyse en cours pour : {food_name} ---")

    # Utilisation du moteur Food
    my_food = Food()

    try:
        # Récupération et affichage
        my_food.retrieve_food_infos(food_name)
        my_food.display_food_infos()

        # Utilisation de la logique métier (is_fat)
        if my_food.is_fat():
            print("⚠️ Cet aliment est riche en lipides (> 20g).")
        else:
            print("✅ Taux de lipides raisonnable.")

        # Sauvegarde
        output_file = "historique_aliments.csv"
        my_food.save_to_csv_file(output_file)
        print(f"Résultats ajoutés à {output_file}")

    except Exception as error:  # pylint: disable=broad-except
        print(f"Une erreur est survenue lors de l'analyse : {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()