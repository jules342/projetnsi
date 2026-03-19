import pygame, sys, os, random
from spawn_system import apparition_aleatoire
from pokemon_data import RARITY_INFO, TYPE_COLORS

W, H = 800, 500
FPS  = 60
ZONE = "cimetiere"
SPRITE_DIR = os.path.dirname(os.path.abspath(__file__))

NOIR   = (  8,   6,  14)
PANEL  = ( 22,  18,  38)
BORD   = ( 55,  45,  90)
BLANC  = (240, 235, 255)
GRIS   = (100,  90, 130)
VERT   = ( 88, 210,  88)
ORANGE = (220, 200,  50)
ROUGE  = (220,  60,  60)

pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pokémon — Appuie sur R pour reroll")
clock  = pygame.time.Clock()

f_grand  = pygame.font.SysFont("consolas", 22, bold=True)
f_normal = pygame.font.SysFont("consolas", 16)
f_petit  = pygame.font.SysFont("consolas", 13)


def charger_sprite(fichier, taille):
    """Charge un sprite. Retourne un carré violet si fichier manquant."""
    try:
        img = pygame.image.load(os.path.join(SPRITE_DIR, fichier)).convert_alpha()
        return pygame.transform.scale(img, (taille, taille))
    except FileNotFoundError:
        surf = pygame.Surface((taille, taille), pygame.SRCALPHA)
        surf.fill((80, 40, 120, 200))
        return surf


def dessiner_barre(surface, x, y, w, h, val, max_val):
    """Barre de HP colorée selon le pourcentage."""
    pct = val / max_val if max_val > 0 else 0
    pygame.draw.rect(surface, (30, 25, 50), pygame.Rect(x, y, w, h), border_radius=h)
    if pct > 0:
        couleur = VERT if pct > 0.5 else (ORANGE if pct > 0.25 else ROUGE)
        pygame.draw.rect(surface, couleur, pygame.Rect(x, y, int(w * pct), h), border_radius=h)
    pygame.draw.rect(surface, BORD, pygame.Rect(x, y, w, h), 1, border_radius=h)


def afficher_texte(surface, texte, police, couleur, x, y, align="left"):
    """Affiche du texte avec alignement."""
    rendu = police.render(texte, True, couleur)
    if align == "center": x -= rendu.get_width() // 2
    if align == "right":  x -= rendu.get_width()
    surface.blit(rendu, (x, y))


# Génère le premier ennemi au lancement
ennemi = apparition_aleatoire(ZONE, niveau_joueur=15)
sprite = charger_sprite(ennemi["sprite"], 220)

# ── Boucle principale ────────────────────────
running = True
while running:

    # 1. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                # Reroll : génère un nouvel ennemi
                ennemi = apparition_aleatoire(ZONE, niveau_joueur=15)
                sprite = charger_sprite(ennemi["sprite"], 220)

    # 2. Update — rien à mettre à jour ici pour l'instant

    # 3. Draw
    screen.fill(NOIR)

    # Panneau infos ennemi (droite)
    panneau = pygame.Rect(420, 60, 340, 240)
    pygame.draw.rect(screen, PANEL, panneau, border_radius=12)
    pygame.draw.rect(screen, BORD,  panneau, 1, border_radius=12)

    # Barre de couleur rareté en haut du panneau
    couleur_rarete = RARITY_INFO[ennemi["rarete"]]["color"]
    pygame.draw.rect(screen, couleur_rarete, pygame.Rect(420, 60, 340, 4), border_radius=2)

    # Nom + niveau
    afficher_texte(screen, ennemi["nom"],          f_grand,  BLANC, 435, 75)
    afficher_texte(screen, f"Niv. {ennemi['niveau']}", f_normal, GRIS,  740, 78, align="right")

    # Rareté
    label_rarete = RARITY_INFO[ennemi["rarete"]]["label"]
    afficher_texte(screen, label_rarete, f_petit, couleur_rarete, 435, 110)

    # Types
    tx = 435
    for t in ennemi["types"]:
        couleur_type = TYPE_COLORS.get(t, (90, 80, 120))
        surf_t = f_petit.render(t.upper(), True, couleur_type)
        rect_t = pygame.Rect(tx - 4, 132, surf_t.get_width() + 8, surf_t.get_height() + 4)
        pygame.draw.rect(screen, tuple(max(0, c - 60) for c in couleur_type), rect_t, border_radius=3)
        pygame.draw.rect(screen, couleur_type, rect_t, 1, border_radius=3)
        screen.blit(surf_t, (tx, 134))
        tx += rect_t.width + 6

    # Barre HP
    afficher_texte(screen, f"HP  {ennemi['hp']} / {ennemi['hp_max']}", f_normal, GRIS, 435, 168)
    dessiner_barre(screen, 435, 192, 300, 12, ennemi["hp"], ennemi["hp_max"])

    # Barre ATK
    afficher_texte(screen, f"ATK  {ennemi['atk']}", f_normal, GRIS, 435, 220)
    dessiner_barre(screen, 435, 244, 220, 8, ennemi["atk"], 150)

    # Sprite ennemi (gauche)
    screen.blit(sprite, (80, 60))

    # Instruction en bas
    afficher_texte(screen, "[R] Nouvel ennemi    [ECHAP] Quitter",
                   f_petit, GRIS, W // 2, H - 30, align="center")

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
