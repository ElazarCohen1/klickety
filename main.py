# Imports ---------------------------------------------------------------------
from tkinter import Tk, ttk, Frame, Button, BOTH, Canvas, TOP, BOTTOM, ALL
import tkinter.font
import random

COULEURS = ["red", "blue", "green", "yellow", "magenta"]


def initialiser_plateau(largeur, hauteur):
    """Renvoie un plateau largeur x hauteur aléatoire de blocs de couleurs.
    Les couleurs sont des chaînes tirées dans la liste COULEURS. """
    array = []
    for i in range(largeur): 
        nv_lst = []
        for j in range(hauteur): 
            nv_lst.append(random.choice(COULEURS))
        array.append(nv_lst)
    return array 



def voisins(plateau, col, ligne):
    """Renvoie la liste des voisins du bloc (col, ligne) de la même
    couleur que lui. On considère qu'une case vide n'a aucun voisin"""
    voisin_base = [(col-1,ligne),(col,ligne-1),(col+1,ligne),(col,ligne+1)]
    voisin = []
    try:   
        for tuple in voisin_base: 
            if tuple[0]>=0 and tuple[1] >=0 and plateau[col][ligne] == plateau[tuple[0]][tuple[1]]  : 
                voisin.append(tuple)
    except: 
        return voisin 
    return voisin


def bloc_isole(plateau, col, ligne):
    """Renvoie True si la case (col, ligne) du plateau est vide ou ne
    possède aucun voisin de la même couleur."""
    voisin = voisins(plateau,col,ligne)
    if len(voisin) >=1: 
        return False
    return True  


def supprimer_piece(plateau, col, ligne):
    """Affecte à None chaque case de plateau appartenant à la même pièce que
    le bloc (col, ligne), et renvoie le nombre de blocs effacés."""
    if plateau[col][ligne] == None: 
        return 0
    n = 1
    voisin = voisins(plateau,col,ligne)

    plateau[col][ligne] = None
    
    for col1,ligne1 in voisin:        
        n+= supprimer_piece(plateau,col1,ligne1)

    return n 

def tasser_blocs(plateau):
    """Modifie plateau de manière à ce que les trous (case de couleur None) 
    fassent chuter les autres blocs.
    si celui d'en dessous est none on le decale avec celui d'en dessous et on refait la fonction 
     condition d'arret: si celui d'apres est rempli ou inferieur a 0
      sinon: on echange les deux et on refait la fonction sur la case d'apres   """
    for i in range(len(plateau)):
        for j in range(len(plateau[i])-1): 
            if plateau[i][j] is not None and plateau[i][j+1] is  None:
                plateau[i][j], plateau[i][j+1] = plateau[i][j+1], plateau[i][j]
                tasser_blocs(plateau)

def tasser_colonnes(plateau):
    """Modifie plateau de manière à ce que les colonnes non vides soient tassées
    du côté gauche.
    """
    for i in range(len(plateau)-1): 
        for j in range(len(plateau[i])): 
            if plateau[i][j] is  None and plateau[i+1][j] is not None: 
                plateau[i][j], plateau[i+1][j] = plateau[i+1][j], plateau[i][j]
                tasser_blocs(plateau)

def partie_finie(plateau):
    """Renvoie True si la partie est finie, c'est-à-dire si le plateau est vide
    ou si les seules pièces restantes sont de taille 1, et False sinon."""
    for i in range(len(plateau)): 
        for j in range(len(plateau[i])):  
            if plateau[i][j] is not  None and not bloc_isole(plateau, i, j):  
                return False
    return True

# =============================================================================
# PARTIE À NE PAS MODIFIER ====================================================
# =============================================================================


class KlicketyGUI:
    """Interface pour le jeu Klickety."""

    def __init__(self):
        # initialisation des structures de données ----------------------------
        self.nb_colonnes = 10
        self.nb_lignes = 16
        self.cote_case = 32  # la longueur du côté d'un bloc à dessiner
        self.largeur_plateau = self.cote_case * self.nb_colonnes
        self.hauteur_plateau = self.cote_case * self.nb_lignes
        self.plateau = []
        self.couleur_fond = "black"

        # initialisation des éléments graphiques ------------------------------
        self.window = Tk()  # la fenêtre principale
        self.window.resizable(0, 0)  # empêcher les redimensionnements
        self.partie_haut = Frame(
            self.window, width=self.largeur_plateau,
            height=self.hauteur_plateau
        )
        self.partie_haut.pack(side=TOP)
        self.partie_bas = Frame(self.window)
        self.partie_bas.pack(side=BOTTOM)

        # le canevas affichant le plateau de jeu
        self.plateau_affiche = Canvas(self.partie_haut,
                                      width=self.largeur_plateau,
                                      height=self.hauteur_plateau)
        self.plateau_affiche.pack()
        self.plateau_affiche.bind('<ButtonPress-1>', self.clic_plateau)
    
        # le bouton "Réinitialiser"
        self.btn = Button(self.partie_bas, text='reinitialiser',
                          command=self.reinitialiser_jeu)
        self.btn.pack(fill=BOTH)

        # affichage du nombre de blocs restants
        self.nb_blocs = self.nb_colonnes * self.nb_lignes
        self.nb_blocs_affiche = ttk.Label(
            self.partie_bas,
            text='Blocs restants: {}'.format(self.nb_blocs))
        self.nb_blocs_affiche.pack(fill=BOTH)

        self.reinitialiser_jeu()
        self.window.title('Klickety')
        self.window.mainloop()

    def rafraichir_nombre_blocs(self, nb=0):
        """Rafraîchit l'affichage du nombre de blocs restants."""
        self.nb_blocs -= nb
        chaine = 'Blocs restants: {}'.format(self.nb_blocs)
        self.nb_blocs_affiche['text'] = chaine

    def rafraichir_plateau(self):   
        """Redessine le plateau de jeu à afficher."""
        self.plateau_affiche.delete(ALL)

        for x in range(self.nb_colonnes):
            for y in range(self.nb_lignes):
                couleur = self.plateau[x][y]
                xc, yc = x * self.cote_case, y * self.cote_case
                if couleur is None:
                    couleur = self.couleur_fond
                # remplissage du bloc
                self.plateau_affiche.create_rectangle(
                    xc, yc, xc + self.cote_case, yc + self.cote_case,
                    outline=couleur, fill=couleur)
        for x in range(self.nb_colonnes):
            for y in range(self.nb_lignes):
                xc, yc = x * self.cote_case, y * self.cote_case
                # séparation avec bloc de gauche
                if x > 0 and self.plateau[x - 1][y] != self.plateau[x][y]:
                    self.plateau_affiche.create_line(
                        xc, yc, xc, yc + self.cote_case,
                        fill=self.couleur_fond,
                        width=2, capstyle='projecting')
                # séparation avec bloc du haut
                if y > 0 and self.plateau[x][y - 1] != self.plateau[x][y]:
                    self.plateau_affiche.create_line(
                        xc, yc, xc + self.cote_case, yc,
                        fill=self.couleur_fond,
                        width=2, capstyle='projecting')

    def clic_plateau(self, event):
        """Récupère les coordonnées de la case sélectionnée, et joue le coup
        correspondant s'il est permis."""
        (x, y) = (event.x // self.cote_case, event.y // self.cote_case)
        if self.plateau[x][y] is None or bloc_isole(self.plateau, x, y):
            return

        # supprimer la pièce et tasser le plateau
        nb = supprimer_piece(self.plateau, x, y)
        tasser_blocs(self.plateau)
        tasser_colonnes(self.plateau)

        # rafraîchir le plateau pour répercuter les modifications
        self.rafraichir_plateau()
        self.rafraichir_nombre_blocs(nb)

        # détecter la fin de partie
        if partie_finie(self.plateau):
            self.plateau_affiche.create_text(
                int(self.plateau_affiche.cget("width")) // 2,
                self.cote_case // 2,
                text="LA PARTIE EST TERMINÉE",
                font=tkinter.font.Font(
                    family="Courier", size=12, weight=tkinter.font.BOLD
                ),
                fill="red"
            )

    def reinitialiser_jeu(self):
        """Réinitialise le plateau de jeu et les scores."""
        self.reinitialiser_plateau()
        self.rafraichir_nombre_blocs()

    def reinitialiser_plateau(self):
        """Réinitialise le plateau de jeu."""
        self.plateau = initialiser_plateau(self.nb_colonnes, self.nb_lignes)
        self.plateau_affiche.delete(ALL)
        if self.plateau is not None:
            self.rafraichir_plateau()


if __name__ == "__main__":
    """plateau = initialiser_plateau(5,5)
    for i in plateau:
        print(i)
    print(voisins(plateau,3,2))"""
    KlicketyGUI()
    