"""
Suite de tests unitaires exhaustive pour la classe Food.
Vérifie la robustesse de la logique métier, la conversion des données
et la gestion des seuils nutritionnels.
"""

import unittest
from food import Food

class TestFood(unittest.TestCase):
    """
    Tests de validation pour la classe Food.
    Couvre l'initialisation, les setters, et la logique conditionnelle.
    """

    def setUp(self):
        """Prépare un objet Food neuf avant chaque test."""
        self.food = Food()

    # --- TESTS D'INITIALISATION ---
    def test_initialization_defaults(self):
        """Vérifie que les valeurs par défaut sont sécurisées."""
        self.assertIsNone(self.food.name)
        self.assertEqual(self.food.calories, 0.0)
        self.assertEqual(self.food.fat, 0.0)

    # --- TESTS DES SETTERS (CONVERSION ET SÉCURITÉ) ---
    def test_setters_conversion(self):
        """Vérifie que les chaînes et les None sont bien convertis en float."""
        # Test avec une chaîne (cas typique du scraping)
        self.food.calories = "120.5"
        self.assertEqual(self.food.calories, 120.5)

        # Test avec une virgule française
        # Note : Si ton code gère le replace(',', '.') dans le setter
        self.food.proteins = "10,5"
        self.assertEqual(self.food.proteins, 10.5)

        # Test avec None ou vide
        self.food.carbs = ""
        self.assertEqual(self.food.carbs, 0.0)
        self.food.fat = None
        self.assertEqual(self.food.fat, 0.0)

    # --- TESTS DE LA LOGIQUE MÉTIER (is_fat) ---
    def test_is_fat_logic(self):
        """Teste le seuil de 20g sous toutes ses coutures."""
        # Cas : Clairement gras
        self.food.fat = 25.0
        self.assertTrue(self.food.is_fat())

        # Cas : Clairement pas gras
        self.food.fat = 5.0
        self.assertFalse(self.food.is_fat())

        # Cas limite (Edge case) : Exactement 20.0
        # Selon la règle > 20, 20.0 doit être False
        self.food.fat = 20.0
        self.assertFalse(self.food.is_fat())

        # Cas limite : 20.1
        self.food.fat = 20.1
        self.assertTrue(self.food.is_fat())

    # --- TEST DU FORMATAGE DE NOM ---
    def test_name_assignment(self):
        """Vérifie que le nom est stocké correctement."""
        test_name = "Beurre de Cacahuètes"
        self.food.name = test_name
        self.assertEqual(self.food.name, test_name)

    # --- TEST DE ROBUSTESSE (VALEURS NÉGATIVES) ---
    def test_negative_values(self):
        """Vérifie que le système gère (ou bloque) les valeurs absurdes."""
        self.food.calories = -100.0
        # Ici on vérifie simplement que le code ne plante pas, 
        # même si la valeur est biologiquement impossible.
        self.assertEqual(self.food.calories, -100.0)

if __name__ == '__main__':
    unittest.main()