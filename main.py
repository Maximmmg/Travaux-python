# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox

from models.client import Client
from models.employe import Employe
from models.acteur import Acteur
from models.carte_credit import CarteCredit
from models.categorie import Categorie
from models.film import Film


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class ApplicationStreaming:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Streaming")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)

        self.employes = []
        self.clients = []
        self.films = []
        self.employe_connecte = None

        self.creer_donnees_hardcodees()
        self.afficher_login()

    def creer_donnees_hardcodees(self):
        # Employés hardcodés
        self.employes = [
            Employe(
                "Admin", "Maxim", "M",
                "2023-01-15", "admin",
                hash_password("admin123"),
                "total"
            ),
            Employe(
                "Lecteur", "Paul", "M",
                "2024-05-10", "lecture",
                hash_password("lecture123"),
                "lecture"
            )
        ]

        # Catégories
        cat_action = Categorie("Action", "Films d'action")
        cat_comedie = Categorie("Comédie", "Films comiques")
        cat_sf = Categorie("Science-fiction", "Films futuristes")

        # Acteurs
        acteur1 = Acteur("Evans", "Chris", "M", "Capitaine Nord", "2018-01-01", "", 1000000)
        acteur2 = Acteur("Johansson", "Scarlett", "F", "Agent Rouge", "2019-01-01", "", 1200000)
        acteur3 = Acteur("Carey", "Jim", "M", "Monsieur Drôle", "2015-01-01", "", 900000)

        # Films
        film1 = Film(
            "FAST N'FURIOUS", 125, "Une mission dangereuse dans l'espace.",
            [cat_action, cat_sf],
            [acteur1, acteur2]
        )
        film2 = Film(
            "Louis des funes", 95, "Une comédie remplie de malentendus.",
            [cat_comedie],
            [acteur3]
        )

        self.films = [film1, film2]

        # Clients
        carte1 = CarteCredit("1111222233334444", "12/28", "123")
        carte2 = CarteCredit("5555666677778888", "09/27", "456")

        self.clients = [
            Client("Homme", "Tit", "M", "2026-03-01", "tit@email.com", hash_password("password123"), [carte1]),
            Client("Martel", "Kirikou", "F", "2026-03-02", "kirikou@email.com", hash_password("bonjour123"), [carte2]),
            Client("Simard", "Alex", "X", "2026-03-03", "alex@email.com", hash_password("soleil123"), [])
        ]

    def nettoyer_fenetre(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def afficher_login(self):
        self.nettoyer_fenetre()

        cadre = tk.Frame(self.root, padx=20, pady=20)
        cadre.pack(expand=True)

        tk.Label(cadre, text="Connexion employé", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(cadre, text="Code utilisateur :").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_code = tk.Entry(cadre, width=30)
        self.entry_code.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(cadre, text="Mot de passe :").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_password = tk.Entry(cadre, width=30, show="*")
        self.entry_password.grid(row=2, column=1, padx=5, pady=5)

        btn_connexion = tk.Button(cadre, text="Se connecter", width=20, command=self.connexion)
        btn_connexion.grid(row=3, column=0, columnspan=2, pady=15)

        info = (
            "Comptes de test :\n"
            "admin / admin123  (accès total)\n"
            "lecture / lecture123  (accès lecture)"
        )
        tk.Label(cadre, text=info, justify="left", fg="gray").grid(row=4, column=0, columnspan=2, pady=10)

    def connexion(self):
        try:
            code = self.entry_code.get().strip()
            mot_de_passe = self.entry_password.get().strip()

            if not code or not mot_de_passe:
                raise ValueError("Veuillez entrer le code utilisateur et le mot de passe.")

            mot_de_passe_hash = hash_password(mot_de_passe)

            for employe in self.employes:
                if employe.code_utilisateur == code and employe.password == mot_de_passe_hash:
                    self.employe_connecte = employe
                    messagebox.showinfo("Succès", f"Bienvenue {employe.prenom} {employe.nom} !")
                    self.afficher_fenetre_principale()
                    return

            raise ValueError("Code utilisateur ou mot de passe invalide.")

        except Exception as e:
            messagebox.showerror("Erreur de connexion", str(e))

    def afficher_fenetre_principale(self):
        self.nettoyer_fenetre()

        self.creer_menu()

        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack(fill="x")

        acces_text = f"Employé connecté : {self.employe_connecte.prenom} {self.employe_connecte.nom} | Accès : {self.employe_connecte.type_acces}"
        tk.Label(frame_top, text=acces_text, font=("Arial", 12, "bold")).pack()

        principal = tk.Frame(self.root)
        principal.pack(fill="both", expand=True, padx=10, pady=10)

        # SECTION CLIENTS
        frame_clients = tk.LabelFrame(principal, text="Clients", padx=10, pady=10)
        frame_clients.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.table_clients = ttk.Treeview(
            frame_clients,
            columns=("nom", "prenom", "courriel"),
            show="headings",
            height=15
        )
        self.table_clients.heading("nom", text="Nom")
        self.table_clients.heading("prenom", text="Prénom")
        self.table_clients.heading("courriel", text="Courriel")

        self.table_clients.column("nom", width=120)
        self.table_clients.column("prenom", width=120)
        self.table_clients.column("courriel", width=220)
        self.table_clients.pack(fill="both", expand=True)

        boutons_clients = tk.Frame(frame_clients)
        boutons_clients.pack(pady=10)

        self.btn_ajouter = tk.Button(boutons_clients, text="Créer client", width=15, command=self.ouvrir_creation_client)
        self.btn_modifier = tk.Button(boutons_clients, text="Modifier client", width=15, command=self.ouvrir_modification_client)
        self.btn_supprimer = tk.Button(boutons_clients, text="Supprimer client", width=15, command=self.supprimer_client)

        self.btn_ajouter.grid(row=0, column=0, padx=5)
        self.btn_modifier.grid(row=0, column=1, padx=5)
        self.btn_supprimer.grid(row=0, column=2, padx=5)

        # SECTION FILMS
        frame_films = tk.LabelFrame(principal, text="Films", padx=10, pady=10)
        frame_films.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.table_films = ttk.Treeview(
            frame_films,
            columns=("nom", "duree", "categories"),
            show="headings",
            height=15
        )
        self.table_films.heading("nom", text="Nom")
        self.table_films.heading("duree", text="Durée")
        self.table_films.heading("categories", text="Catégories")

        self.table_films.column("nom", width=180)
        self.table_films.column("duree", width=80)
        self.table_films.column("categories", width=200)
        self.table_films.pack(fill="both", expand=True)

        self.table_films.bind("<<TreeviewSelect>>", self.afficher_details_film)

        self.label_details_film = tk.Label(
            frame_films,
            text="Sélectionnez un film pour voir ses acteurs.",
            justify="left",
            anchor="w"
        )
        self.label_details_film.pack(fill="x", pady=10)

        self.rafraichir_clients()
        self.rafraichir_films()
        self.appliquer_droits_acces()

    def creer_menu(self):
        barre_menu = tk.Menu(self.root)

        menu_fichier = tk.Menu(barre_menu, tearoff=0)
        menu_fichier.add_command(label="Se déconnecter", command=self.deconnexion)
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.root.quit)

        barre_menu.add_cascade(label="Fichier", menu=menu_fichier)
        self.root.config(menu=barre_menu)

    def deconnexion(self):
        self.employe_connecte = None
        self.afficher_login()

    def appliquer_droits_acces(self):
        if self.employe_connecte.type_acces == "lecture":
            self.btn_ajouter.config(state="disabled")
            self.btn_modifier.config(state="disabled")
            self.btn_supprimer.config(state="disabled")
        else:
            self.btn_ajouter.config(state="normal")
            self.btn_modifier.config(state="normal")
            self.btn_supprimer.config(state="normal")

    def rafraichir_clients(self):
        for item in self.table_clients.get_children():
            self.table_clients.delete(item)

        for index, client in enumerate(self.clients):
            self.table_clients.insert(
                "",
                "end",
                iid=str(index),
                values=(client.nom, client.prenom, client.courriel)
            )

    def rafraichir_films(self):
        for item in self.table_films.get_children():
            self.table_films.delete(item)

        for index, film in enumerate(self.films):
            categories = ", ".join([c.nom for c in film.categories])
            self.table_films.insert(
                "",
                "end",
                iid=str(index),
                values=(film.nom, f"{film.duree} min", categories)
            )

    def afficher_details_film(self, event=None):
        selection = self.table_films.selection()
        if not selection:
            return

        index = int(selection[0])
        film = self.films[index]

        acteurs = []
        for acteur in film.acteurs:
            acteurs.append(f"{acteur.prenom} {acteur.nom} ({acteur.nom_personnage})")

        texte = (
            f"Description : {film.description}\n"
            f"Acteurs : {', '.join(acteurs) if acteurs else 'Aucun'}"
        )
        self.label_details_film.config(text=texte)

    def ouvrir_creation_client(self):
        self.ouvrir_formulaire_client(mode="creation")

    def ouvrir_modification_client(self):
        selection = self.table_clients.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un client à modifier.")
            return

        index = int(selection[0])
        client = self.clients[index]
        self.ouvrir_formulaire_client(mode="modification", client=client, index=index)

    def ouvrir_formulaire_client(self, mode="creation", client=None, index=None):
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Créer un client" if mode == "creation" else "Modifier un client")
        fenetre.geometry("500x450")
        fenetre.grab_set()

        tk.Label(fenetre, text="Nom").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        entry_nom = tk.Entry(fenetre, width=30)
        entry_nom.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Prénom").grid(row=1, column=0, padx=10, pady=8, sticky="e")
        entry_prenom = tk.Entry(fenetre, width=30)
        entry_prenom.grid(row=1, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Sexe").grid(row=2, column=0, padx=10, pady=8, sticky="e")
        entry_sexe = tk.Entry(fenetre, width=30)
        entry_sexe.grid(row=2, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Date inscription").grid(row=3, column=0, padx=10, pady=8, sticky="e")
        entry_date = tk.Entry(fenetre, width=30)
        entry_date.grid(row=3, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Courriel").grid(row=4, column=0, padx=10, pady=8, sticky="e")
        entry_courriel = tk.Entry(fenetre, width=30)
        entry_courriel.grid(row=4, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Mot de passe").grid(row=5, column=0, padx=10, pady=8, sticky="e")
        entry_password = tk.Entry(fenetre, width=30, show="*")
        entry_password.grid(row=5, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Numéro carte").grid(row=6, column=0, padx=10, pady=8, sticky="e")
        entry_numero = tk.Entry(fenetre, width=30)
        entry_numero.grid(row=6, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Expiration carte").grid(row=7, column=0, padx=10, pady=8, sticky="e")
        entry_expiration = tk.Entry(fenetre, width=30)
        entry_expiration.grid(row=7, column=1, padx=10, pady=8)

        tk.Label(fenetre, text="Code secret").grid(row=8, column=0, padx=10, pady=8, sticky="e")
        entry_code_secret = tk.Entry(fenetre, width=30, show="*")
        entry_code_secret.grid(row=8, column=1, padx=10, pady=8)

        if mode == "modification" and client is not None:
            entry_nom.insert(0, client.nom)
            entry_prenom.insert(0, client.prenom)
            entry_sexe.insert(0, client.sexe)
            entry_date.insert(0, client.date_inscription)
            entry_courriel.insert(0, client.courriel)

            if client.cartes_credit:
                carte = client.cartes_credit[0]
                entry_numero.insert(0, carte.numero_carte)
                entry_expiration.insert(0, carte.date_expiration)
                entry_code_secret.insert(0, carte.code_secret)

        def sauvegarder():
            try:
                nom = entry_nom.get().strip()
                prenom = entry_prenom.get().strip()
                sexe = entry_sexe.get().strip()
                date_inscription = entry_date.get().strip()
                courriel = entry_courriel.get().strip().lower()
                password = entry_password.get().strip()
                numero = entry_numero.get().strip()
                expiration = entry_expiration.get().strip()
                code_secret = entry_code_secret.get().strip()

                if not nom or not prenom or not sexe or not date_inscription or not courriel:
                    raise ValueError("Tous les champs principaux doivent être remplis.")

                if not re.match(r"^[^@]+@[^@]+\.[^@]+$", courriel):
                    raise ValueError("Le courriel est invalide.")

                for i, autre_client in enumerate(self.clients):
                    if autre_client.courriel.lower() == courriel and i != index:
                        raise ValueError("Le courriel doit être unique.")

                if mode == "creation":
                    if len(password) < 8:
                        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")
                else:
                    if password and len(password) < 8:
                        raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

                cartes = []
                if numero or expiration or code_secret:
                    if not numero or not expiration or not code_secret:
                        raise ValueError("Pour la carte de crédit, remplissez tous les champs ou laissez-les tous vides.")
                    cartes.append(CarteCredit(numero, expiration, code_secret))

                if mode == "creation":
                    nouveau_client = Client(
                        nom,
                        prenom,
                        sexe,
                        date_inscription,
                        courriel,
                        hash_password(password),
                        cartes
                    )
                    self.clients.append(nouveau_client)
                    messagebox.showinfo("Succès", "Client créé avec succès.")
                else:
                    self.clients[index].nom = nom
                    self.clients[index].prenom = prenom
                    self.clients[index].sexe = sexe
                    self.clients[index].date_inscription = date_inscription
                    self.clients[index].courriel = courriel
                    self.clients[index].cartes_credit = cartes

                    if password:
                        self.clients[index].password = hash_password(password)

                    messagebox.showinfo("Succès", "Client modifié avec succès.")

                self.rafraichir_clients()
                fenetre.destroy()

            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        btn_texte = "Créer" if mode == "creation" else "Modifier"
        tk.Button(fenetre, text=btn_texte, width=20, command=sauvegarder).grid(
            row=9, column=0, columnspan=2, pady=20
        )

    def supprimer_client(self):
        try:
            selection = self.table_clients.selection()
            if not selection:
                raise ValueError("Veuillez sélectionner un client à supprimer.")

            index = int(selection[0])
            client = self.clients[index]

            confirmation = messagebox.askyesno(
                "Confirmation",
                f"Voulez-vous vraiment supprimer {client.prenom} {client.nom} ?"
            )

            if confirmation:
                del self.clients[index]
                self.rafraichir_clients()
                messagebox.showinfo("Succès", "Client supprimé avec succès.")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))


def main():
    root = tk.Tk()
    app = ApplicationStreaming(root)
    root.mainloop()


if __name__ == "__main__":
    main()






# See PyCharm help at https://www.jetbrains.com/help/pycharm/
