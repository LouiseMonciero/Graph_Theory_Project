from itertools import product

class Element:
    def __init__(self, valeur, successeur):
        self.valeur = valeur
        self.successeur = successeur  # Liste des valeurs qu'il peut suivre

    def __repr__(self):
        return f"{self.valeur}"

def generate_valid_combinations(t):
    all_combinations = product(*t)  # Génère toutes les combinaisons possibles
    valid_combinations = []
    
    for comb in all_combinations:
        valid = True
        for i in range(1, len(comb)):
            if comb[i].valeur not in comb[i-1].successeur:
                valid = False
                break
        if valid:
            valid_combinations.append([elem.valeur for elem in comb])  # Stocke les valeurs

    return valid_combinations

# Définition des objets avec leur successeur autorisé
e1 = Element(1, [3])  
e2 = Element(2, [3])
e3 = Element(3, [4, 5])  
e0 = Element(0, [4])  
e4 = Element(4, [])  
e5 = Element(5, [])

# Exemple de liste t avec ces objets
t1 = [[e1, e2], [e3, e0], [e4, e5]]

# Génération des combinaisons valides
l1 = generate_valid_combinations(t1)

print(l1)  # Affiche uniquement les combinaisons respectant les successeurs
