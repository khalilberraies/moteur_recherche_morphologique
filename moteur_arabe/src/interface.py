# -*- coding: utf-8 -*-
from arbre_abr import ArbreAVL
from table_hachage import TableHachage
from moteur import MoteurMorphologique

class InterfaceCLI:
    """Interface en ligne de commande"""
    
    def __init__(self):
        self.arbre = ArbreAVL()
        self.table = TableHachage()
        self.moteur = MoteurMorphologique()
        self.moteur.initialiser(self.arbre, self.table)
    
    def afficher_menu(self):
        """Affiche le menu principal"""
        print("\n" + "="*50)
        print("    MOTEUR MORPHOLOGIQUE ARABE")
        print("="*50)
        print("1. 📥 Charger les données depuis fichiers")
        print("2. 🌳 Afficher toutes les racines")
        print("3. 🏷️  Afficher tous les schèmes")
        print("4. ➕ Ajouter une nouvelle racine")
        print("5. 🏗️  Ajouter un nouveau schème")
        print("6. 🔨 Générer un mot")
        print("7. ✅ Valider un mot")
        print("8. 👨‍👩‍👧‍👦 Afficher famille morphologique")
        print("9. 🚀 Générer tous les dérivés d'une racine")
        print("10.🔍 Trouver racine d'un mot (RAPIDE)")
        print("11.📊 Statistiques")
        print("0. 🚪 Quitter")
        print("="*50)
    
    def charger_donnees(self):
        """Charge les données depuis les fichiers"""
        print("\n=== CHARGEMENT DES DONNÉES ===")
        
        fichier_racines = input("Fichier racines (defaut: data/racines.txt): ") or "data/racines.txt"
        fichier_schemes = input("Fichier schèmes (defaut: data/schemes.txt): ") or "data/schemes.txt"
        
        # Charger les racines
        self.arbre.charger_depuis_fichier(fichier_racines)
        
        # Charger les schèmes
        self.table.charger_depuis_fichier(fichier_schemes)
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def ajouter_racine(self):
        """Ajoute une nouvelle racine"""
        print("\n=== AJOUTER UNE NOUVELLE RACINE ===")
        racine = input("Entrez la racine (3 lettres arabes): ").strip()
        
        if len(racine) < 3:
            print("❌ Une racine doit avoir au moins 3 caractères")
            return
        
        self.arbre.racine = self.arbre.inserer(self.arbre.racine, racine)
        print(f"✅ Racine '{racine}' ajoutée avec succès")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def ajouter_scheme(self):
        """Ajoute un nouveau schème"""
        print("\n=== AJOUTER UN NOUVEAU SCHÈME ===")
        cle = input("Nom du schème (ex: فاعل): ").strip()
        pattern = input("Pattern (utiliser C1,C2,C3, ex: C1اC2C3): ").strip()
        description = input("Description: ").strip()
        
        if not cle or not pattern:
            print("❌ Le nom et le pattern sont obligatoires")
            return
        
        self.table.inserer(cle, pattern, description)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def generer_mot(self):
        """Génère un mot"""
        print("\n=== GÉNÉRATION D'UN MOT ===")
        racine = input("Entrez la racine: ").strip()
        scheme_cle = input("Entrez le schème (ex: فاعل): ").strip()
        
        if not racine or not scheme_cle:
            print("❌ Racine et schème requis")
            return
        
        self.moteur.generer_mot(racine, scheme_cle)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def valider_mot(self):
        """Valide un mot"""
        print("\n=== VALIDATION D'UN MOT ===")
        mot = input("Entrez le mot à valider: ").strip()
        racine = input("Entrez la racine supposée: ").strip()
        
        if not mot or not racine:
            print("❌ Mot et racine requis")
            return
        
        valide, scheme = self.moteur.valider_mot(mot, racine)
        if valide:
            print(f"✅ Résultat: OUI, schème: {scheme}")
        else:
            print("❌ Résultat: NON")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def trouver_racine_d_un_mot(self):
        """Trouve la racine d'un mot"""
        print("\n=== TROUVER RACINE D'UN MOT ===")
        mot = input("Entrez le mot: ").strip()
        
        if not mot:
            print("❌ Mot requis")
            return
        
        self.moteur.trouver_racine_d_un_mot(mot)
        input("\nAppuyez sur Entrée pour continuer...")
    
    def afficher_statistiques(self):
        """Affiche des statistiques"""
        print("\n=== STATISTIQUES ===")
        
        # Compter les racines
        nb_racines = self.arbre.compter_noeuds(self.arbre.racine)
        print(f"📈 Nombre de racines: {nb_racines}")
        
        # Compter les dérivés totaux
        total_derives = 0
        def compter_derives(noeud):
            nonlocal total_derives
            if noeud:
                total_derives += len(noeud.derivees)
                compter_derives(noeud.gauche)
                compter_derives(noeud.droite)
        
        compter_derives(self.arbre.racine)
        print(f"📈 Nombre total de dérivés: {total_derives}")
        
        # Taille de l'index inverse
        print(f"⚡ Taille index inverse: {len(self.arbre.index_inverse)}")
        print("   (permet validation O(1) des mots)")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def executer(self):
        """Exécute l'interface principale"""
        print("Bienvenue dans le Moteur Morphologique Arabe!")
        print("Commencez par charger les données (option 1)")
        
        while True:
            self.afficher_menu()
            choix = input("\nVotre choix (0-11): ").strip()
            
            try:
                choix = int(choix)
            except ValueError:
                print("❌ Veuillez entrer un nombre")
                continue
            
            if choix == 0:
                print("\nAu revoir! 👋")
                break
            elif choix == 1:
                self.charger_donnees()
            elif choix == 2:
                print("\n=== RACINES DISPONIBLES ===")
                self.arbre.afficher_infixe(self.arbre.racine)
                input("\nAppuyez sur Entrée pour continuer...")
            elif choix == 3:
                self.table.afficher_tous()
                input("\nAppuyez sur Entrée pour continuer...")
            elif choix == 4:
                self.ajouter_racine()
            elif choix == 5:
                self.ajouter_scheme()
            elif choix == 6:
                self.generer_mot()
            elif choix == 7:
                self.valider_mot()
            elif choix == 8:
                racine = input("\nEntrez la racine: ").strip()
                self.moteur.afficher_famille(racine)
                input("\nAppuyez sur Entrée pour continuer...")
            elif choix == 9:
                racine = input("\nEntrez la racine: ").strip()
                self.moteur.generer_tous_dérivés(racine)
                input("\nAppuyez sur Entrée pour continuer...")
            elif choix == 10:
                self.trouver_racine_d_un_mot()
            elif choix == 11:
                self.afficher_statistiques()
            else:
                print("❌ Choix invalide")