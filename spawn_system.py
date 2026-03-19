# spawn_system.py — Système d'apparition aléatoire des Pokémon
# Auteur : ton nom ici
# NSI Terminale — Projet Pokémon

# "random" est un module Python intégré qui gère tout ce qui est aléatoire.
# On s'en sert pour les tirages pondérés, les variances de niveau, etc.
import random

# On importe uniquement ce dont on a besoin depuis pokemon_data.py.
# ZONES contient tous les Pokémon organisés par zone et rareté.
# RARITY_WEIGHTS contient les probabilités de base commun/rare/légendaire.
from pokemon_data import ZONES, RARITY_WEIGHTS


# ─────────────────────────────────────────────
#  Fonctions utilitaires
# ─────────────────────────────────────────────

# "elements: list" et "cle_poids: str" sont des annotations de type.
# Elles ne forcent rien, elles servent juste à documenter ce qu'on attend.
# "-> dict" indique que la fonction retourne un dictionnaire.
def tirage_pondere(elements: list, cle_poids: str) -> dict:
    """
    Effectue un tirage aléatoire pondéré dans une liste de dicts.
    Un élément avec poids 60 a 3× plus de chances qu'un élément avec poids 20.

    Exemple :
        pool = [{"nom": "A", "poids": 70}, {"nom": "B", "poids": 30}]
        tirage_pondere(pool, "poids")  →  "A" 70% du temps
    """
    # Liste en compréhension : raccourci pour construire une liste.
    # Pour chaque élément du pool, on récupère sa valeur de poids.
    # Ex : si cle_poids = "poids", on obtient [60, 40, 5] pour nos 3 Pokémon.
    poids_totaux = [elem[cle_poids] for elem in elements]

    # random.choices() tire au sort en tenant compte des poids.
    # k=1 signifie "tire 1 seul élément".
    # Elle retourne TOUJOURS une liste, donc [0] extrait le premier élément.
    return random.choices(elements, weights=poids_totaux, k=1)[0]


def choisir_rarete(niveau_joueur: int) -> str:
    """
    Tire une rareté (commun / rare / légendaire) de façon pondérée.
    Le niveau du joueur booste progressivement les rares.

    Paramètre :
        niveau_joueur (int) : niveau actuel du joueur (1-100)

    Retourne :
        str : "commun", "rare" ou "legendaire"
    """
    # .copy() crée une copie du dictionnaire original.
    # SANS .copy(), on modifierait RARITY_WEIGHTS directement et les
    # probabilités changeraient définitivement après le premier appel.
    poids = RARITY_WEIGHTS.copy()

    # // est la division entière : 25 // 10 = 2, pas 2.5.
    # On obtient le nombre de "paliers de 10 niveaux" atteints.
    # min(..., 15) plafonne le bonus à +15, peu importe le niveau.
    bonus_rare = min(niveau_joueur // 10, 15)

    # On ajoute le bonus aux rares et on le retire des communs,
    # pour que la somme totale des poids reste stable.
    poids["rare"]   += bonus_rare
    poids["commun"] -= bonus_rare

    # random.choices attend des listes, pas un dictionnaire.
    # .keys() donne ["commun", "rare", "legendaire"]
    # .values() donne les poids correspondants [68, 27, 5] par exemple
    raretés = list(poids.keys())
    weights = list(poids.values())

    # Même principe que tirage_pondere : tirage au sort pondéré, k=1, [0] pour extraire.
    return random.choices(raretés, weights=weights, k=1)[0]


def calculer_niveau_pokemon(base_level: int, niveau_joueur: int) -> int:
    """
    Calcule le niveau du Pokémon adverse selon le niveau du joueur.
    Formule : 80% du niveau joueur + variance aléatoire, plancher = base_level.

    Paramètres :
        base_level    (int) : niveau minimum naturel du Pokémon
        niveau_joueur (int) : niveau actuel du joueur

    Retourne :
        int : niveau final du Pokémon (entre base_level et 100)
    """
    # randint(-3, 5) tire un entier entre -3 et 5 inclus.
    # Asymétrique exprès : le Pokémon peut être un peu plus fort (+5)
    # que plus faible (-3), ce qui rend les combats plus challengeants.
    variance = random.randint(-3, 5)

    # int() arrondit à l'entier inférieur car la multiplication donne un float.
    # Ex : 25 * 0.8 = 20.0 → int(20.0) = 20
    scaling  = int(niveau_joueur * 0.8)

    # max() garantit que le niveau ne descend jamais sous base_level.
    # Ex : Tomboss a base_level=40, donc même contre un joueur niveau 1,
    # il apparaîtra au moins niveau 40.
    niveau   = max(base_level, scaling + variance)

    # min() garantit qu'on ne dépasse jamais le niveau maximum du jeu.
    return min(niveau, 100)


def calculer_stats(poke_data: dict, niveau: int) -> dict:
    """
    Calcule les stats finales (HP, Attaque) à partir des stats de base et du niveau.

    Paramètres :
        poke_data (dict) : données brutes du Pokémon (hp_base, atk_base…)
        niveau    (int)  : niveau calculé du Pokémon

    Retourne :
        dict : {"hp": int, "atk": int}
    """
    # Formule de scaling : plus le niveau est élevé, plus les stats sont hautes.
    # 2.5 et 1.2 sont des coefficients de game design : tu peux les ajuster
    # pour rendre les ennemis plus ou moins coriaces.
    # random.randint ajoute une légère variance pour éviter des stats identiques.
    # int() arrondit le résultat final à l'entier inférieur.
    hp  = int(poke_data["hp_base"]  + niveau * 2.5 + random.randint(-5, 10))
    atk = int(poke_data["atk_base"] + niveau * 1.2 + random.randint(-3,  8))

    # max(1, ...) garantit qu'un Pokémon a toujours au moins 1 HP et 1 ATK.
    # Sans ça, une variance très négative pourrait donner 0 ou négatif.
    return {"hp": max(1, hp), "atk": max(1, atk)}


# ─────────────────────────────────────────────
#  Fonction principale
# ─────────────────────────────────────────────

def apparition_aleatoire(zone: str, niveau_joueur: int) -> dict:
    """
    Génère un Pokémon adverse aléatoire adapté à la zone et au niveau du joueur.
    C'est le point d'entrée principal : les autres fichiers n'appellent que celle-ci.

    Paramètres :
        zone          (str) : clé de zone ("cimetiere", "foret", etc.)
        niveau_joueur (int) : niveau actuel du joueur (1-100)

    Retourne :
        dict avec les clés :
            nom      (str)  : nom du Pokémon
            types    (list) : liste des types
            rarete   (str)  : "commun" | "rare" | "legendaire"
            niveau   (int)  : niveau du Pokémon généré
            hp       (int)  : points de vie
            atk      (int)  : stat d'attaque
            hp_max   (int)  : HP maximum (= hp à la création)
            sprite   (str)  : nom du fichier image

    Lève :
        ValueError si la zone n'existe pas dans ZONES
    """
    # "not in" vérifie si la clé n'est PAS dans le dictionnaire.
    # raise ValueError déclenche volontairement une erreur avec un message clair,
    # plutôt que de laisser le programme planter mystérieusement plus loin.
    if zone not in ZONES:
        raise ValueError(f"Zone inconnue : '{zone}'. Zones disponibles : {list(ZONES.keys())}")

    # ── Étape 1 : choisir la rareté ──────────────────────────────────────
    # On appelle choisir_rarete() qui retourne "commun", "rare" ou "legendaire".
    rarete = choisir_rarete(niveau_joueur)

    # ── Étape 2 : filtrer le pool ─────────────────────────────────────────
    # Deux accès de dictionnaire en chaîne :
    # ZONES["cimetiere"] donne la zone entière,
    # puis ["commun"] (ou "rare"/"legendaire") donne la liste des Pokémon de cette rareté.
    pool = ZONES[zone][rarete]

    # ── Étape 3 : tirer un Pokémon dans le pool ───────────────────────────
    # tirage_pondere() choisit un Pokémon au hasard, en tenant compte de
    # son champ "poids" : un Pokémon avec poids 60 sort bien plus souvent
    # qu'un Pokémon avec poids 5.
    poke_data = tirage_pondere(pool, "poids")

    # ── Étape 4 : calculer le niveau et les stats ─────────────────────────
    # On passe base_level du Pokémon ET le niveau du joueur pour le scaling.
    niveau = calculer_niveau_pokemon(poke_data["base_level"], niveau_joueur)
    # On passe ensuite le niveau final pour calculer HP et ATK.
    stats  = calculer_stats(poke_data, niveau)

    # ── Étape 5 : assembler et retourner le dict complet ──────────────────
    # Ce dictionnaire est ce que reçoit main.py pour afficher le Pokémon.
    # "hp_max" est séparé de "hp" car pendant le combat, "hp" va diminuer
    # mais "hp_max" reste fixe (pour calculer le % de la barre de vie).
    # .get("sprite", "") est plus sûr que poke_data["sprite"] :
    # si la clé "sprite" n'existe pas, on retourne "" au lieu de planter.
    return {
        "nom":    poke_data["nom"],
        "types":  poke_data["types"],
        "rarete": rarete,
        "niveau": niveau,
        "hp":     stats["hp"],
        "hp_max": stats["hp"],
        "atk":    stats["atk"],
        "sprite": poke_data.get("sprite", ""),
    }


# ─────────────────────────────────────────────
#  Test rapide en ligne de commande
# ─────────────────────────────────────────────

# __name__ est une variable spéciale de Python.
# Quand on lance CE fichier directement (python spawn_system.py),
# Python lui donne la valeur "__main__".
# Quand un autre fichier l'importe (from spawn_system import ...),
# __name__ vaut "spawn_system" et ce bloc est ignoré.
# C'est le moyen standard d'écrire des tests dans un module.
if __name__ == "__main__":
    print("=== Test du système d'apparition ===\n")

    # On teste uniquement les zones qui ont des Pokémon déclarés.
    # any() retourne True si au moins un élément de la séquence est vrai (non vide).
    zones_actives = [z for z, data in ZONES.items()
                     if any(data[r] for r in ("commun", "rare", "legendaire"))]

    for zone in zones_actives:
        print(f"Zone : {zone.upper()}")
        # On génère 5 Pokémon pour voir la variété des tirages.
        for _ in range(5):
            # _ est une convention Python pour "je n'utilise pas cette variable".
            p = apparition_aleatoire(zone, niveau_joueur=25)
            # :12s  = chaîne alignée sur 12 caractères (pour l'affichage en colonnes)
            # :3d   = entier aligné sur 3 chiffres
            # :4d   = entier aligné sur 4 chiffres
            print(f"  {p['nom']:14s} | niv.{p['niveau']:3d} | {p['rarete']:10s} | HP:{p['hp']:4d} ATK:{p['atk']:3d} | {p['sprite']}")
        print()
