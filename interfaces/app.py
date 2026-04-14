"""
Serveur Flask pour l'analyseur nutritionnel.
Gère les routes web et l'interaction avec la classe Food.
"""

import sys
import os
from flask import Flask, render_template, request

# Cette ligne dit à Python d'aller chercher food.py dans le dossier parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from food import Food # Maintenant il va le trouver !

app = Flask(__name__, template_folder='../templates')


@app.route('/', methods=['GET', 'POST'])
def home():
    """Route principale affichant le formulaire et les résultats."""
    resultat = None
    erreur = None
    
    if request.method == 'POST':
        food_name = request.form.get('food')
        if food_name:
            try:
                # Initialisation du moteur
                my_food = Food()
                my_food.retrieve_food_infos(food_name)
                resultat = my_food
                # Sauvegarde automatique
                my_food.save_to_csv_file("historique_web.csv")
            except Exception as e:
                erreur = f"Impossible de trouver l'aliment : {e}"
    
    return render_template('index.html', resultat=resultat, erreur=erreur)

if __name__ == '__main__':
    app.run(debug=True)