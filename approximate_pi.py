#!/usr/bin/env python3
"""Module approximate_pi qui prend un entier en paramètre et simule une approximation de Pi"""

import sys
import random

LIST_PTS=[] #Variable Globale qui va stocker les points générés
LIST_PI=[]  #Variable qui stocke la valeur de pi à chaque fois qu'1/10 des points est tiré

def approx_pi(nb_points):
    """Fonction qui simule une approximation de π"""
    # Compteur des points à l'intérieur du cerlce de centre (0,0) et de rayon 1
    cpt=0
    #Si le module n'est le principal
    if __name__!="__main__":
        global LIST_PTS
        global LIST_PI
        dixieme=nb_points//10
        n_dixieme=dixieme
        for i in range(0,nb_points):
            # Génération des coordonnées des points
            absc=random.uniform(-1,1)
            ordo=random.uniform(-1,1)
            # Distance par rapport au centre du cercle
            distance_2=absc*absc+ordo*ordo
            if distance_2<=1:
                cpt+=1
                # 1 pour indiquer que le point appartient au cercle
                LIST_PTS.append((absc,ordo,1))
            else:
                LIST_PTS.append((absc,ordo,0))
            if i==n_dixieme:
                # Si un dixième des pts est généré, on calcul une approx de pi et stock sa valeur
                LIST_PI.append(4*cpt/n_dixieme)
                n_dixieme+=dixieme
        # Stockage de résultat final de l'approx de pi
        LIST_PI.append(4*cpt/nb_points)
    else:
        for i in range(0,nb_points):
            absc=random.uniform(-1,1)
            ordo=random.uniform(-1,1)
            distance_2=absc*absc+ordo*ordo
            if distance_2<=1:
                cpt+=1
    return 4*cpt/nb_points

def main():
    """Fonction de test"""
    # Verification des paramètres
    if len(sys.argv)!=2:
        print("Usage: ./approximate.py entier")
        return
    #Exécution et affichage de l'approximation
    print(approx_pi(int(sys.argv[1])))

# Exécution du main seulement si le module est principal
if __name__=="__main__":
    main()
