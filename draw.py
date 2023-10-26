#!/usr/bin/env python3
"""Module qui a pour but de génere un GIF qui représente """

import copy
import sys
import subprocess

from approximate_pi import LIST_PTS, LIST_PI
import approximate_pi


def generate_ppm_file(nomfichier, list_pixels):
    """Genere une seule image ppm"""
    # Ouverture du fichier en mode écriture
    fichier=open(nomfichier, "w")
    # Les pixels spnt en RGB
    print("P3",file=fichier)
    # écriture de la taille de l'image
    dim=int(sys.argv[1])
    print(dim ,dim,file=fichier)
    # Format Binaire
    print("1",file=fichier)
    # Ecriture de la list contenant les couleurs des pixels
    for ligne in list_pixels:
        print(' '.join(ligne),file=fichier)
    # Fermeture du fichier
    fichier.close()


def vers_pixels(liste_pts,list_pixels):
    """Conversion d'une list de point de coordonnées entre [-1,1] en pixels,
    en leurs attribuant des couleurs"""
    dim=int(sys.argv[1])
    for i in liste_pts:
        # Conversion des points de coordonnées [-1,1] en pixels
        absc=int(((i[0]+1)/2)*dim)
        ordo=int(((i[1]+1)/2)*dim)
        if i[2]==1:         # Vert si point à l'intérieur du cercle
            list_pixels[absc][ordo]="0 1 0"
        else:               # Rouge sinon
            list_pixels[absc][ordo]="1 0 0"
    return list_pixels


def generate_all_files(liste_pts):
    """Genere tous les fichiers ppm (10 en total)"""
    # Liste qui stock les noms des fichiers ppm
    img_list=[]
    dim=int(sys.argv[1])
    # Liste qui va contenir les couleurs des pixels
    list_pixels=[["1 1 1"] * dim for _ in range(dim)]
    # Indice+1 du point du k-1 dixième des points
    slice_prec=0
    # 10 images
    for i in range(10):
        # Indice du dernier points du k-dixième des pts
        slice_curr=((i+1)*int(sys.argv[2]))//10
        # Conversion en pixels colorés d'un dixième des pts
        vers_pixels(liste_pts[slice_prec:slice_curr],list_pixels)
        slice_prec=slice_curr
        # Génération du nom du fichier i
        nom_img=nom_fichier_ppm(i)
        # Ajout du nom à la liste
        img_list.append(nom_img)
        # Ecriture du π courant sur la list de list de pixels
        # Utilisation de deepcopy pour ne pas devoir génerer une list_pixels complète à chaque fois
        list_pixels_ecrit=ecriture_pi(copy.deepcopy(list_pixels),i)
        # Génération du fichier ppm
        generate_ppm_file(nom_img,list_pixels_ecrit)
    return img_list


def nom_fichier_ppm(num_image):
    """Formatage du nom des fichiers ppm"""
    global LIST_PI
    nom_img =f'img{num_image}_'
    pi_str=str(LIST_PI[num_image])
    for i in pi_str:
        if i=='.':
            nom_img+="-"
        else:
            nom_img+=i
    return nom_img+".ppm"


def gif(img_list):
    """Conversion de tous les ppm du rep courant en GIF 'resultat.gif'"""
    str1 = 'convert -delay 100 -loop 0 ' + ' '.join(img_list)  + ' resultat.gif'
    subprocess.call(str1, shell=True)


def exceptions():
    """Raise exception"""
    # Exceptions : Les types ne conviennent pas
    if not isinstance(int(sys.argv[1]), int):
        raise TypeError("La taille : le premier paramètre n'est pas un entier ")
    if not isinstance(int(sys.argv[2]), int):
        raise TypeError("Le nombre de points : le deuxième paramètre n'est pas un entier ")
    if not isinstance(int(sys.argv[3]), int):
        raise TypeError("Le troisième paramètre n'est pas un entier ")
    # Exceptions : Les valeurs ne conviennent pas
    if int(sys.argv[1])<100:
        raise ValueError("Le 1er paramètre qui represente la taille de l'image est inférieur à 100")
    if int(sys.argv[2])<=100:
        raise ValueError("Le 2ème paramètre qui represente le nombre de points est inférieur à 100")
    if int(sys.argv[3])<1 or int(sys.argv[3])>5:
        raise ValueError("Le 3ème paramètre n'est pas entre 1 et 5")


def line_horiz(absc,y_debut,y_fin,list_pixels):
    """Dessine une ligne horizentale sur list_pixels passée en paramètre"""
    # Epaisseur de la ligne selon la taille de l'image si la taille est assez grande, 0 sinon
    epaisseur = int(sys.argv[1])//250 if int(sys.argv[1])>500 else 0
    for ordo in range(y_debut,y_fin):
        for ep in range(absc-(epaisseur//2),absc+(epaisseur//2)+1):
            # En noir
            list_pixels[ep][ordo]="0 0 0"
    return list_pixels


def line_verti(ordo,x_debut,x_fin,list_pixels):
    """Dessine une ligne horizentale sur list_pixels passée en paramètre"""
    # Epaisseur de la ligne selon la taille de l'image si la taille est assez grande, 0 sinon
    epaisseur = int(sys.argv[1])//250 if int(sys.argv[1])>500 else 0
    for absc in range(x_debut,x_fin):
        for ep in range(ordo-(epaisseur//2), ordo+(epaisseur//2)+1):
            # En noir
            list_pixels[absc][ep]="0 0 0"
    return list_pixels


def ecriture_pi(list_pixels,num_img):
    """Fonction qui écrit la valeur de pi en changeant les valeurs des pixels
    sur la list de list en paramètre"""
    dim=int(sys.argv[1])
    # Coordonnées qui délimitent la partie "centrale" de la list de list de pixels, calculer
    # En fonction de la taille de l'image
    haut=(dim//9)*4
    bas=(dim//9)*5
    gauche=(dim//7)*2
    droite=(dim//7)*5
    # Nombre à écrire et sa taille
    pi_str=str(LIST_PI[num_img])
    taille_pi=len(pi_str)
    # Espace pour chaque chiffre de π
    espace_chiffre=(droite-gauche)//taille_pi
    # Ecriture des chiffres par traitement conditionel
    for charac in pi_str:
        # int(espace_chiffre*0.8) histoire de s'éloigner du chiffre qui suit
        if charac=='1':
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
        elif charac=='2':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche,haut+(bas-haut)//2, bas,list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut,haut+(bas-haut)//2,list_pixels)
        elif charac=='3':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
        elif charac=='4':
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
            line_verti(gauche,haut,haut+(bas-haut)//2,list_pixels)
        elif charac=='5':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche,haut, haut+(bas-haut)//2,list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut+(bas-haut)//2,bas,list_pixels)
        elif charac=='6':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche,haut, haut+(bas-haut)//2,list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut+(bas-haut)//2,bas,list_pixels)
            line_verti(gauche,haut+(bas-haut)//2, bas,list_pixels)
        elif charac=='7':
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
        elif charac=='8':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche,haut, bas,list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
        elif charac=='9':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(haut+(bas-haut)//2,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche,haut,haut+(bas-haut)//2,list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
        elif charac=='0':
            line_horiz(haut,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_horiz(bas,gauche,gauche+int((espace_chiffre)*0.8),list_pixels)
            line_verti(gauche,haut, bas,list_pixels)
            line_verti(gauche+int((espace_chiffre)*0.8),haut,bas,list_pixels)
        elif charac=='.':
            if dim<200:
                # si l'image est assez petite, le point n'occupe qu'un seul pixel
                list_pixels[bas][gauche]="0 0 0"
            else:
                for absc in range(bas-int(espace_chiffre*0.2),bas):
                    for ordo in range(gauche + int(espace_chiffre*0.2), gauche+2*int(espace_chiffre*0.2)):
                        list_pixels[absc][ordo]="0 0 0"
        gauche+=espace_chiffre
    return list_pixels


def main():
    """Fonction de test"""
    # Message si il n'y a pas 4 arguments dans la commande d'éxécution
    if len(sys.argv)!=4:
        print("Usage: ./draw.py image_dimension>=100     points>100     1<=decimal_format<=5")
        return
    # Lancement des exceptions
    exceptions()
    global LIST_PI
    # Execution de l'approximation par Montre Carlo
    approximate_pi.approx_pi(int(sys.argv[2]))
    # Formatage des nombres π pour avoir le nombre de chiffre après la virgule passé en argument
    for i in range(10):
        LIST_PI[i]=f'{{:.{sys.argv[3]}f}}'.format(LIST_PI[i])
    #Genère les images ppm
    list_img=generate_all_files(LIST_PTS)
    #Gènere le GIF
    gif(list_img)

# Exécution du main seulement si le module est principal
if __name__=="__main__":
    main()
