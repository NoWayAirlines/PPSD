"""
Interface Graphique pour l'analyseur nutritionnel.
Permet de rechercher des aliments et d'afficher leurs valeurs dans une fenêtre.
"""

import tkinter as tk
from tkinter import messagebox
from food import Food

class FoodApp:
    """Classe principale de l'application graphique."""

    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur Nutritionnel Pro")
        self.root.geometry("400x450")
        self.root.configure(bg="#f0f0f0")

        # Instance de notre moteur Food
        self.food_engine = Food()

        # --- Création de l'interface ---
        self._setup_ui()

    def _setup_ui(self):
        """Configure les widgets de la fenêtre."""
        # Titre
        tk.Label(self.root, text="Recherche d'Aliment", font=("Arial", 16, "bold"), 
                 bg="#f0f0f0", fg="#333").pack(pady=10)

        # Champ de saisie
        self.entry_food = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.entry_food.pack(pady=5)
        self.entry_food.insert(0, "riz cru") # Exemple par défaut

        # Bouton Rechercher
        tk.Button(self.root, text="Analyser", command=self.process_search,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                  width=20, height=2).pack(pady=15)

        # Zone d'affichage des résultats
        self.result_frame = tk.LabelFrame(self.root, text=" Valeurs pour 100g ", 
                                          bg="#f0f0f0", padx=10, pady=10)
        self.result_frame.pack(padx=20, fill="both", expand=True)

        self.label_cal = tk.Label(self.result_frame, text="Calories: -", bg="#f0f0f0")
        self.label_cal.pack(anchor="w")
        
        self.label_prot = tk.Label(self.result_frame, text="Protéines: -", bg="#f0f0f0")
        self.label_prot.pack(anchor="w")

        self.label_carb = tk.Label(self.result_frame, text="Glucides: -", bg="#f0f0f0")
        self.label_carb.pack(anchor="w")

        self.label_fat = tk.Label(self.result_frame, text="Lipides: -", bg="#f0f0f0")
        self.label_fat.pack(anchor="w")

        # Indicateur de gras
        self.label_status = tk.Label(self.root, text="", font=("Arial", 10, "italic"), bg="#f0f0f0")
        self.label_status.pack(pady=10)

    def process_search(self):
        """Récupère les données et met à jour l'affichage."""
        name = self.entry_food.get().strip()
        if not name:
            messagebox.showwarning("Attention", "Veuillez entrer un nom d'aliment.")
            return

        try:
            self.food_engine.retrieve_food_infos(name)
            
            # Mise à jour des labels (on utilise les @property de food.py)
            self.label_cal.config(text=f"Calories : {self.food_engine.calories} kcal")
            self.label_prot.config(text=f"Protéines : {self.food_engine.proteins} g")
            self.label_carb.config(text=f"Glucides : {self.food_engine.carbs} g")
            self.label_fat.config(text=f"Lipides : {self.food_engine.fat} g")

            # Logique is_fat
            if self.food_engine.is_fat():
                self.label_status.config(text="⚠️ Riche en lipides !", fg="red")
            else:
                self.label_status.config(text="✅ Taux de lipides correct", fg="green")

            # Sauvegarde automatique
            self.food_engine.save_to_csv_file("historique_gui.csv")

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de trouver l'aliment : {e}")

if __name__ == "__main__":
    window = tk.Tk()
    app = FoodApp(window)
    window.mainloop()