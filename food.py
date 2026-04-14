import requests
from bs4 import BeautifulSoup
import re
import csv

BASE_URL = "https://www.infocalories.fr/calories/calories-"

class Food:
    def __init__(self):
        self.__name = None
        self.__calories = 0.0
        self.__proteins = 0.0
        self.__carbs = 0.0
        self.__fat = 0.0

    # --- Getters / Setters ---
    def get_name(self): return self.__name
    def set_name(self, name): self.__name = name

    def get_calories(self): return self.__calories
    def set_calories(self, val): self.__calories = float(val) if val else 0.0

    def get_proteins(self): return self.__proteins
    def set_proteins(self, val): self.__proteins = float(val) if val else 0.0

    def get_carbs(self): return self.__carbs
    def set_carbs(self, val): self.__carbs = float(val) if val else 0.0

    def get_fat(self): return self.__fat
    def set_fat(self, val): self.__fat = float(val) if val else 0.0

    # --- LA MÉTHODE MANQUANTE ---
    def is_fat(self):
        """ Retourne True si le taux de lipides est > 20g """
        return self.get_fat() > 20.0

    # --- Récupération des données ---
    def retrieve_food_infos(self, food_name):
        nom_url = food_name.lower().replace(" ", "-")
        url = f"{BASE_URL}{nom_url}.php"
        headers = {'User-Agent': 'Mozilla/5.0'}
        reponse = requests.get(url, headers=headers)

        if reponse.status_code != 200:
            raise Exception(f"Aliment '{food_name}' introuvable.")

        soup = BeautifulSoup(reponse.text, 'html.parser')
        self.set_name(food_name)
        text = soup.get_text(separator=' ', strip=True)

        # Calories (Après)
        m_cal = re.search(r"Calories\s*[:]\s*(\d+[\.,]?\d*)", text, re.IGNORECASE)
        if m_cal: self.set_calories(m_cal.group(1).replace(',', '.'))

        # Nutriments (Avant)
        def ex(label):
            motif = rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}"
            match = re.search(motif, text, re.IGNORECASE)
            return match.group(1).replace(',', '.') if match else 0.0

        self.set_proteins(ex("protéines"))
        self.set_carbs(ex("glucides"))
        self.set_fat(ex("lipides"))

    def display_food_infos(self):
        print(f"{self.get_name():<18} {self.get_calories():<10.1f} {self.get_proteins():<10.1f} {self.get_carbs():<10.1f} {self.get_fat():<10.1f}")

    def save_to_csv_file(self, file_name):
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([self.__name, self.__calories, self.__proteins, self.__carbs, self.__fat])