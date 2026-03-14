from models.personne import Personne


class Client(Personne):

    def __init__(self, nom, prenom, sexe, date_inscription, courriel, password, cartes_credit):
        super().__init__(nom, prenom, sexe)

        self.date_inscription = date_inscription
        self.courriel = courriel
        self.password = password
        self.cartes_credit = cartes_credit