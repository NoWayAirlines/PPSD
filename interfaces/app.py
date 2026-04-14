"""
Module Flask pour l'interface web de NutriScan.
Gère les requêtes utilisateur, l'autocomplétion et la logique de recherche.
"""

import os
import sys
import difflib
from flask import Flask, render_template, request

# --- CONFIGURATION DES CHEMINS ---
# On récupère le dossier racine pour importer le moteur food.py
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# pylint: disable=import-error, wrong-import-position
from food import Food

# --- INITIALISATION ---
app = Flask(__name__, template_folder='../templates')

# Liste constante (UPPER_CASE pour Pylint)
ALIMENTS_DISPONIBLES = sorted([
    "Abricot", "Agneau", "Aiglefin", "Ail", "Airelle", "Amande", "Ananas", "Anchois",
    "Anguille", "Artichaut", "Asperge", "Aubergine", "Autruche", "Avocat", "Bacon",
    "Baguette", "Banane", "Bar", "Basilic", "Betterave", "Beurre", "Bière", "Bifteck",
    "Biscotte", "Biscuit", "Blé", "Boudin", "Bouillon", "Boulgour", "Brie", "Brioche",
    "Brochet", "Brocoli", "Brugnon", "Cabillaud", "Cacahuète", "Cacao", "Café", "Caille",
    "Calamar", "Camembert", "Canard", "Canneberge", "Cannelle", "Cantal", "Capre",
    "Cardon", "Carotte", "Carpe", "Carrelet", "Cassis", "Céleri", "Cerise", "Cervelle",
    "Champignon", "Chapon", "Châtaigne", "Cheval", "Chevreuil", "Chipolata",
    "Chocolat blanc", "Chocolat au lait", "Chocolat noir", "Chorizo", "Chou",
    "Chou-fleur", "Chou de Bruxelles", "Cidre", "Citron", "Citrouille", "Clémentine",
    "Cochon", "Coco", "Coing", "Colin", "Comté", "Concombre", "Confiture", "Coq",
    "Coquille Saint-Jacques", "Cornichon", "Courge", "Courgette", "Couscous", "Crabe",
    "Crème fraîche", "Crevette", "Croissant", "Cuisse de grenouille", "Curcuma",
    "Curry", "Datte", "Daurade", "Dinde", "Échalote", "Églefin", "Emmental", "Épeautre",
    "Épinard", "Escargot", "Espadon", "Estragon", "Faisan", "Farine", "Fenouil", "Fève",
    "Figue", "Flageolet", "Flétan", "Foie", "Foie gras", "Fraise", "Framboise",
    "Fromage blanc", "Fromage de chèvre", "Fruit de la passion", "Fruits de mer",
    "Galette", "Gambas", "Gâteau", "Gaufre", "Gelée royale", "Genièvre", "Germe de blé",
    "Gibier", "Gigot", "Gingembre", "Girofle", "Glace", "Gombo", "Gorgonzola", "Gouda",
    "Goyave", "Graines de courge", "Graines de sésame", "Graines de tournesol",
    "Graisse de canard", "Grenade", "Griotte", "Grison", "Groseille", "Gruyère",
    "Guacamole", "Guimauve", "Haddock", "Halva", "Hareng", "Haricot blanc",
    "Haricot rouge", "Haricot vert", "Homard", "Huile de colza", "Huile de maïs",
    "Huile d'olive", "Huile de tournesol", "Huître", "Jambon cru", "Jambon cuit",
    "Jarret de porc", "Jaune d'œuf", "Jus d'orange", "Jus de pomme", "Kaki", "Ketchup",
    "Kiwi", "Lait de coco", "Lait de soja", "Lait de vache", "Laitue", "Langouste",
    "Langoustine", "Lapin", "Lard", "Lardon", "Lentilles", "Lièvre", "Lieu", "Limande",
    "Lotte", "Loup", "Macaroni", "Mâche", "Maquereau", "Margarine", "Marron",
    "Mascarpone", "Mayonnaise", "Melon", "Menthe", "Merguez", "Merlan", "Miel",
    "Millet", "Mirabelle", "Miso", "Morue", "Moules", "Moutarde", "Mozzarella",
    "Muesli", "Mûre", "Myrtille", "Navet", "Nectarine", "Noisette", "Noix",
    "Noix de cajou", "Noix de coco", "Noix de pécan", "Nouilles", "Œuf", "Oie",
    "Oignon", "Olive", "Omelette", "Orange", "Orge", "Origan", "Pain", "Pain de mie",
    "Pamplemousse", "Papaye", "Paprika", "Parmesan", "Pastèque", "Patate douce",
    "Pâtes", "Pêche", "Persil", "Petit pois", "Pignon de pin", "Piment", "Pistache",
    "Pizza", "Poire", "Poireau", "Pois chiche", "Poisson", "Poivron", "Pomme",
    "Pomme de terre", "Porc", "Potiron", "Poulet", "Poulpe", "Prune", "Pruneau",
    "Quinoa", "Radis", "Raisin", "Ravioli", "Rhubarbe", "Ricotta", "Riz cru",
    "Rognon", "Roquefort", "Salami", "Sardine", "Saumon", "Saucisson", "Semoule",
    "Soja", "Sole", "Sorbet", "Steak haché", "Sucre", "Surimi", "Sushi", "Tofu",
    "Tomate", "Truite", "Veau", "Viande des Grisons", "Vinaigre", "Yaourt"
])


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Point d'entrée principal de l'application.
    Gère l'affichage du formulaire et le traitement du scraping.
    """
    resultat = None
    erreur = None
    correction_auto = None
    query = request.form.get('food_input', '').strip()

    if request.method == 'POST' and query:
        target_food = query

        # Logique d'auto-correction floue
        if query not in ALIMENTS_DISPONIBLES:
            matches = difflib.get_close_matches(query, ALIMENTS_DISPONIBLES, n=1, cutoff=0.6)
            if matches:
                target_food = matches[0]
                correction_auto = target_food

        try:
            # Nom de variable explicite (pas juste 'f')
            food_item = Food()
            food_item.retrieve_food_infos(target_food)
            resultat = food_item
        except (ConnectionError, FileNotFoundError) as err:
            erreur = f"Problème lors de la recherche : {err}"
        except Exception:  # pylint: disable=broad-except
            erreur = f"Désolé, impossible de trouver '{target_food}'."

    return render_template('index.html',
                           aliments=ALIMENTS_DISPONIBLES,
                           resultat=resultat,
                           erreur=erreur,
                           query=query,
                           correction_auto=correction_auto)


if __name__ == '__main__':
    app.run(debug=True)