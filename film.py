class Film:
    def __init__(self, nom, duree, description, categories=None, acteurs=None):
        self.nom = nom
        self.duree = duree
        self.description = description
        self.categories = categories if categories is not None else []
        self.acteurs = acteurs if acteurs is not None else []