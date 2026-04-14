"""
Interface graphique NutriScan (guifood).
Permet une utilisation desktop du moteur de recherche nutritionnel.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from food import Food


class NutriScanGUI:
    """
    Application graphique principale pour NutriScan.
    """

    def __init__(self, root: tk.Tk) -> None:
        """Configure l'interface et les widgets."""
        self.root = root
        self.root.title("NutriScan Pro - Desktop")
        self.root.geometry("400x500")
        
        # Initialisation du moteur
        self.engine = Food()

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Crée les composants de l'interface."""
        # Titre
        ttk.Label(self.root, text="NutriScan Search", font=("Helvetica", 16, "bold")).pack(py=20)

        # Champ de saisie
        self.entry_var = tk.StringVar()
        ttk.Label(self.root, text="Entrez un aliment :").pack()
        self.entry = ttk.Entry(self.root, textvariable=self.entry_var, width=30)
        self.entry.pack(pady=10)

        # Bouton
        self.btn_search = ttk.Button(self.root, text="Analyser", command=self.handle_search)
        self.btn_search.pack(pady=10)

        # Zone de résultats
        self.result_text = tk.StringVar(value="\n\nEn attente de recherche...")
        ttk.Label(self.root, textvariable=self.result_text, justify="center").pack(pady=20)

    def handle_search(self) -> None:
        """Gère l'événement de recherche et met à jour l'affichage."""
        query = self.entry_var.get().strip()
        if not query:
            messagebox.showwarning("Attention", "Veuillez saisir un aliment.")
            return

        self.btn_search.config(state="disabled")
        
        try:
            self.engine.retrieve_food_infos(query)
            self._display_results()
        except FileNotFoundError as err:
            messagebox.showerror("Erreur", str(err))
            self.result_text.set("Aliment introuvable.")
        except ConnectionError:
            messagebox.showerror("Erreur", "Problème de connexion internet.")
        finally:
            self.btn_search.config(state="normal")

    def _display_results(self) -> None:
        """Met à jour le texte des résultats avec les données de l'ingénieur."""
        res = (
            f"Résultats pour : {self.engine.name}\n"
            f"---------------------------\n"
            f"🔥 Calories : {self.engine.calories} kcal\n"
            f"💪 Protéines : {self.engine.proteins} g\n"
            f"🍞 Glucides : {self.engine.carbs} g\n"
            f"🥑 Lipides : {self.engine.fat} g\n"
        )
        if self.engine.is_fat():
            res += "\n⚠️ Aliment riche en graisses !"
        
        self.result_text.set(res)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = NutriScanGUI(app_root)
    app_root.mainloop()