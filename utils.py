import heapq  # j’utilise heapq pour gérer une file de priorité 

def chercher_chemin_dijkstra(grille, debut, fin):
    """
    On veut trouver le chemin le plus court en utilisant l’algorithme de Dijkstra.
    
    Mots clés :
    - grille : une matrice qui représente le labyrinthe (0 : chemin libre, 1: mur).
    - debut : coordonnées (x, y) du point de départ.
    - fin : coordonnées (x, y) du point d’arrivée.
    
    """
    
    ''' Étape 1 : Initialisation '''
    
    # dimensions: largeur(nombre de colonnes) et l'hauteur(nombre de lignes)
    largeur, hauteur = len(grille[0]), len(grille)
    # Une liste qui représente les distances où toutes les cases contiennent « infini » au début  
    distances = [[float('inf')] * largeur for _ in range(hauteur)]
    # On initialise la distance du point de départ à 0
    distances[debut[1]][debut[0]] = 0
    # file de priorité avec un tuples de : (distance, coordonnées)
    file_priorite = [(0, debut)]
    # ce dictionnaire garde la trace des cases visitées
    noeuds_precedents = {}
    
    ''' Étape 2 : Boucle principale '''
    
    # tant que la liste est non vide la boucle continue
    while file_priorite:
        
        # On retire et retourne la case avec la plus petite distance
        distance_actuelle, (x, y) = heapq.heappop(file_priorite)
        
        # On vérifie si on est arrivé à la destination
        if (x, y) == fin:
            break

        # On cherche les voisins de la case (haut, bas, gauche, droite)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            # On doit vérifier si le voisin n'est pas un mur
            if 0 <= nx < largeur and 0 <= ny < hauteur and grille[ny][nx] == 0:
                # Si le voisin est valide on calcule la nouvelle distance
                nouvelle_distance = distance_actuelle + 1
                
                # On doit garder toujours la distance minimale pour atteindre la case
                if nouvelle_distance < distances[ny][nx]:
                    distances[ny][nx] = nouvelle_distance
                    # On ajoute la case (nx,ny) à la file pour l'explorer plus tard afin d'avoir un chemin plus court
                    heapq.heappush(file_priorite, (nouvelle_distance, (nx, ny)))
                    # On doit enregistrer d’où on vient pour garder la trace de chemin
                    noeuds_precedents[(nx, ny)] = (x, y)

    """ Étape 3 : Reconstruction du chemin"""
    
    #On crée une liste vide 
    chemin = []
    #On initialise le noeud à la case de distinataire
    noeud = fin
    #Boucle qui vérifie si la case noeud existe dans le dictionnaire
    while noeud in noeuds_precedents:
        # On ajoute la case de la fin au chemin
        chemin.append(noeud)
        # On récupère la case précédentes grace au dictionnaire
        noeud = noeuds_precedents[noeud]
        # et la boucle continue
    # On ajoute la case de début pour completer le chemin
    chemin.append(debut)
    # On retourne le chemin dans le bon ordre, du début à la fin
    return chemin[::-1]



