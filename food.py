"""
Module de gestion des données nutritionnelles.

Ce module définit la classe Food permettant de récupérer, traiter et
sauvegarder les informations nutritionnelles d'un aliment via scraping.
Il gère automatiquement la conversion des formats numériques (virgules).
"""

import re
import csv
from typing import Optional, Any
import requests
from bs4 import BeautifulSoup

# Constante globale
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

    def _clean_float(self, value: Any) -> float:
        """Nettoie et convertit une valeur en float (gère les virgules)."""
        if value is None or value == "":
            return 0.0
        try:
            # Conversion en string pour remplacer la virgule par un point
            clean_val = str(value).replace(',', '.')
            return float(clean_val)
        except ValueError:
            return 0.0

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
    def calories(self, value: Any) -> None:
        """Définit les calories avec nettoyage du format."""
        self._calories = self._clean_float(value)

    @property
    def proteins(self) -> float:
        """Retourne le taux de protéines."""
        return self._proteins

    @proteins.setter
    def proteins(self, value: Any) -> None:
        """Définit les protéines avec nettoyage du format."""
        self._proteins = self._clean_float(value)

    @property
    def carbs(self) -> float:
        """Retourne le taux de glucides."""
        return self._carbs

    @carbs.setter
    def carbs(self, value: Any) -> None:
        """Définit les glucides avec nettoyage du format."""
        self._carbs = self._clean_float(value)

    @property
    def fat(self) -> float:
        """Retourne le taux de lipides."""
        return self._fat

    @fat.setter
    def fat(self, value: Any) -> None:
        """Définit les lipides avec nettoyage du format."""
        self._fat = self._clean_float(value)

    def is_fat(self) -> bool:
        """
        Vérifie si l'aliment est riche en graisses (> 20g).
        """
        return self._fat > 20.0

    def retrieve_food_infos(self, food_name: str) -> None:
        """
        Extrait les données nutritionnelles depuis le site web.
        """
        formatted_name = food_name.lower().replace(" ", "-")
        url = f"{BASE_URL}{formatted_name}.php"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        self.name = food_name
        page_text = soup.get_text(separator=' ', strip=True)

        # Extraction via Regex
        cal_match = re.search(r"Calories\s*[:]\s*(\d+[\.,]?\d*)", page_text, re.IGNORECASE)
        if cal_match:
            self.calories = cal_match.group(1)

        def _extract(label: str) -> str:
            pattern = rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}"
            match = re.search(pattern, page_text, re.IGNORECASE)
            return match.group(1) if match else "0.0"

        self.proteins = _extract("protéines")
        self.carbs = _extract("glucides")
        self.fat = _extract("lipides")

    def display_food_infos(self) -> None:
        """Affiche les résultats formatés dans la console."""
        sep = "-" * 65
        print(sep)
        print(f"{'NOM':<18} {'CALORIES':<12} {'PROTÉINES':<12} {'GLUCIDES':<12} {'LIPIDES'}")
        print(f"{self._name if self._name else 'N/A':<18} {self._calories:<12.1f} "
              f"{self._proteins:<12.1f} {self._carbs:<12.1f} {self._fat:<10.1f}")
        print(sep)

    def save_to_csv_file(self, file_name: str) -> None:
        """Sauvegarde les données dans un fichier CSV."""
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([self._name, self._calories, self._proteins, self._carbs, self._fat])