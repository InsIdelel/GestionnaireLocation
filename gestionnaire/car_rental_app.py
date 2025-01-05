import os
import json
import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk


SAVE_FILE = "sauvegarde.json"
IMAGE_FOLDER = "images"


DEFAULT_DATA = [
    {"nom": "Renault Clio", "photo": "clio.jpg", "stock": 10, "en_location": 3},
    {"nom": "Peugeot 208", "photo": "208.jpg", "stock": 8, "en_location": 1}
]

# Charge les données du fichier de sauvegarde
def chargement():
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'w') as f:
            json.dump(DEFAULT_DATA, f, indent=4)
    with open(SAVE_FILE, 'r') as f:
        return json.load(f)

# Sauvegarder les données dans le fichier des sauvegarde
def sauvegarde(data):
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Augmente le compteur de location pour la voiture mise en argumet
def increment_rental(car):
    if car['stock'] > 0:
        car['stock'] -= 1
        car['en_location'] += 1
        sauvegarde(data)



# Diminue le compteur de location pour la voiture mise en argument
def decrement_rental(car):
    if car['en_location'] > 0:
        car['stock'] += 1
        car['en_location'] -= 1
        sauvegarde(data)


def main():
    global data
    data = chargement()

    
    fenetre = tk.Tk()
    fenetre.title("Gestion de Location de Voitures")
    fenetre.geometry("800x600")

    # accueil
    def show_dashboard():
        accueil_frame.pack_forget()
        dashboard_frame.pack(fill="both", expand=True)

    accueil_frame = tk.Frame(fenetre)
    accueil_frame.pack(fill="both", expand=True)

    welcome_label = tk.Label(accueil_frame, text="Bienvenue dans le prototype d'application de gestion de location de voitures", font=("Arial", 16))
    welcome_label.pack(pady=20)

    dashboard_button = tk.Button(accueil_frame, text="Aller au tableau de bord", font=("Arial", 14), command=show_dashboard)
    dashboard_button.pack(pady=20)

    # dashboard
    dashboard_frame = tk.Frame(fenetre)

    def update_dashboard():
        for widget in dashboard_frame.winfo_children():
            widget.destroy()

        for car in data:
            tile = tk.Frame(dashboard_frame, borderwidth=2, relief="ridge")
            tile.pack(pady=10, padx=10, fill="x")

            # Info de la voiture
            car_name = tk.Label(tile, text=car['nom'], font=("Arial", 14))
            car_name.pack(anchor="w", padx=10)

            # Photo  voiture
            image_path = os.path.join(IMAGE_FOLDER, car['photo'])
            
            print(image_path)

            if os.path.exists(image_path):
                car_image = ImageTk.PhotoImage(Image.open(image_path).resize((150, 100)))
                image_label = tk.Label(tile, image=car_image)
                image_label.image = car_image  # Empêche le garbage collection
                image_label.pack(side="left", padx=10)
            else:
                error_label = tk.Label(tile, text=image_path, fg="red")
                error_label.pack(side="left", padx=10)

            # Données de stock
            stock_label = tk.Label(tile, text=f"Stock: {car['stock']} • En location: {car['en_location']}", font=("Arial", 12))
            stock_label.pack(anchor="w", padx=10)

            # Boutons
            buttons_frame = tk.Frame(tile)
            buttons_frame.pack(anchor="e", padx=10, pady=5)

            rent_button = tk.Button(buttons_frame, text="+", command=lambda c=car: [increment_rental(c), update_dashboard()])
            rent_button.pack(side="left", padx=5)
            if car['stock'] == 0:
                rent_button.config(state="disabled")

            return_button = tk.Button(buttons_frame, text="-", command=lambda c=car: [decrement_rental(c), update_dashboard()])
            return_button.pack(side="left", padx=5)
            if car['en_location'] == 0:
                return_button.config(state="disabled")

    update_dashboard()

    fenetre.mainloop()

if __name__ == "__main__":
    main()
