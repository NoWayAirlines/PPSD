import re
import csv
import unicodedata
import requests
from bs4 import BeautifulSoup
from typing import Optional, Any

BASE_URL = "https://www.infocalories.fr/calories/calories-"

class Food:
    def __init__(self) -> None:
        self._name: Optional[str] = None
        self._calories: float = 0.0
        self._proteins: float = 0.0
        self._carbs: float = 0.0
        self._fat: float = 0.0

    def _clean_float(self, value: Any) -> float:
        if not value: return 0.0
        try:
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError): return 0.0

    # --- PROPERTIES ---
    @property
    def name(self) -> Optional[str]: return self._name
    @name.setter
    def name(self, value: str): self._name = value

    @property
    def calories(self) -> float: return self._calories
    @calories.setter
    def calories(self, value: Any): self._calories = self._clean_float(value)

    @property
    def proteins(self) -> float: return self._proteins
    @proteins.setter
    def proteins(self, value: Any): self._proteins = self._clean_float(value)

    @property
    def carbs(self) -> float: return self._carbs
    @carbs.setter
    def carbs(self, value: Any): self._carbs = self._clean_float(value)

    @property
    def fat(self) -> float: return self._fat
    @fat.setter
    def fat(self, value: Any): self._fat = self._clean_float(value)

    # --- MOTEUR DE GÉNÉRATION D'URL (SLUGIFIER) ---

    def _generate_slugs(self, name: str) -> list:
        """
        Génère une liste de patterns possibles pour l'URL.
        Gère les pluriels, les articles et les caractères spéciaux.
        """
        def basic_clean(t):
            t = t.lower().strip()
            t = "".join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')
            t = t.replace("œ", "oe").replace("'", "-").replace(" ", "-")
            t = re.sub(r'[^a-z0-9-]', '', t)
            return re.sub(r'-+', '-', t).strip('-')

        slugs = []
        base = basic_clean(name)
        slugs.append(base) # 1. Test exact (ex: pommes-de-terre)

        # 2. Test variante Pluriel/Singulier sur le premier mot
        # (Très fréquent : pomme -> pommes)
        parts = base.split('-')
        if len(parts) > 0:
            # Si singulier, on tente le pluriel
            if not parts[0].endswith('s'):
                alt_parts = list(parts)
                alt_parts[0] += 's'
                slugs.append("-".join(alt_parts))
            # Si pluriel, on tente le singulier
            elif parts[0].endswith('s'):
                alt_parts = list(parts)
                alt_parts[0] = alt_parts[0][:-1]
                slugs.append("-".join(alt_parts))

        # 3. Suppression des articles au début (ex: le-riz -> riz)
        articles = ['le-', 'la-', 'les-', 'l-']
        for art in articles:
            if base.startswith(art):
                slugs.append(base.replace(art, '', 1))

        return list(dict.fromkeys(slugs)) # Supprime les doublons

    # --- LOGIQUE DE RÉCUPÉRATION ---

    def retrieve_food_infos(self, food_name: str) -> None:
        """Tente tous les patterns générés jusqu'à trouver une page 200."""
        possible_slugs = self._generate_slugs(food_name)
        headers = {'User-Agent': 'Mozilla/5.0'}
        success = False

        for slug in possible_slugs:
            url = f"{BASE_URL}{slug}.php"
            try:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    self._parse_page(response.text, food_name)
                    success = True
                    break # On a trouvé !
            except requests.RequestException:
                continue

        if not success:
            raise FileNotFoundError(f"Aucun pattern trouvé pour : {food_name}")

    def _parse_page(self, html: str, original_name: str) -> None:
        """Analyse le contenu HTML une fois la bonne page trouvée."""
        soup = BeautifulSoup(html, 'html.parser')
        self.name = original_name
        text = soup.get_text(separator=' ', strip=True)

        # Extraction robuste avec Regex
        cal = re.search(r"Calories\s*[:]\s*(\d+[\.,]?\d*)", text, re.IGNORECASE)
        self.calories = cal.group(1) if cal else 0

        def get_val(label):
            m = re.search(rf"(\d+[\.,]?\d*)\s*g\s*(?:de\s+)?{label}", text, re.IGNORECASE)
            return m.group(1) if m else "0"

        self.proteins = get_val("protéines")
        self.carbs = get_val("glucides")
        self.fat = get_val("lipides")

    def is_fat(self) -> bool:
        return self._fat > 20.0