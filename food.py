"""
Module de gestion des données nutritionnelles.

Ce module définit la classe Food permettant de récupérer, traiter et
sauvegarder les informations nutritionnelles d'un aliment via scraping.
"""

import re
import csv
import pylint
from typing import Optional
import requests
from bs4 import BeautifulSoup

# Constante globale en majuscules (PEP 8)
BASE_URL = "https://www.infocalories.fr/calories/calories-"


class Food:
    """
    Représente un produit alimentaire et ses valeurs nutritionnelles.
    """

    def __init__(self) -> None:
        """Initialise les attributs de l'aliment à des valeurs par défaut."""
        self._name: Optional[str] = None
        self._calories: float = 0.0
        self._proteins: float = 0.0
        self._carbs: float = 0.0
        self._fat: float = 0.0

    @property
    def name(self) -> Optional[str]:
        """Retourne le nom de l'aliment."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Définit le nom de l'aliment."""
        self._name = value

    @property
    def calories(self) -> float:
        """Retourne la valeur énergétique."""
        return self._calories

    @calories.setter
    def calories(self, value: float) -> None:
        """Définit les calories (convertit en float si nécessaire)."""
        self._calories = float(value) if value else 0.0

    @property
    def proteins(self) -> float:
        """Retourne le taux de protéines."""
        return self._proteins

    @proteins.setter
    def proteins(self, value: float) -> None:
        """Définit les protéines."""
        self._proteins = float(value) if value else 0.0

    @property
    def carbs(self) -> float:
        """Retourne le taux de glucides."""
        return self._carbs

    @carbs.setter
    def carbs(self, value: float) -> None:
        """Définit les glucides."""
        self._carbs = float(value) if value else 0.0

    @property
    def fat(self) -> float:
        """Retourne le taux de lipides."""
        return self._fat

    @fat.setter
    def fat(self, value: float) -> None:
        """Définit les lipides."""
        self._fat = float(value) if value else 0.0

    def is_fat(self) -> bool:
        """
        Vérifie si l'aliment est riche en graisses.

        Returns:
            bool: True si les lipides dépassent 20g, False sinon.
        """
        return self._fat > 20.0

    def retrieve_food_infos(self, food_name: str) -> None:
        """
        Extrait les données nutritionnelles depuis le site web.

        Args:
            food_name: Le nom de l'aliment à rechercher.

        Raises:
            requests.exceptions.RequestException: En cas d'erreur réseau.
        """
        formatted_name = food_name.lower().replace(" ", "-")
        url = f"{BASE_URL}{formatted_name}.php"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        self.name = food_name
        page_text = soup.get_text(separator=' ', strip=True)

        # Extraction des Calories
        calories_match = re.search(
            r"Calories\s*[:]\s*(\d+[\.,]?\d*)", page_text, re.IGNORECASE
        )
        if calories_match:
            self.calories = float(calories_match.group(1).replace(',', '.'))

        # Fonction interne pour les nutriments
        def _extract_val(label: str) -> float:
            pattern = rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}"
            match = re.search(pattern, page_text, re.IGNORECASE)
            return float(match.group(1).replace(',', '.')) if match else 0.0

        self.proteins = _extract_val("protéines")
        self.carbs = _extract_val("glucides")
        self.fat = _extract_val("lipides")

    def display_food_infos(self) -> None:
        """Affiche les résultats formatés dans la console."""
        separator = "-" * 65
        header = (f"{'NOM':<18} {'CALORIES':<12} {'PROTÉINES':<12} "
                  f"{'GLUCIDES':<12} {'LIPIDES'}")
        data = (f"{self._name if self._name else 'N/A':<18} "
                f"{self._calories:<12.1f} {self._proteins:<12.1f} "
                f"{self._carbs:<12.1f} {self._fat:<10.1f}")

        print(separator)
        print(header)
        print(data)
        print(separator)

    def save_to_csv_file(self, file_name: str) -> None:
        """
        Sauvegarde les données dans un fichier CSV.

        Args:
            file_name: Nom du fichier de destination.
        """
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                self._name, self._calories, self._proteins,
                self._carbs, self._fat
            ])