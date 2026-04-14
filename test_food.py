"""
Module de tests unitaires pour la classe Food.

Vérifie l'intégrité des données, la gestion des noms et la logique
de détection du taux de graisses.
"""

import unittest
from food import Food


class TestFood(unittest.TestCase):
    """
    Suite de tests pour valider le comportement de l'objet Food.
    """

    def test_name_management(self) -> None:
        """
        Vérifie que le nom est correctement initialisé puis modifié.
        """
        food_empty = Food()
        food_named = Food()

        food_named.name = 'coconut'

        # Vérifications via les propriétés
        self.assertIsNone(food_empty.name)
        self.assertEqual(food_named.name, 'coconut')

    def test_fat_content_logic(self) -> None:
        """
        Vérifie la logique de la méthode is_fat sur différents paliers.
        """
        # Cas 1 : Aliment riche en lipides
        food_high_fat = Food()
        food_high_fat.fat = 50.0
        self.assertTrue(food_high_fat.is_fat())

        # Cas 2 : Aliment faible en lipides
        food_low_fat = Food()
        food_low_fat.fat = 0.5
        self.assertFalse(food_low_fat.is_fat())

        # Cas 3 : Valeur charnière (20.0 ne doit pas être considéré comme gras)
        food_borderline = Food()
        food_borderline.fat = 20.0
        self.assertFalse(food_borderline.is_fat())

    def test_numeric_initialization(self) -> None:
        """
        Vérifie que les valeurs numériques sont bien à 0.0 par défaut.
        """
        new_food = Food()
        self.assertEqual(new_food.calories, 0.0)
        self.assertEqual(new_food.proteins, 0.0)


if __name__ == "__main__":
    unittest.main()