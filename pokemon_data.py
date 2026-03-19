# pokemon_data.py — Données des Pokémon par zone
# Ce fichier ne contient QUE des données, aucune logique.
# Pour ajouter un Pokémon, on modifie uniquement ce fichier.
# Noms temporaires → cherche "TODO_NOM" pour les remplacer quand tu auras les vrais noms !


# ─────────────────────────────────────────────
#  Couleurs des types
# ─────────────────────────────────────────────

# Dictionnaire qui associe chaque nom de type à une couleur RGB.
# Ces couleurs sont utilisées dans main.py pour afficher les badges de type.
# RGB = (Rouge, Vert, Bleu), chaque valeur entre 0 et 255.
TYPE_COLORS = {
    "Feu":      (240, 120,  70),   # orange chaud
    "Poison":   (196, 160, 210),   # violet clair
    "Spectre":  ( 80,  60, 130),   # violet sombre
    "Ténèbres": ( 60,  40,  80),   # presque noir violacé
    "Plante":   (120, 200, 120),   # vert moyen
    "Roche":    (180, 160, 100),   # beige sableux
    "Sol":      (220, 185, 100),   # ocre
    "Normal":   (168, 168, 120),   # gris verdâtre
    "Eau":      ( 90, 150, 220),   # bleu ciel
    "Électrik": (250, 210,  60),   # jaune vif
    "Vol":      (150, 185, 240),   # bleu pâle
    "Glace":    (130, 210, 230),   # cyan glacé
    "Combat":   (200,  80,  80),   # rouge sombre
    "Dragon":   ( 80,  80, 200),   # bleu indigo
    "Psy":      (240, 100, 160),   # rose fuchsia
    "Acier":    (160, 175, 190),   # gris bleuté
}


# ─────────────────────────────────────────────
#  Infos d'affichage des raretés
# ─────────────────────────────────────────────

# Pour chaque rareté, on stocke son label (texte à afficher) et sa couleur.
# Utilisé dans main.py pour les badges et les textes colorés.
RARITY_INFO = {
    "commun":     {"label": "Commun",     "color": ( 80, 160,  60)},  # vert
    "rare":       {"label": "Rare",       "color": ( 50, 120, 200)},  # bleu
    "legendaire": {"label": "Légendaire", "color": (210, 150,  30)},  # or
}


# ─────────────────────────────────────────────
#  Poids de base des raretés
# ─────────────────────────────────────────────

# Ces poids servent de point de départ dans choisir_rarete() (spawn_system.py).
# La somme fait 100 pour que ce soit lisible comme des pourcentages.
# Mais ce n'est pas obligatoire : random.choices normalise automatiquement.
# Ex : poids [70, 25, 5] → 70/100 = 70% de chances d'avoir "commun".
RARITY_WEIGHTS = {
    "commun":      70,   # 70% de chances de base
    "rare":        25,   # 25% de chances de base
    "legendaire":   5,   #  5% de chances de base
}


# ─────────────────────────────────────────────
#  Base de données des zones et des Pokémon
# ─────────────────────────────────────────────

# ZONES est un dictionnaire imbriqué (dict dans un dict dans un dict).
# Structure : ZONES[nom_zone][rareté] = liste de Pokémon
#
# Chaque Pokémon est un dictionnaire avec ces clés obligatoires :
#   nom        (str)   : nom affiché dans le jeu
#   sprite     (str)   : nom du fichier image (doit être dans le même dossier)
#   types      (list)  : liste de 1 ou 2 types (doit correspondre à TYPE_COLORS)
#   base_level (int)   : niveau minimum naturel (plancher du calcul de niveau)
#   poids      (int)   : fréquence relative d'apparition dans son pool
#   hp_base    (int)   : HP de base avant scaling par le niveau
#   atk_base   (int)   : ATK de base avant scaling par le niveau
ZONES = {

    # ════════════════════════════════════════════
    #  Zone : Cimetière
    # ════════════════════════════════════════════
    "cimetiere": {
        "nom": "Cimetière",

        # bg_color = couleur de fond de l'écran pour cette zone (RGB)
        "bg_color": (25, 20, 35),   # violet très sombre, ambiance nocturne

        # ── Commun (apparaît 70% du temps) ──────
        "commun": [
            {
                "nom":        "Petitombe",       # TODO_NOM — la petite tombe avec flammes
                "sprite":     "petitombe.png",   # fichier image à mettre dans le même dossier
                "types":      ["Spectre", "Feu"],
                "base_level": 5,                 # niveau minimum : ne descend jamais sous 5
                "poids":      60,                # poids dans son pool (seul commun → 100%)
                "hp_base":    45,                # HP avant scaling : ex niveau 20 → ~45+50+var
                "atk_base":   18,
            },
        ],

        # ── Rare (apparaît 25% du temps) ────────
        "rare": [
            {
                "nom":        "Poisitome",       # TODO_NOM — le violet avec bulles vertes
                "sprite":     "poisitome.png",
                "types":      ["Poison", "Spectre"],
                "base_level": 12,
                "poids":      40,                # poids dans son pool (seul rare → 100%)
                "hp_base":    70,
                "atk_base":   35,
            },
        ],

        # ── Légendaire (apparaît 5% du temps) ───
        "legendaire": [
            {
                "nom":        "Tomboss",         # TODO_NOM — le gros boss crâne et flammes
                "sprite":     "tombe.png",
                "types":      ["Spectre", "Feu"],
                "base_level": 40,                # niveau minimum 40 : toujours un gros défi
                "poids":      5,                 # poids dans son pool (seul légendaire → 100%)
                "hp_base":    150,               # beaucoup de HP : c'est le boss
                "atk_base":   90,
            },
        ],
    },

    # ════════════════════════════════════════════
    #  Zones à compléter avec tes prochains sprites
    # ════════════════════════════════════════════

    # Pour ajouter un Pokémon dans une zone vide, copie le bloc ci-dessus
    # et adapte les valeurs. Les listes vides [] font que la zone est ignorée
    # par le système d'apparition jusqu'à ce que tu la remplisses.
    "foret": {
        "nom": "Forêt",
        "bg_color": (20, 50, 20),
        "commun":     [],   # ← ajoute tes sprites ici
        "rare":       [],
        "legendaire": [],
    },
    "grotte": {
        "nom": "Grotte",
        "bg_color": (30, 25, 45),
        "commun":     [],
        "rare":       [],
        "legendaire": [],
    },
    "volcan": {
        "nom": "Volcan",
        "bg_color": (80, 20, 10),
        "commun":     [],
        "rare":       [],
        "legendaire": [],
    },
}
