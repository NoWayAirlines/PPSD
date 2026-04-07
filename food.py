import requests
from bs4 import BeautifulSoup
import re
import csv

# Global variable for the URL
BASE_URL = "https://www.infocalories.fr/calories/calories-"

class Food:
    """ class food """
    __name = None
    __calories = None
    __fat = None
    __carbs = None
    __proteins = None

    def get_name(self): 
        """ function : get the food name """
        return self.__name

    def set_name(self, name):
        """ function : set the food name """
        self.__name = name

    def get_calories(self):
        """ function : get the property named calories of the food """
        return self.__calories

    def set_calories(self, calories):
        """ function : set the property named calories of the food """
        self.__calories = float(calories)

    def get_fat(self):
        """ function : get the property named fat of the food """
        return self.__fat

    def set_fat(self, fat):
        """ function : set the property named fat of the food """
        self.__fat = float(fat)

    def get_carbs(self):
        """ function : get the property named carbs of the food """
        return self.__carbs

    def set_carbs(self, carbs):
        """ function : set the property named carbs of the food """
        self.__carbs = float(carbs)

    def get_proteins(self):
        """ function : get the property named proteins of the food """
        return self.__proteins

    def set_proteins(self, proteins):
        """ function : set the property named proteins of the food """
        self.__proteins = float(proteins)

    def retrieve_food_infos(self, food_name):
        """ function : scrap the properties of the food from a website given its name
        
        - think of making the URL a global variable
        - check whether the request succeed before trying to parse the payload
        - if not succesfull, raise an error
        
        """
        # Formater le nom pour l'URL (ex: "riz cru" -> "riz-cru")
        formatted_name = food_name.lower().replace(" ", "-")
        url = f"{BASE_URL}{formatted_name}.php"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        # check whether the request succeed
        if response.status_code != 200:
            # if not succesfull, raise an error
            raise ConnectionError(f"Erreur {response.status_code} : Impossible de trouver l'aliment '{food_name}'")

        soup = BeautifulSoup(response.text, 'html.parser')
        self.set_name(food_name)

        # Fonction interne pour extraire les chiffres du texte HTML
        def parse_value(label):
            element = soup.find(string=lambda t: label in t)
            if element:
                # Trouve le premier nombre (entier ou décimal) dans la chaîne
                match = re.search(r"(\d+\.?\d*)", element)
                return float(match.group(1)) if match else 0.0
            return 0.0

        self.set_calories(parse_value("Calories"))
        self.set_fat(parse_value("Lipides"))
        self.set_carbs(parse_value("Glucides"))
        self.set_proteins(parse_value("Protéines"))

    def display_food_infos(self):
        """ function : display the properties of the food 
        the outlook should be similar to this:
                ------------------------------------------------
                name        calories    fat     carbs   proteins
                tomate      21.0        0.3     4.6     0.8
                ------------------------------------------------
        """
        line = "-" * 48
        # Utilisation de f-strings avec espacement fixe pour aligner les colonnes
        header = f"{'name':<12} {'calories':<11} {'fat':<7} {'carbs':<8} {'proteins':<8}"
        
        # Valeurs par défaut à 0.0 si non définies
        n = self.__name if self.__name else "unknown"
        c = self.__calories if self.__calories is not None else 0.0
        f = self.__fat if self.__fat is not None else 0.0
        cb = self.__carbs if self.__carbs is not None else 0.0
        p = self.__proteins if self.__proteins is not None else 0.0

        data = f"{n:<12} {c:<11.1f} {f:<7.1f} {cb:<8.1f} {p:<8.1f}"

        print(line)
        print(header)
        print(data)
        print(line)

    def save_to_csv_file(self, file_name):
        """ function : save the properties of the food in a csv file 
        - use function with for file opening
        """
        # Utilisation de 'with' pour l'ouverture sécurisée
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Écrit les données (Name, Cal, Fat, Carbs, Prot)
            writer.writerow([self.__name, self.__calories, self.__fat, self.__carbs, self.__proteins])

    def is_fat(self):
        """ function : return true or false whether the food has more than 20% of fat 
        - define a fat threshold and write the function accordingly
        """
        FAT_THRESHOLD = 20.0
        if self.__fat is None:
            return False
        return self.__fat > FAT_THRESHOLD

# --- Test rapide ---
if __name__ == "__main__":
    item = Food()
    try:
        nom_recherche = "tomate" # Essaye avec "riz cru" ou "beurre" pour tester is_fat
        item.retrieve_food_infos(nom_recherche)
        item.display_food_infos()
        
        if item.is_fat():
            print(f"--> {nom_recherche} est considéré comme gras.")
            
        item.save_to_csv_file("journal_alimentaire.csv")
        print("Données sauvegardées dans le CSV.")
        
    except Exception as e:
        print(f"Erreur : {e}")