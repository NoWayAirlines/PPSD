import requests
from bs4 import BeautifulSoup
import re
import csv

BASE_URL = "https://www.infocalories.fr/calories/calories-"

class Food:
    def __init__(self):
        self.__name = None
        self.__calories = None
        self.__proteins = None
        self.__carbs = None
        self.__fat = None

    def set_name(self, name): self.__name = name
    def set_calories(self, val): self.__calories = float(val) if val else 0.0
    def set_proteins(self, val): self.__proteins = float(val) if val else 0.0
    def set_carbs(self, val): self.__carbs = float(val) if val else 0.0
    def set_fat(self, val): self.__fat = float(val) if val else 0.0

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

        # Extraction Calories (Après)
        m_cal = re.search(r"Calories\s*[:]\s*(\d+[\.,]?\d*)", text, re.IGNORECASE)
        self.set_calories(m_cal.group(1).replace(',', '.') if m_cal else 0.0)

        # Extraction Nutriments (Avant)
        def ex(label):
            motif = rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}"
            match = re.search(motif, text, re.IGNORECASE)
            return match.group(1).replace(',', '.') if match else 0.0

        self.set_proteins(ex("protéines"))
        self.set_carbs(ex("glucides"))
        self.set_fat(ex("lipides"))

    def display_food_infos(self):
        line = "-" * 65
        header = f"{'NOM':<18} {'CALORIES':<12} {'PROTÉINES':<12} {'GLUCIDES':<12} {'LIPIDES'}"
        data = f"{self.__name:<18} {self.__calories:<12.1f} {self.__proteins:<12.1f} {self.__carbs:<12.1f} {self.__fat:<10.1f}"
        print(f"{line}\n{header}\n{data}\n{line}")

    def save_to_csv_file(self, file_name):
        with open(file_name, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.__name, self.__calories, self.__proteins, self.__carbs, self.__fat])