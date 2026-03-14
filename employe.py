from models.personne import Personne


class Employe(Personne):
    def __init__(self, nom, prenom, sexe, date_embauche, code_utilisateur, password, type_acces):
        super().__init__(nom, prenom, sexe)
        self.date_embauche = date_embauche
        self.code_utilisateur = code_utilisateur
        self.password = password
        self.type_acces = type_acces  # "lecture" ou "total"