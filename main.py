from labyrinthe import Labyrinthe
from affichage import Affichage
from utils import chercher_chemin_dijkstra

if __name__ == "__main__":
    largeur, hauteur = 50, 50# dimensions du labyrinthe
    labyrinthe = Labyrinthe(largeur, hauteur)
    largeur, hauteur = labyrinthe.adapter_dimensions_labyrinthe(largeur, hauteur)
    labyrinthe = Labyrinthe(largeur, hauteur)
    affichage = Affichage(largeur, hauteur)

    labyrinthe.generer_labyrinthe()
    affichage.afficher_menu(labyrinthe, chercher_chemin_dijkstra)
