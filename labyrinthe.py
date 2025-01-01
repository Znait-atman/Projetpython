import random

class Labyrinthe:
    '''
    Classe qui représente un labyrinthe.
    - Une grille de murs (1) et chemins(0).
    - La position initiale du joueur(départ).
    - La position de la sortie (fin).
    - Deux méthodes.
    '''
    def __init__(self, largeur, hauteur):
        '''
        Constructeur
        '''
        self.largeur = largeur  # nb colonnes
        self.hauteur = hauteur  # nb lignes
        # Initialisation de la grille en matrice de 1
        self.grille = [[1 for _ in range(largeur)] for _ in range(hauteur)]
        # la position initiale du joueur
        self.joueur_x = 0
        self.joueur_y = 0
        # la position de la sortie
        self.sortie_x = largeur - 1
        self.sortie_y = hauteur - 1

    def generer_labyrinthe(self):
        '''
        Genere un labyrinthe aleatoire en utilisant un parcours en profondeur (DFS).
        - On utilise une pile pour se déplacer entre les cases
        '''
        pile = []  # pile pour stocker les positions des cases en cours de traitement
        debut_x, debut_y = (0, 0)  # point de depart du labyrinthe
        self.grille[debut_y][debut_x] = 0  # chemin = 0
        pile.append((debut_x, debut_y))  # on ajoute la case de départ à la pile
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]


        while pile:  # tant que la pile n'est pas vide
            x, y = pile[-1]  # on récupère la dernière case ajoutée à la pile
            random.shuffle(directions)  # on prend une direction aléatoire
            creuse = False


            for dx, dy in directions:  # parcourt les directions possibles
                nx, ny = x + dx, y + dy  # coordonnées de la case voisine en fonction de la direction
                if (0 <= nx < self.largeur and  # on doit vérifier que nx est dans les limites horizontales
                        0 <= ny < self.hauteur and  #  on doit vérifier que ny est dans les limites verticales
                        self.grille[ny][nx] == 1):  #  on doit vérifier que la case voisine est un mur
                    self.grille[ny][nx] = 0  # Case ------> chemin (0)
                    self.grille[y + dy // 2][x + dx // 2] = 0  # Casse le mur intermédiaire
                    pile.append((nx, ny))  # on ajout de la case voisine à la pile
                    creuse = True  # Un chemin creusé ---> sortir de la boucle
                    break


            if not creuse:  # si aucun chemin n'a été creusé, on retire la case actuelle de la pile (impasse)
                pile.pop()
                
    def adapter_dimensions_labyrinthe(self, largeur, hauteur):
        '''
        Adapter les dimensions du Labyrinthe pour que l'algorithme de DFS fonctionne correctement
        - On doit avoir des dimernsions impaires 
        - On doit respecter une certaine limite de dimension pour avoir une affichage claire et complète
        '''
        # On doit verifier si les dimensions sont impaires, car l'algorithme DFS fonctionne mieux ainsi.
        if largeur % 2 == 0:
            largeur += 1
        if hauteur % 2 == 0:
            hauteur += 1

        # On doit verifier les limites minimales et maximales
        largeur = max(5, min(largeur, 101))
        hauteur = max(5, min(hauteur, 101))

        # on récupère les bonnes valeurs
        self.largeur = largeur
        self.hauteur = hauteur

        return largeur, hauteur


