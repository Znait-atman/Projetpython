import tkinter as tk
import time

class Affichage:
    # constructeur 
    def __init__(self, largeur, hauteur, taille_case=20):
        self.largeur = largeur  # nb cases en largeur 
        self.hauteur = hauteur
        self.taille_case = taille_case  # taille de chaque case en pixels 
        
        # Ajustement dynamique de la taille des cases si le labyrinthe est trop grand
        screen_width = 800  # Largeur maximale de la fenêtre
        screen_height = 600  # Hauteur maximale de la fenêtre
        max_case_width = screen_width // self.largeur # taille max des cases en hauteur 
        max_case_height = screen_height // self.hauteur # taille min
        self.taille_case = min(self.taille_case, max_case_width, max_case_height) #ajustement des cases 
        
        self.fenetre = tk.Tk()  # fenetre graphique avec tkinter 
        self.fenetre.title("Jeu de Labyrinthe") 
        self.canvas = tk.Canvas( 
            self.fenetre,
            width=self.largeur * self.taille_case, # largeur canvas 
            height=self.hauteur * self.taille_case, 
            bg="#2B2B2B"  # couleur de fond sombre 
        )
        self.canvas.pack()  # ajout du canvas à la fenetre 

        # Ajuste la geometrie de la fenetre pour s'adapter au canvas
        self.fenetre.geometry(f"{self.largeur * self.taille_case}x{self.hauteur * self.taille_case}")
        self.fenetre.update_idletasks()  # Mise à jour de l'affichage pour garantir le redimensionnement
        
       

    # dessine le labyrinthe, le joueur et le chemin parcouru
    def dessiner_labyrinthe(self, grille, joueur_x, joueur_y, sortie_x, sortie_y):
        self.canvas.delete("all")  # un clean pour le canvas
        # parcours de la grille 
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if grille[y][x] == 1:
                    couleur = "#2B2B2B"  # Mur en noir
                elif grille[y][x] == 0.5:
                    couleur = "#FFD700"  # Chemin parcouru en jaune
                else:
                    couleur = "#E0E0E0"  # Chemin libre en gris clair  
                # creature de la case    
                self.canvas.create_rectangle(
                    x * self.taille_case, y * self.taille_case,  # point de départ de la case 
                    (x + 1) * self.taille_case, (y + 1) * self.taille_case,  # point d'arrivée (logique canvas de tkinter)
                    fill=couleur, outline="#404040"
                )
        # creation du joueur         
        self.canvas.create_oval(
            joueur_x * self.taille_case + 2, joueur_y * self.taille_case + 2,
            (joueur_x + 1) * self.taille_case - 2, (joueur_y + 1) * self.taille_case - 2,
            fill="#1E90FF", outline="white"
        )
        # creation d'un rectangle representant la sortie 
        self.canvas.create_rectangle(
            max(0, sortie_x * self.taille_case),
            max(0, sortie_y * self.taille_case),
            min(self.largeur * self.taille_case, (sortie_x + 1) * self.taille_case),
            min(self.hauteur * self.taille_case, (sortie_y + 1) * self.taille_case),
            fill="#32CD32", outline="white"
        )
        self.fenetre.update()
        

    # affichage d'un message de victoire une fois la sortie atteinte 
    def afficher_victoire(self):
        self.canvas.create_text(
            # positionnement au centre 
            self.largeur * self.taille_case // 2,
            self.hauteur * self.taille_case // 2,
            text="Victoire !", fill="#FF6347", font=("Arial", 24)
        )
        self.fenetre.update()
        

    # affichage d'un menu pour choisir entre jouer manuellement ou appeler Dijkstra 
    def afficher_menu(self, labyrinthe, chercher_chemin_dijkstra):
        #mode manuel
        def lancer_jeu():
            print("Mode manuel activé.")
            self.canvas.delete("all")
            self.dessiner_labyrinthe(
                labyrinthe.grille, labyrinthe.joueur_x, labyrinthe.joueur_y,
                labyrinthe.sortie_x, labyrinthe.sortie_y
            )
            # association des touches du clavier au déplacement du joueur 
            self.fenetre.bind("<KeyPress>", lambda event: self.deplacer_joueur(event, labyrinthe))
            self.fenetre.mainloop()
        # mode djikstra
        def lancer_dijkstra():
            print("Mode Dijkstra active.")
            self.canvas.delete("all")
            chemin = chercher_chemin_dijkstra(  # chercher le chemin le plus court
                labyrinthe.grille, (0, 0), (labyrinthe.sortie_x, labyrinthe.sortie_y)
            )
            for x, y in chemin:
                # Marque le chemin dans la grille
                labyrinthe.grille[y][x] = 0.5  # 0.5 pour chemin parcouru
                labyrinthe.joueur_x, labyrinthe.joueur_y = x, y  # mise à jour de la position du joueur 
                self.dessiner_labyrinthe(
                    labyrinthe.grille, labyrinthe.joueur_x, labyrinthe.joueur_y,
                    labyrinthe.sortie_x, labyrinthe.sortie_y
                )
                time.sleep(0.1)  # Pause pour animation fluide
            self.afficher_victoire()
            self.fenetre.mainloop()

        self.canvas.delete("all")
        self.canvas.create_text(
            self.largeur * self.taille_case // 2,
            self.hauteur * self.taille_case // 3,
            text="Choisissez une option :", fill="#FFFFFF", font=("Arial", 24), anchor="center"
        )
        self.canvas.create_text(
            self.largeur * self.taille_case // 2,
            self.hauteur * self.taille_case // 2,
            text="1. Jouer manuellement", fill="#32CD32", font=("Arial", 18), anchor="center"
        )
        self.canvas.create_text(
            self.largeur * self.taille_case // 2,
            self.hauteur * self.taille_case // 1.5,
            text="2. Trouver un chemin (Dijkstra)", fill="#1E90FF", font=("Arial", 18), anchor="center"
        )

        self.fenetre.bind("1", lambda event: lancer_jeu())  # associe la touche au mode manuel
        self.fenetre.bind("2", lambda event: lancer_dijkstra())
        self.fenetre.update()
        self.fenetre.mainloop()

    # déplacement du joueur 
    def deplacer_joueur(self, event, labyrinthe):
        
        direction = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}

        if event.keysym in direction:  # vérifie si la touche choisie correspond à une direction 
            dx, dy = direction[event.keysym]  # récupère le déplacement par rapport à la touche
            # calcul nouvelle position joueur
            nouveau_x = labyrinthe.joueur_x + dx
            nouveau_y = labyrinthe.joueur_y + dy

            # Vérifie si le joueur peut se déplacer sur cette case
            if (0 <= nouveau_x < labyrinthe.largeur and 
                0 <= nouveau_y < labyrinthe.hauteur and 
                labyrinthe.grille[nouveau_y][nouveau_x] == 0):
                # Marque la case actuelle comme visitée
                labyrinthe.grille[labyrinthe.joueur_y][labyrinthe.joueur_x] = 0.5  # 0.5 pour chemin parcouru
                labyrinthe.joueur_x = nouveau_x
                labyrinthe.joueur_y = nouveau_y
                # redessine le labyrinthe avec la nouvelle position du joueur 
                self.dessiner_labyrinthe(labyrinthe.grille, labyrinthe.joueur_x, labyrinthe.joueur_y, labyrinthe.sortie_x, labyrinthe.sortie_y)

            # vérifie si le joueur atteint la sortie
            if labyrinthe.joueur_x == labyrinthe.sortie_x and labyrinthe.joueur_y == labyrinthe.sortie_y:
                self.afficher_victoire()

