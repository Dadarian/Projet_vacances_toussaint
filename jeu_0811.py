import pygame
import random

# les paramètres du jeu
largeur, hauteur = 400, 400
taille_case = 40
nombre_lignes, nombre_colonnes = largeur // taille_case, hauteur // taille_case
nombre_mines = 20

# les couleurs
noir = (0, 0, 0)
blanc = (255, 255, 255)
gris_fond = (192, 192, 192)
gris_contour = (128, 128, 128)
rouge = (255, 0, 0)
vert = (0, 255, 0) 

pygame.init()

fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Démineur")

def creer_plateau():
    #liste bidimensionnelle 
    plateau = [[0 for _ in range(nombre_colonnes)] for _ in range(nombre_lignes)]
    mines_placees = 0
    while mines_placees < nombre_mines:
        x, y = random.randint(0, nombre_lignes - 1), random.randint(0, nombre_colonnes - 1)
        #vérification si la case pas de mine 
        if plateau[x][y] != -1:
            plateau[x][y] = -1
            mines_placees += 1
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if 0 <= i < nombre_lignes and 0 <= j < nombre_colonnes and plateau[i][j] != -1:
                        plateau[i][j] += 1
    return plateau

def afficher_plateau(plateau, case_revelee):
    #examine chaque case
    for x in range(nombre_lignes):
        for y in range(nombre_colonnes):
            rect = pygame.Rect(y * taille_case, x * taille_case, taille_case, taille_case)
            pygame.draw.rect(fenetre, gris_fond, rect)
            pygame.draw.rect(fenetre, gris_contour, rect, 1)
            if case_revelee[x][y]:
                if plateau[x][y] == -1:
                    pygame.draw.circle(fenetre, rouge, (y * taille_case + taille_case // 2, x * taille_case + taille_case // 2), taille_case // 2)
                elif plateau[x][y] > 0:
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(plateau[x][y]), True, noir)
                    fenetre.blit(text, (y * taille_case + taille_case // 2 - 10, x * taille_case + taille_case // 2 - 10))
                else:
                    pygame.draw.rect(fenetre, vert, rect)

# Fonction principale
def demineur():
    #nouveau plateau
    plateau = creer_plateau()
    case_revelee = [[False for _ in range(nombre_colonnes)] for _ in range(nombre_lignes)]
    en_cours = True
    gagne = False

    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #case cliquée
                x, y = event.pos[1] // taille_case, event.pos[0] // taille_case
                if not case_revelee[x][y]:
                    case_revelee[x][y] = True
                    #jeu se termine	
                    if plateau[x][y] == -1:
                        en_cours = False
                    elif plateau[x][y] == 0:
                        # révèle les cases vides adjacentes
                        a_reveler = [(x, y)]
                        while a_reveler:
                            i, j = a_reveler.pop()
                            for m in range(i - 1, i + 2):
                                for n in range(j - 1, j + 2):
                                    if 0 <= m < nombre_lignes and 0 <= n < nombre_colonnes and not case_revelee[m][n]:
                                        case_revelee[m][n] = True
                                        if plateau[m][n] == 0:
                                            a_reveler.append((m, n))
            #réinitialisation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                plateau = creer_plateau()
                case_revelee = [[False for _ in range(nombre_colonnes)] for _ in range(nombre_lignes)]
                gagne = False

        fenetre.fill(blanc)
        afficher_plateau(plateau, case_revelee)
        #upload affichage
        pygame.display.flip()

        # vérif pour la victoire
        if all(plateau[x][y] == -1 or case_revelee[x][y] for x in range(nombre_lignes) for y in range(nombre_colonnes)):
            gagne = True
            en_cours = False

    fenetre.fill(blanc)
    afficher_plateau(plateau, case_revelee)
    pygame.display.flip()

    if gagne:
        font = pygame.font.Font(None, 36)
        text = font.render("Vous avez gagné !", True, noir)
        fenetre.blit(text, (150, 200))
    else:
        font = pygame.font.Font(None, 36)
        text = font.render("Vous avez perdu.", True, noir)
        fenetre.blit(text, (175, 200))

    pygame.display.flip()

    pygame.time.wait(2000)

    pygame.quit()

# Lancement du jeu
demineur()
