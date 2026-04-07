import requests
from bs4 import BeautifulSoup
import re
import csv

# Variable globale pour l'URL de base
BASE_URL = "https://www.infocalories.fr/"

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
        self.__calories = float(calories) if calories is not None else 0.0

    def get_fat(self):
        """ function : get the property named fat of the food """
        return self.__fat

    def set_fat(self, fat):
        """ function : set the property named fat of the food """
        self.__fat = float(fat) if fat is not None else 0.0

    def get_carbs(self):
        """ function : get the property named carbs of the food """
        return self.__carbs

    def set_carbs(self, carbs):
        """ function : set the property named carbs of the food """
        self.__carbs = float(carbs) if carbs is not None else 0.0

    def get_proteins(self):
        """ function : get the property named proteins of the food """
        return self.__proteins

    def set_proteins(self, proteins):
        """ function : set the property named proteins of the food """
        self.__proteins = float(proteins) if proteins is not None else 0.0

    def retrieve_food_infos(self, food_name):
        """ function : scrap the properties of the food from a website given its name
        
        - think of making the URL a global variable
        - check whether the request succeed before trying to parse the payload
        - if not succesfull, raise an error
        
        """
        # Formatage du nom pour l'URL (minuscules et tirets)
        # Exemple: "Beurre Cacahuetes" -> "beurre-cacahuetes"
        formatted_name = food_name.lower().replace(" ", "-")
        url = f"{BASE_URL}calories/calories-{formatted_name}.php"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        # check whether the request succeed before trying to parse the payload
        if response.status_code != 200:
            # if not succesfull, raise an error
            raise Exception(f"Erreur {response.status_code} : Impossible de trouver l'aliment '{food_name}' à l'adresse {url}")

        soup = BeautifulSoup(response.text, 'html.parser')
        self.set_name(food_name)

        # Fonction pour extraire les valeurs numériques (gère les virgules et les points)
        def extract_value(label):
            # On cherche le texte contenant le label (ex: "Lipides")
            element = soup.find(string=lambda t: label in t if t else False)
            if element:
                # On capture le nombre qui suit (ex: "50,2" ou "50.2")
                match = re.search(r"(\d+[\.,]?\d*)", element)
                if match:
                    return match.group(1).replace(',', '.')
            return 0.0

        # Mise à jour des propriétés avec les données du site
        self.set_calories(extract_value("Calories"))
        self.set_fat(extract_value("Lipides"))
        self.set_carbs(extract_value("Glucides"))
        self.set_proteins(extract_value("Protéines"))

    def display_food_infos(self):
        """ function : display the properties of the food 
        the outlook should be similar to this:
                ------------------------------------------------
                name        calories    fat     carbs   proteins
                tomate      21.0        0.3     4.6     0.8
                ------------------------------------------------
        """
        line = "-" * 55
        header = f"{'name':<15} {'calories':<12} {'fat':<8} {'carbs':<8} {'proteins':<8}"
        
        # Récupération des valeurs (ou 0.0 par défaut)
        n = self.__name if self.__name else "N/A"
        c = self.__calories if self.__calories is not None else 0.0
        f = self.__fat if self.__fat is not None else 0.0
        cb = self.__carbs if self.__carbs is not None else 0.0
        p = self.__proteins if self.__proteins is not None else 0.0
        
        data_row = f"{n:<15} {c:<12.1f} {f:<8.1f} {cb:<8.1f} {p:<8.1f}"
        
        print(line)
        print(header)
        print(data_row)
        print(line)

    def save_to_csv_file(self, file_name):
        """ function : save the properties of the food in a csv file 
        - use function with for file opening
        """
        # "with" assure la fermeture automatique du fichier
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([self.__name, self.__calories, self.__fat, self.__carbs, self.__proteins])

    def is_fat(self):
        """ function : return true or false whether the food has more than 20% of fat 
        - define a fat threshold and write the function accordingly
        """
        # Définition du seuil (20g de lipides pour 100g)
        FAT_THRESHOLD = 20.0
        if self.__fat is None:
            return False
        return self.__fat > FAT_THRESHOLD

# Exemple de test
if __name__ == "__main__":
    beurre = Food()
    try:
        # En tapant "beurre cacahuetes", le script va sur l'URL que tu as donnée
        beurre.retrieve_food_infos("beurre cacahuetes")
        beurre.display_food_infos()
        
        if beurre.is_fat():
            print("Résultat : Cet aliment est riche en graisses.")
            
    except Exception as e:
        print(f"Erreur : {e}")