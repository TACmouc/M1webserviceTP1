import tkinter as tk
from tkinter import ttk
import requests

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendrier Viewer")

        # Créer les étiquettes et les champs de saisie
        self.label_month = tk.Label(root, text="Mois (1-12):")
        self.label_year = tk.Label(root, text="Année:")
        self.entry_month = tk.Entry(root)
        self.entry_year = tk.Entry(root)
        self.button_show = tk.Button(root, text="Afficher", command=self.show_calendar)

        # Placer les éléments sur la grille
        self.label_month.grid(row=0, column=0)
        self.label_year.grid(row=1, column=0)
        self.entry_month.grid(row=0, column=1)
        self.entry_year.grid(row=1, column=1)
        self.button_show.grid(row=2, columnspan=2)

        # Créer un Treeview pour afficher les jours du calendrier
        self.treeview = ttk.Treeview(root, columns=("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"), show="headings")
        for day in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]:
            self.treeview.heading(day, text=day)
            self.treeview.column(day, width=50)  # Réduire la largeur des colonnes
        self.treeview.grid(row=3, column=0, columnspan=2)

        # Créer un champ de saisie pour ajouter une tâche
        self.label_task = tk.Label(root, text="Tâche:")
        self.entry_task = tk.Entry(root)
        self.button_add_task = tk.Button(root, text="Ajouter Tâche", command=self.add_task)
        self.label_task.grid(row=4, column=0)
        self.entry_task.grid(row=4, column=1)
        self.button_add_task.grid(row=4, column=2)

        # Associer un événement de clic au Treeview pour la sélection d'une journée
        self.treeview.bind("<ButtonRelease-1>", self.select_day)

        # Garder une référence au jour sélectionné
        self.selected_day = None

        # Créer un Treeview pour afficher les tâches
        self.task_treeview = ttk.Treeview(root, columns=("Jour", "Tâche"), show="headings")
        self.task_treeview.heading("Jour", text="Jour")
        self.task_treeview.heading("Tâche", text="Tâche")
        self.task_treeview.grid(row=5, column=0, columnspan=2)

        self.label_selected_day = tk.Label(root, text="Journée sélectionnée:")
        self.label_selected_day.grid(row=6, column=0, columnspan=2)

    def show_calendar(self):
        month = self.entry_month.get()
        year = self.entry_year.get()

        if month and year:
            try:
                # Effacer les données actuelles du Treeview
                for item in self.treeview.get_children():
                    self.treeview.delete(item)

                # Effacer les données actuelles du Treeview des tâches
                for item in self.task_treeview.get_children():
                    self.task_treeview.delete(item)

                # Envoyer une requête à l'API pour obtenir les jours du calendrier
                response = requests.get(f"http://localhost:5000/calendrier?month={month}&year={year}")
                data = response.json()

                # Afficher les jours dans le Treeview
                days = data.get("days", [])
                row_values = [""] * 7  # Initialiser une liste vide de 7 colonnes
                for day_info in days:
                    day = day_info["day"]
                    day_name = day_info["day_name"]
                    # Trouver le bon jour de la semaine dans le tableau
                    column_index = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"].index(day_name)
                    row_values[column_index] = day
                    # Si le jour est dimanche, ajouter la ligne et réinitialiser les valeurs
                    if day_name == "dimanche":
                        self.treeview.insert("", "end", values=row_values)
                        row_values = [""] * 7

            except Exception as e:
                self.treeview.delete(*self.treeview.get_children())
                self.treeview.insert("", "end", values=("Erreur:", str(e)))
        else:
            self.treeview.delete(*self.treeview.get_children())
            self.treeview.insert("", "end", values=("Veuillez entrer un mois et une année valides.", ""))

    def select_day(self, event):
        selected_item = self.treeview.selection()
        if selected_item:
            self.selected_day = self.treeview.item(selected_item)["values"][0]
            self.label_selected_day.config(text=f"Journée sélectionnée: {self.selected_day}/{self.entry_month.get()}/{self.entry_year.get()}")

    def add_task(self):
        if self.selected_day:
            task = self.entry_task.get()
            if task:
                try:
                    # Envoyer une requête POST à l'API pour ajouter la tâche
                    print(self.selected_day)
                    data = {"date": f"{self.selected_day}/{self.entry_month.get()}/{self.entry_year.get()}", "task": task}
                    response = requests.post("http://localhost:5000/calendrier/add_task", json=data)
                    print(response)

                    if response.status_code == 200:
                        # Ajouter la tâche au Treeview des tâches
                        self.task_treeview.insert("", "end", values=(self.selected_day, task))
                        # Effacer la zone de saisie de la tâche
                        self.entry_task.delete(0, tk.END)

                    else:
                        self.task_treeview.delete(*self.task_treeview.get_children())
                        self.task_treeview.insert("", "end", values=("Erreur:", "Impossible d'ajouter la tâche"))

                except Exception as e:
                    self.task_treeview.delete(*self.task_treeview.get_children())
                    self.task_treeview.insert("", "end", values=("Erreur:", str(e)))


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
