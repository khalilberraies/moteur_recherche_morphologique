# -*- coding: utf-8 -*-
import flet as ft
from src.arbre_abr import ArbreAVL
from src.table_hachage import TableHachage
from src.moteur import MoteurMorphologique

def main(page: ft.Page):
    # Configuration de la page
    page.title = "🎯 MOTEUR MORPHOLOGIQUE ARABE"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    
    # Initialiser les structures de données
    arbre = ArbreAVL()
    table = TableHachage()
    moteur = MoteurMorphologique()
    moteur.initialiser(arbre, table)
    
    # Variables pour l'interface
    resultats = ft.Column(scroll=ft.ScrollMode.AUTO)
    racines_liste = ft.Column(spacing=5, scroll=ft.ScrollMode.AUTO)
    
    # Variables pour stocker les entrées
    nouvelle_racine_input = ft.Ref[ft.TextField]()
    racine_gen_input = ft.Ref[ft.TextField]()
    scheme_gen_input = ft.Ref[ft.TextField]()
    mot_val_input = ft.Ref[ft.TextField]()
    racine_val_input = ft.Ref[ft.TextField]()
    racine_tous_input = ft.Ref[ft.TextField]()
    mot_trouver_input = ft.Ref[ft.TextField]()
    
    # ============ FONCTIONS UTILITAIRES ============
    
    def vider_resultats():
        """Vide la zone des résultats"""
        resultats.controls.clear()
        page.update()
    
    def ajouter_resultat_simple(message, type_msg="info"):
        """Ajoute un message aux résultats (remplace l'historique)"""
        vider_resultats()  # Vide d'abord les anciens résultats
        
        couleurs = {
            "success": ft.colors.GREEN,
            "error": ft.colors.RED,
            "warning": ft.colors.ORANGE,
            "info": ft.colors.BLUE
        }
        
        icones = {
            "success": "✅",
            "error": "❌", 
            "warning": "⚠️",
            "info": "📝"
        }
        
        resultats.controls.append(
            ft.Row([
                ft.Text(icones.get(type_msg, "📝"), size=16),
                ft.Text(message, color=couleurs.get(type_msg, ft.colors.BLACK), size=14)
            ])
        )
        page.update()
    
    def charger_donnees():
        """Charge les données depuis les fichiers"""
        try:
            arbre.charger_depuis_fichier("data/racines.txt")
            table.charger_depuis_fichier("data/schemes.txt")
            ajouter_resultat_simple("✅ Données chargées avec succès", "success")
            afficher_racines()
        except Exception as e:
            ajouter_resultat_simple(f"❌ Erreur: {str(e)}", "error")
    
    def afficher_racines():
        """Affiche la liste des racines"""
        racines_liste.controls.clear()
        
        racines_trouvees = []
        
        def collecter_racines(noeud):
            if noeud:
                collecter_racines(noeud.gauche)
                racines_trouvees.append(noeud)
                collecter_racines(noeud.droite)
        
        collecter_racines(arbre.racine)
        
        if not racines_trouvees:
            racines_liste.controls.append(
                ft.Text("Aucune racine disponible", color=ft.colors.GREY)
            )
        else:
            # Trier par ordre alphabétique
            racines_trouvees.sort(key=lambda x: x.racine)
            
            for noeud in racines_trouvees:
                # Crée un élément avec boutons d'action pour chaque racine
                item = ft.Container(
                    content=ft.Row([
                        ft.Text(noeud.racine, size=16, weight=ft.FontWeight.BOLD, width=100),
                        ft.Text(f"({len(noeud.derivees)} dérivés)", 
                               color=ft.colors.GREY_600, size=12, width=100),
                        ft.IconButton(
                            icon=ft.icons.REMOVE_RED_EYE,
                            on_click=lambda e, r=noeud.racine: afficher_details(r),
                            height=30,
                            width=40,
                            icon_color=ft.colors.BLUE,
                            tooltip="Voir détails"
                        ),
                        ft.IconButton(
                            icon=ft.icons.PLAY_ARROW,
                            on_click=lambda e, r=noeud.racine: generer_tous_action_auto(r),
                            height=30,
                            width=40,
                            icon_color=ft.colors.ORANGE,
                            tooltip="Générer tous les dérivés"
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, r=noeud.racine: demander_suppression(r),
                            height=30,
                            width=40,
                            icon_color=ft.colors.RED,
                            tooltip="Supprimer cette racine"
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.symmetric(5, 10),
                    bgcolor=ft.colors.BLUE_50,
                    border_radius=5,
                    margin=ft.margin.only(bottom=5)
                )
                racines_liste.controls.append(item)
        
        # Ajouter un compteur
        if racines_trouvees:
            racines_liste.controls.append(
                ft.Text(f"Total: {len(racines_trouvees)} racine(s)", 
                       color=ft.colors.GREY, size=12, italic=True)
            )
        
        page.update()
    
    def demander_suppression(racine):
        """Demande confirmation avant suppression"""
        def confirmer_suppression(e):
            # Supprimer la racine de l'arbre AVL
            arbre.racine = arbre.supprimer(arbre.racine, racine)
            
            # Mettre à jour l'interface
            ajouter_resultat_simple(f"✅ Racine '{racine}' supprimée avec succès", "success")
            afficher_racines()
            
            page.dialog.open = False
            page.update()
        
        def annuler_suppression(e):
            page.dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmation de suppression"),
            content=ft.Text(f"Voulez-vous vraiment supprimer la racine '{racine}' ?\n\n"
                           f"⚠️ Attention : Tous les dérivés seront également supprimés."),
            actions=[
                ft.TextButton("Annuler", on_click=annuler_suppression),
                ft.ElevatedButton("Supprimer", on_click=confirmer_suppression, 
                                bgcolor=ft.colors.RED, color=ft.colors.WHITE)
            ]
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def afficher_details(racine):
        """Affiche les détails d'une racine"""
        noeud = arbre.rechercher(arbre.racine, racine)
        if not noeud:
            ajouter_resultat_simple(f"❌ Racine '{racine}' non trouvée", "error")
            return
        
        # Crée une boîte de dialogue avec défilement
        contenu = ft.Column([
            ft.Text(f"Détails de la racine: {racine}", 
                   size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            ft.Text(f"Nombre de dérivés: {len(noeud.derivees)}", size=14),
        ])
        
        # Ajoute la liste des dérivés avec défilement
        if noeud.derivees:
            contenu.controls.append(ft.Text("Dérivés:", size=14, weight=ft.FontWeight.BOLD))
            
            derivees_liste = ft.Column(scroll=ft.ScrollMode.AUTO, height=200)
            for i, mot in enumerate(noeud.derivees, 1):
                derivees_liste.controls.append(
                    ft.Row([
                        ft.Text(f"{i}. {mot}", size=12, width=200),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, m=mot, r=racine: supprimer_derive_action(m, r),
                            height=25,
                            width=30,
                            icon_color=ft.colors.RED
                        )
                    ])
                )
            
            contenu.controls.append(
                ft.Container(
                    content=derivees_liste,
                    border=ft.border.all(1, ft.colors.GREY_200),
                    padding=10,
                    border_radius=5
                )
            )
        else:
            contenu.controls.append(ft.Text("Aucun dérivé généré", color=ft.colors.GREY))
        
        # Bouton pour générer tous les dérivés
        contenu.controls.append(
            ft.ElevatedButton(
                "🚀 Générer tous les dérivés",
                on_click=lambda e, r=racine: generer_tous_action_auto(r),
                bgcolor=ft.colors.ORANGE,
                color=ft.colors.WHITE
            )
        )
        
        contenu.controls.append(
            ft.ElevatedButton("Fermer", on_click=lambda e: fermer_dialog(e))
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Détails de la racine"),
            content=contenu,
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def fermer_dialog(e):
            page.dialog.open = False
            page.update()
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def supprimer_derive_action(mot, racine):
        """Supprime un dérivé d'une racine"""
        noeud = arbre.rechercher(arbre.racine, racine)
        if not noeud:
            return
        
        if mot in noeud.derivees:
            noeud.derivees.remove(mot)
            # Supprimer de l'index inverse aussi
            if mot in arbre.index_inverse:
                del arbre.index_inverse[mot]
            
            ajouter_resultat_simple(f"✅ Dérivé '{mot}' supprimé de la racine '{racine}'", "success")
            afficher_racines()
            # Fermer et rouvrir le dialogue pour mettre à jour
            page.dialog.open = False
            afficher_details(racine)
    
    def generer_tous_action_auto(racine):
        """Génère tous les dérivés pour une racine (sans champ de saisie)"""
        if not racine:
            ajouter_resultat_simple("❌ Veuillez entrer une racine", "error")
            return
        
        noeud = arbre.rechercher(arbre.racine, racine)
        if not noeud:
            ajouter_resultat_simple(f"❌ Racine '{racine}' non trouvée", "error")
            return
        
        ajouter_resultat_simple(f"🔨 Génération des dérivés pour '{racine}'...", "info")
        
        mots_generes = []
        for i in range(table.taille):
            entree = table.table[i]
            while entree:
                mot = moteur.generer_mot(racine, entree.cle)
                if mot and mot not in mots_generes:
                    mots_generes.append(mot)
                entree = entree.suivant
        
        ajouter_resultat_simple(f"✅ {len(mots_generes)} dérivé(s) généré(s) pour '{racine}'", "success")
        afficher_racines()
        page.update()
    
    # ============ FONCTIONS PRINCIPALES ============
    
    def on_charger_click(e):
        """Gestionnaire pour le bouton Charger"""
        charger_donnees()
    
    def on_exporter_click(e):
        """Gestionnaire pour le bouton Exporter"""
        try:
            # Exporter les racines
            with open("data/racines_export.txt", "w", encoding="utf-8") as f:
                def exporter_racines(noeud):
                    if noeud:
                        exporter_racines(noeud.gauche)
                        f.write(f"{noeud.racine}\n")
                        exporter_racines(noeud.droite)
                
                exporter_racines(arbre.racine)
            
            # Exporter les dérivés
            with open("data/derives_export.txt", "w", encoding="utf-8") as f:
                def exporter_derives(noeud):
                    if noeud:
                        exporter_derives(noeud.gauche)
                        if noeud.derivees:
                            for mot in noeud.derivees:
                                f.write(f"{mot}|{noeud.racine}\n")
                        exporter_derives(noeud.droite)
                
                exporter_derives(arbre.racine)
            
            ajouter_resultat_simple("✅ Données exportées avec succès", "success")
        except Exception as e:
            ajouter_resultat_simple(f"❌ Erreur lors de l'export: {str(e)}", "error")
    
    def on_ajouter_racine_click(e):
        """Gestionnaire pour ajouter une racine"""
        racine = nouvelle_racine_input.current.value.strip()
        
        if len(racine) < 3:
            ajouter_resultat_simple("❌ Une racine doit avoir au moins 3 caractères", "error")
            return
        
        arbre.racine = arbre.inserer(arbre.racine, racine)
        ajouter_resultat_simple(f"✅ Racine '{racine}' ajoutée", "success")
        nouvelle_racine_input.current.value = ""
        afficher_racines()
        page.update()
    
    def on_generer_mot_click(e):
        """Gestionnaire pour générer un mot"""
        racine = racine_gen_input.current.value.strip()
        scheme = scheme_gen_input.current.value.strip()
        
        if not racine or not scheme:
            ajouter_resultat_simple("❌ Veuillez remplir tous les champs", "error")
            return
        
        mot = moteur.generer_mot(racine, scheme)
        if mot:
            ajouter_resultat_simple(f"✅ Mot généré: {mot}", "success")
            racine_gen_input.current.value = ""
            afficher_racines()
        page.update()
    
    def on_valider_mot_click(e):
        """Gestionnaire pour valider un mot"""
        mot = mot_val_input.current.value.strip()
        racine = racine_val_input.current.value.strip()
        
        if not mot or not racine:
            ajouter_resultat_simple("❌ Veuillez remplir tous les champs", "error")
            return
        
        valide, scheme = moteur.valider_mot(mot, racine)
        
        if valide:
            ajouter_resultat_simple(f"✅ '{mot}' appartient à '{racine}'", "success")
            if scheme and scheme != "déjà connu":
                ajouter_resultat_simple(f"   Schème détecté: {scheme}", "info")
        else:
            ajouter_resultat_simple(f"❌ '{mot}' n'appartient PAS à '{racine}'", "error")
        
        mot_val_input.current.value = ""
        racine_val_input.current.value = ""
        afficher_racines()
        page.update()
    
    def on_generer_tous_click(e):
        """Gestionnaire pour générer tous les dérivés"""
        racine = racine_tous_input.current.value.strip()
        
        if not racine:
            ajouter_resultat_simple("❌ Veuillez entrer une racine", "error")
            return
        
        generer_tous_action_auto(racine)
        racine_tous_input.current.value = ""
        page.update()
    
    def on_trouver_racine_click(e):
        """Gestionnaire pour trouver la racine d'un mot"""
        mot = mot_trouver_input.current.value.strip()
        
        if not mot:
            ajouter_resultat_simple("❌ Veuillez entrer un mot", "error")
            return
        
        # Utilise l'index inverse si disponible
        if hasattr(arbre, 'index_inverse') and mot in arbre.index_inverse:
            racine = arbre.index_inverse[mot]
            ajouter_resultat_simple(f"✅ '{mot}' → racine: {racine}", "success")
        else:
            # Cherche dans tout l'arbre
            racine_trouvee = None
            def chercher_recursif(noeud, mot):
                nonlocal racine_trouvee
                if noeud and not racine_trouvee:
                    if mot in noeud.derivees:
                        racine_trouvee = noeud.racine
                        return
                    chercher_recursif(noeud.gauche, mot)
                    chercher_recursif(noeud.droite, mot)
            
            chercher_recursif(arbre.racine, mot)
            
            if racine_trouvee:
                ajouter_resultat_simple(f"✅ '{mot}' → racine: {racine_trouvee}", "success")
            else:
                ajouter_resultat_simple(f"❌ Racine non trouvée pour '{mot}'", "error")
        
        mot_trouver_input.current.value = ""
        page.update()
    
    def on_afficher_schemes_click(e):
        """Affiche tous les schèmes disponibles"""
        schemes_trouves = []
        
        for i in range(table.taille):
            entree = table.table[i]
            while entree:
                schemes_trouves.append(entree)
                entree = entree.suivant
        
        contenu = ft.Column(scroll=ft.ScrollMode.AUTO, height=300)
        contenu.controls.append(
            ft.Text("SCHÈMES DISPONIBLES", size=18, weight=ft.FontWeight.BOLD)
        )
        
        if schemes_trouves:
            for scheme in schemes_trouves:
                contenu.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"🔸 {scheme.cle}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Pattern: {scheme.pattern}", size=14),
                            ft.Text(f"Description: {scheme.description}", size=12, color=ft.colors.GREY_600),
                        ]),
                        padding=10,
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        margin=ft.margin.only(bottom=10)
                    )
                )
        else:
            contenu.controls.append(ft.Text("Aucun schème disponible", color=ft.colors.GREY))
        
        dialog = ft.AlertDialog(
            title=ft.Text("Liste des schèmes"),
            content=contenu,
            actions=[
                ft.ElevatedButton("Fermer", on_click=lambda e: fermer_dialog_schemes(e))
            ]
        )
        
        def fermer_dialog_schemes(e):
            page.dialog.open = False
            page.update()
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    # ============ CONSTRUCTION DE L'INTERFACE ============
    
    # Titre principal
    titre = ft.Container(
        content=ft.Text(
            "📚 MOTEUR MORPHOLOGIQUE ARABE",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_700
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.only(bottom=20)
    )
    
    # ============ SECTION GAUCHE (AVEC DÉFILEMENT) ============
    
    # Créer une colonne scrollable pour le menu de gauche
    menu_gauche = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        height=700  # Hauteur fixe avec défilement
    )
    
    # Section Chargement
    section_chargement = ft.Container(
        content=ft.Column([
            ft.Text("CHARGEMENT & EXPORT", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(
                    "📥 Charger",
                    icon=ft.icons.DOWNLOAD,
                    on_click=on_charger_click,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    expand=True
                ),
                ft.ElevatedButton(
                    "📤 Exporter",
                    icon=ft.icons.UPLOAD,
                    on_click=on_exporter_click,
                    bgcolor=ft.colors.GREEN,
                    color=ft.colors.WHITE,
                    expand=True
                )
            ])
        ]),
        padding=15,
        bgcolor=ft.colors.BLUE_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_chargement)
    
    # Section Ajout Racine
    section_ajout_racine = ft.Container(
        content=ft.Column([
            ft.Text("AJOUTER RACINE", size=16, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=nouvelle_racine_input,
                label="Nouvelle racine",
                hint_text="Ex: ذهب",
                width=300
            ),
            ft.ElevatedButton("➕ Ajouter", on_click=on_ajouter_racine_click,
                            bgcolor=ft.colors.GREEN, color=ft.colors.WHITE)
        ]),
        padding=15,
        bgcolor=ft.colors.GREEN_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_ajout_racine)
    
    # Section Génération
    section_generation = ft.Container(
        content=ft.Column([
            ft.Text("GÉNÉRATION", size=16, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=racine_gen_input,
                label="Racine",
                hint_text="Ex: كتب",
                width=300
            ),
            ft.TextField(
                ref=scheme_gen_input,
                label="Schème",
                value="فاعل",
                width=300
            ),
            ft.ElevatedButton("🔨 Générer mot", on_click=on_generer_mot_click,
                            bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE)
        ]),
        padding=15,
        bgcolor=ft.colors.ORANGE_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_generation)
    
    # Section Validation
    section_validation = ft.Container(
        content=ft.Column([
            ft.Text("VALIDATION", size=16, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=mot_val_input,
                label="Mot à valider",
                hint_text="Ex: كاتب",
                width=300
            ),
            ft.TextField(
                ref=racine_val_input,
                label="Racine supposée",
                hint_text="Ex: كتب",
                width=300
            ),
            ft.ElevatedButton("✅ Valider mot", on_click=on_valider_mot_click,
                            bgcolor=ft.colors.PURPLE, color=ft.colors.WHITE)
        ]),
        padding=15,
        bgcolor=ft.colors.PURPLE_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_validation)
    
    # Section Générer Tous
    section_generer_tous = ft.Container(
        content=ft.Column([
            ft.Text("GÉNÉRER TOUS", size=16, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=racine_tous_input,
                label="Racine pour tous dérivés",
                hint_text="Ex: كتب",
                width=300
            ),
            ft.ElevatedButton("🚀 Générer tous", on_click=on_generer_tous_click,
                            bgcolor=ft.colors.DEEP_ORANGE, color=ft.colors.WHITE)
        ]),
        padding=15,
        bgcolor=ft.colors.DEEP_ORANGE_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_generer_tous)
    
    # Section Trouver Racine
    section_trouver = ft.Container(
        content=ft.Column([
            ft.Text("TROUVER RACINE", size=16, weight=ft.FontWeight.BOLD),
            ft.TextField(
                ref=mot_trouver_input,
                label="Mot à analyser",
                hint_text="Ex: كاتب",
                width=300
            ),
            ft.ElevatedButton("🔍 Trouver racine", on_click=on_trouver_racine_click,
                            bgcolor=ft.colors.CYAN, color=ft.colors.WHITE)
        ]),
        padding=15,
        bgcolor=ft.colors.CYAN_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_trouver)
    
    # Section Outils
    section_outils = ft.Container(
        content=ft.Column([
            ft.Text("OUTILS", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(
                    "🏷️ Voir schèmes",
                    on_click=on_afficher_schemes_click,
                    bgcolor=ft.colors.INDIGO,
                    color=ft.colors.WHITE,
                    expand=True
                ),
                ft.ElevatedButton(
                    "🗑️ Vider résultats",
                    on_click=lambda e: vider_resultats(),
                    bgcolor=ft.colors.RED,
                    color=ft.colors.WHITE,
                    expand=True
                )
            ])
        ]),
        padding=15,
        bgcolor=ft.colors.INDIGO_50,
        border_radius=10
    )
    
    menu_gauche.controls.append(section_outils)
    
    # ============ SECTION DROITE ============
    
    # Section Résultats
    resultats_container = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("RÉSULTATS", size=18, weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    on_click=lambda e: vider_resultats(),
                    icon_color=ft.colors.RED,
                    tooltip="Vider les résultats"
                )
            ]),
            ft.Container(
                content=resultats,
                border=ft.border.all(1, ft.colors.GREY_300),
                padding=10,
                border_radius=5,
                height=250,
                expand=True
            )
        ]),
        padding=15,
        bgcolor=ft.colors.GREY_50,
        border_radius=10,
        expand=True
    )
    
    # Section Racines
    racines_container = ft.Container(
        content=racines_liste,
        border=ft.border.all(1, ft.colors.GREY_300),
        padding=10,
        border_radius=5,
        height=350,
        expand=True
    )
    
    section_racines = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("RACINES DISPONIBLES", size=16, weight=ft.FontWeight.BOLD),
                ft.IconButton(
                    icon=ft.icons.REFRESH,
                    on_click=lambda e: afficher_racines(),
                    icon_color=ft.colors.BLUE,
                    tooltip="Rafraîchir la liste"
                )
            ]),
            ft.Text("👁️=Voir | ▶️=Générer | 🗑️=Supprimer", size=10, color=ft.colors.GREY_600),
            racines_container
        ]),
        padding=15,
        bgcolor=ft.colors.GREY_50,
        border_radius=10,
        expand=True
    )
    
    # Colonne de droite
    colonne_droite = ft.Column([
        resultats_container,
        section_racines
    ], expand=True)
    
    # Layout principal
    layout_principal = ft.Row([
        # Conteneur scrollable pour le menu gauche
        ft.Container(
            content=menu_gauche,
            width=400,
            padding=ft.padding.only(right=10)
        ),
        ft.VerticalDivider(width=1),
        colonne_droite
    ], expand=True)
    
    # Ajouter tout à la page
    page.add(
        titre,
        layout_principal
    )
    
    # Charger les données et afficher les racines
    charger_donnees()

# Lancement de l'application
ft.app(target=main)