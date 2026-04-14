"""
Module de gestion des données nutritionnelles NutriScan.
Ce module gère le scraping, la normalisation des noms et le traitement des données.
"""

import re
import csv
import unicodedata
from typing import Optional, Any, List
import requests
from bs4 import BeautifulSoup

# Constantes en majuscules pour Pylint
BASE_URL = "https://www.infocalories.fr/calories/calories-"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}


class Food:
    """
    Représente un produit alimentaire et ses capacités de récupération de données.
    """

    def __init__(self) -> None:
        """Initialise un objet Food avec des valeurs par défaut."""
        self._name: Optional[str] = None
        self._calories: float = 0.0
        self._proteins: float = 0.0
        self._carbs: float = 0.0
        self._fat: float = 0.0

    def _clean_float(self, value: Any) -> float:
        """Convertit une valeur brute en float sécurisé (gère les virgules)."""
        if not value:
            return 0.0
        try:
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError):
            return 0.0

    @property
    def name(self) -> Optional[str]:
        """Retourne le nom de l'aliment."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def calories(self) -> float:
        """Retourne la valeur calorique."""
        return self._calories

    @calories.setter
    def calories(self, value: Any) -> None:
        self._calories = self._clean_float(value)

    @property
    def proteins(self) -> float:
        """Retourne le taux de protéines."""
        return self._proteins

    @proteins.setter
    def proteins(self, value: Any) -> None:
        self._proteins = self._clean_float(value)

    @property
    def carbs(self) -> float:
        """Retourne le taux de glucides."""
        return self._carbs

    @carbs.setter
    def carbs(self, value: Any) -> None:
        self._carbs = self._clean_float(value)

    @property
    def fat(self) -> float:
        """Retourne le taux de lipides."""
        return self._fat

    @fat.setter
    def fat(self, value: Any) -> None:
        self._fat = self._clean_float(value)

    def _generate_slugs(self, name: str) -> List[str]:
        """Génère des variantes d'URL pour contourner les pluriels et articles."""
        def basic_clean(text: str) -> str:
            text = text.lower().strip()
            # Supprimer les accents
            text = "".join(c for c in unicodedata.normalize('NFD', text)
                           if unicodedata.category(c) != 'Mn')
            text = text.replace("œ", "oe").replace("'", "-").replace(" ", "-")
            text = re.sub(r'[^a-z0-9-]', '', text)
            return re.sub(r'-+', '-', text).strip('-')

        slugs = []
        base = basic_clean(name)
        slugs.append(base)

        parts = base.split('-')
        if parts:
            # Test pluriel automatique sur le premier mot
            alt_parts = list(parts)
            if not parts[0].endswith('s'):
                alt_parts[0] += 's'
                slugs.append("-".join(alt_parts))
            elif parts[0].endswith('s'):
                alt_parts[0] = alt_parts[0][:-1]
                slugs.append("-".join(alt_parts))

        return list(dict.fromkeys(slugs))

    def retrieve_food_infos(self, food_name: str) -> None:
        """Tente de récupérer les infos via plusieurs patterns d'URL."""
        possible_slugs = self._generate_slugs(food_name)
        success = False

        for slug in possible_slugs:
            url = f"{BASE_URL}{slug}.php"
            try:
                response = requests.get(url, headers=HEADERS, timeout=5)
                if response.status_code == 200:
                    self._parse_page(response.text, food_name)
                    success = True
                    break
            except requests.RequestException:
                continue

        if not success:
            raise FileNotFoundError(f"Aliment non trouvé sur le web : {food_name}")

    def _parse_page(self, html: str, original_name: str) -> None:
        """Extrait les données nutritionnelles du HTML brut."""
        soup = BeautifulSoup(html, 'html.parser')
        self.name = original_name
        text = soup.get_text(separator=' ', strip=True)

        cal_search = re.search(r"Calories\s*[:]\s*(\d+[\.,]?\d*)", text, re.IGNORECASE)
        self.calories = cal_search.group(1) if cal_search else 0

        def extract(label: str) -> str:
            pattern = rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}"
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1) if match else "0"

        self.proteins = extract("protéines")
        self.carbs = extract("glucides")
        self.fat = extract("lipides")

    def is_fat(self) -> bool:
        """Détermine si l'aliment est riche en graisses."""
        return self._fat > 20.0

    def save_to_csv(self, filename: str) -> None:
        """Sauvegarde les données dans un fichier CSV."""
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([self.name, self.calories, self.proteins, self.carbs, self.fat])