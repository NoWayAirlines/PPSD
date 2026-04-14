import requests
from bs4 import BeautifulSoup
import re
import csv

# Variable globale pour l'URL de base
BASE_URL = "https://www.infocalories.fr/calories/calories-"

class Aliment:
    """ class food """
    __nom = None
    __calories = None
    __proteines = None  # Classé en 2ème selon l'image
    __glucides = None   # Classé en 3ème selon l'image
    __lipides = None    # Classé en 4ème selon l'image

    # --- Accesseurs (Getters / Setters) ---
    def get_nom(self):
        return self.__nom
    def set_nom(self, nom):
        self.__nom = nom

    def get_calories(self):
        return self.__calories
    def set_calories(self, calories):
        self.__calories = float(calories) if calories else 0.0

    def get_proteines(self):
        return self.__proteines
    def set_proteines(self, proteines):
        self.__proteines = float(proteines) if proteines else 0.0

    def get_glucides(self):
        return self.__glucides
    def set_glucides(self, glucides):
        self.__glucides = float(glucides) if glucides else 0.0

    def get_lipides(self):
        return self.__lipides
    def set_lipides(self, lipides):
        self.__lipides = float(lipides) if lipides else 0.0

    # --- Méthodes de récupération ---

    def recuperer_infos_aliment(self, nom_aliment):
        """ function : scrap properties following the image order """
        nom_url = nom_aliment.lower().replace(" ", "-")
        url = f"{BASE_URL}{nom_url}.php"

        headers = {'User-Agent': 'Mozilla/5.0'}
        reponse = requests.get(url, headers=headers)

        if reponse.status_code != 200:
            raise Exception(f"Erreur {reponse.status_code} : Page introuvable.")

        soup = BeautifulSoup(reponse.text, 'html.parser')
        self.set_nom(nom_aliment)
        texte_page = soup.get_text(separator=' ', strip=True)

        # 1. CALORIES (Format : Calories : 588)
        # On cherche le mot puis le chiffre
        match_cal = re.search(r"Calories\s*[:]\s*(\d+[\.,]?\d*)", texte_page, re.IGNORECASE)
        self.set_calories(match_cal.group(1).replace(',', '.') if match_cal else 0.0)

        # Fonction pour les nutriments (Format : 25g de protéines)
        # On cherche le chiffre situé AVANT le nom
        def extraire_avant(label):
            motif = rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}"
            match = re.search(motif, texte_page, re.IGNORECASE)
            if match:
                return match.group(1).replace(',', '.')
            return 0.0

        # 2. PROTÉINES
        self.set_proteines(extraire_avant("protéines"))

        # 3. GLUCIDES
        self.set_glucides(extraire_avant("glucides"))

        # 4. LIPIDES
        self.set_lipides(extraire_avant("lipides"))

    def afficher_infos_aliment(self):
        """ function : display properties in the image order """
        barre = "-" * 65
        # L'entête suit maintenant l'ordre visuel
        entete = f"{'NOM':<18} {'CALORIES':<12} {'PROTÉINES':<12} {'GLUCIDES':<12} {'LIPIDES'}"

        n = self.__nom if self.__nom else "Inconnu"
        # On aligne les valeurs sur l'entête
        donnees = f"{n:<18} {self.__calories:<12.1f} {self.__proteines:<12.1f} {self.__glucides:<12.1f} {self.__lipides:<10.1f}"

        print(barre)
        print(entete)
        print(donnees)
        print(barre)

    def sauvegarder_dans_csv(self, nom_fichier):
        """ function : save to csv file in the right order """
        with open(nom_fichier, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Sauvegarde dans l'ordre : Nom, Cal, Prot, Glu, Lip
            writer.writerow([self.__nom, self.__calories, self.__proteines, self.__glucides, self.__lipides])

# --- Test Multi-Aliments avec le bon ordre ---
if __name__ == "__main__":
    mon_aliment = Aliment()
    tests = ["beurre cacahuetes", "tomate", "riz cru","oeuf au plat","mousse chocolat",'nougat glace']

    for nom in tests:
        try:
            mon_aliment.recuperer_infos_aliment(nom)
            mon_aliment.afficher_infos_aliment()
        except Exception as e:
            print(f"Erreur sur {nom} : {e}")