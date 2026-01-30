#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime

class InterfaceCLI:
    """
    Interface en ligne de commande pour le moteur morphologique arabe.
    Fournit un menu interactif pour toutes les fonctionnalités.
    """
    
    def __init__(self, moteur):
        """
        Initialise l'interface avec le moteur.
        
        Args:
            moteur: Instance de MoteurMorphologique
        """
        self.moteur = moteur
        self.quitter = False
    
    def afficher_menu(self):
        """Affiche le menu principal avec des bordures."""
        print("\n" + "═" * 60)
        print("          🕌 MOTEUR MORPHOLOGIQUE ARABE 🕌")
        print("═" * 60)
        print(" 1. 📋 Afficher toutes les racines")
        print(" 2. 🎯 Afficher tous les schèmes")
        print(" 3. ➕ Ajouter une nouvelle racine")      # ← NOUVEAU
        print(" 4. ➕ Ajouter un nouveau schème")        # ← NOUVEAU
        print(" 5. 🔧 Générer un mot dérivé")
        print(" 6. ✅ Valider un mot")
        print(" 7. 📂 Charger depuis fichiers")
        print(" 8. 💾 Sauvegarder les données")          # ← NOUVEAU
        print(" 9. 📊 Afficher les statistiques")
        print("10. 🆘 Aide / Exemples")
        print("11. 🚪 Quitter")
        print("═" * 60)
    
    def executer(self):
        """Boucle principale de l'interface."""
        print("\n✨ Bienvenue dans le moteur morphologique arabe! ✨")
        print("  Un outil pour explorer la morphologie de la langue arabe.")
        print("  Basé sur le système racine-schème (Root-Pattern).\n")
        
        # Charger les données par défaut au démarrage
        self.charger_donnees_par_defaut()
        
        while not self.quitter:
            self.afficher_menu()
            choix = input("\n📝 Votre choix (1-11): ").strip()
            
            if choix == "1":
                self.afficher_racines()
            elif choix == "2":
                self.afficher_schemas()
            elif choix == "3":
                self.ajouter_racine()
            elif choix == "4":
                self.ajouter_schema()
            elif choix == "5":
                self.generer_mot()
            elif choix == "6":
                self.valider_mot()
            elif choix == "7":
                self.charger_fichiers_personnalises()
            elif choix == "8":
                self.sauvegarder_donnees()
            elif choix == "9":
                self.moteur.afficher_statistiques()
            elif choix == "10":
                self.afficher_aide()
            elif choix == "11":
                self.quitter = True
                print("\n👋 Au revoir! Merci d'avoir utilisé le moteur.")
            else:
                print("\n❌ Choix invalide. Veuillez entrer un nombre entre 1 et 11.")
    
    def charger_donnees_par_defaut(self):
        """Charge les données par défaut au démarrage."""
        print("\n🔧 Chargement des données par défaut...")
        
        # Charger depuis les fichiers s'ils existent
        racines_ok = self.moteur.charger_racines_fichier()
        schemas_ok = self.moteur.charger_schemas_fichier()
        
        # Si fichiers non trouvés, charger des données minimales
        if not racines_ok:
            print("⚠️  Aucun fichier de racines trouvé. Chargement de données minimales...")
            racines_defaut = ["كتب", "فعل", "درس", "سلم", "حسب", "علم", "عمل", "قرب"]
            for racine in racines_defaut:
                self.moteur.arbre_racines.inserer(racine)
            print(f"✅ {len(racines_defaut)} racines chargées (par défaut)")
        
        if not schemas_ok:
            print("⚠️  Aucun fichier de schèmes trouvé. Chargement de schèmes de base...")
            from src.table_hachage import Schema
            schemas_defaut = [
                ("فاعل", "1a23", "nom d'agent (écrivain)"),
                ("مفعول", "ma123", "participe passif (écrit)"),
                ("مفعل", "ma12a3", "nom de lieu (bibliothèque)"),
                ("افعل", "af1a2", "impératif (écris!)"),
                ("تفاعل", "tafa12a3", "forme réciproque"),
            ]
            for nom, modele, desc in schemas_defaut:
                self.moteur.table_schemas.ajouter(Schema(nom, modele, desc))
            print(f"✅ {len(schemas_defaut)} schèmes chargés (par défaut)")
    
    def afficher_racines(self):
        """Affiche toutes les racines de l'arbre."""
        print("\n" + "─" * 50)
        print("📚 RACINES ARABES DANS L'ARBRE")
        print("─" * 50)
        
        if self.moteur.arbre_racines.racine is None:
            print("ℹ️  L'arbre est vide. Chargez des racines d'abord.")
            return
        
        # Parcours infixe pour afficher trié
        print("Racines triées par ordre alphabétique arabe:")
        self._afficher_racines_recursif(self.moteur.arbre_racines.racine)
        
        print(f"\n📊 Total: {self.moteur.arbre_racines.taille()} racine(s)")
        print("─" * 50)
    
    def _afficher_racines_recursif(self, noeud):
        """Méthode auxiliaire pour afficher les racines récursivement."""
        if noeud:
            self._afficher_racines_recursif(noeud.gauche)
            # Afficher la racine et ses dérivés
            if hasattr(noeud, 'derives_list') and noeud.derives_list:
                print(f"  • {noeud.racine} → Dérivés: {', '.join(noeud.derives_list)}")
            elif hasattr(noeud, 'derives') and noeud.derives:
                print(f"  • {noeud.racine} → Dérivés: {', '.join(noeud.derives)}")
            else:
                print(f"  • {noeud.racine} (aucun dérivé)")
            self._afficher_racines_recursif(noeud.droit)
    
    def afficher_schemas(self):
        """Affiche tous les schèmes disponibles."""
        print("\n" + "─" * 50)
        print("🎯 SCHÈMES MORPHOLOGIQUES DISPONIBLES")
        print("─" * 50)
        
        self.moteur.table_schemas.afficher_tous()
        print("─" * 50)
    
    def ajouter_racine(self):
        """Interface pour ajouter dynamiquement une racine."""
        print("\n" + "─" * 50)
        print("➕ AJOUT D'UNE NOUVELLE RACINE")
        print("─" * 50)
        
        print("\nℹ️  Format requis:")
        print("  • 3 lettres arabes (ex: 'كتب', 'فعل', 'درس')")
        print("  • Racine trilitère standard")
        print("  • Pas d'espaces, pas de voyelles")
        print("─" * 20)
        
        while True:
            racine = input("📥 Entrez la nouvelle racine (ou 'q' pour annuler): ").strip()
            
            if racine.lower() == 'q':
                print("❌ Ajout annulé.")
                return
            
            # Validation de la racine
            if not racine:
                print("❌ Erreur: La racine ne peut pas être vide.")
                continue
            
            if len(racine) != 3:
                print(f"❌ Erreur: La racine doit avoir 3 lettres (vous avez {len(racine)}).")
                print(f"   Exemples: 'كتب', 'فعل', 'سلم'")
                continue
            
            # Vérifier que ce sont bien des lettres arabes
            if not all('\u0600' <= c <= '\u06FF' for c in racine):
                print("❌ Erreur: La racine doit contenir uniquement des lettres arabes.")
                continue
            
            # Vérifier si la racine existe déjà
            if self.moteur.arbre_racines.rechercher(racine):
                print(f"⚠️  La racine '{racine}' existe déjà dans l'arbre.")
                
                # Demander si on veut quand même l'ajouter (pour re-ajouter si supprimée)
                choix = input("Voulez-vous quand même l'ajouter? (o/n): ").strip().lower()
                if choix != 'o':
                    continue
            
            # Confirmation
            print(f"\n📝 Racine à ajouter: '{racine}'")
            confirmation = input("Confirmez l'ajout? (o/n): ").strip().lower()
            
            if confirmation == 'o':
                # Insérer la racine
                self.moteur.arbre_racines.inserer(racine)
                
                # Afficher confirmation
                print(f"\n✅ Racine '{racine}' ajoutée avec succès!")
                print(f"   Elle est maintenant disponible pour la génération de mots.")
                
                # Demander si on veut ajouter des dérivés manuellement
                ajouter_derives = input("\n💡 Voulez-vous ajouter des dérivés manuellement? (o/n): ").strip().lower()
                if ajouter_derives == 'o':
                    self.ajouter_derives_manuels(racine)
                
                break
            else:
                print("❌ Ajout annulé.")
                break
        
        print("─" * 50)
    
    def ajouter_derives_manuels(self, racine):
        """Permet d'ajouter des dérivés manuellement à une racine."""
        print(f"\n📝 Ajout de dérivés pour la racine '{racine}':")
        print("  (Appuyez sur Entrée sans texte pour terminer)")
        
        while True:
            derive = input(f"  Dérivé pour '{racine}': ").strip()
            
            if not derive:
                print("  ✓ Fin de l'ajout des dérivés.")
                break
            
            # Ajouter le dérivé
            if self.moteur.arbre_racines.ajouter_derive(racine, derive):
                print(f"    ✅ '{derive}' ajouté.")
            else:
                print(f"    ⚠️  '{derive}' existe déjà ou erreur.")
    
    def ajouter_schema(self):
        """Interface pour ajouter dynamiquement un schème."""
        print("\n" + "─" * 50)
        print("➕ AJOUT D'UN NOUVEAU SCHÈME")
        print("─" * 50)
        
        print("\nℹ️  Format requis:")
        print("  • Nom du schème (ex: 'فاعل', 'مفعول')")
        print("  • Modèle abstrait (ex: '1a23', 'ma123')")
        print("  • Description optionnelle")
        print("─" * 20)
        
        nom = input("📥 Nom du schème: ").strip()
        modele = input("📥 Modèle abstrait (ex: 1a23): ").strip()
        description = input("📥 Description (optionnel): ").strip()
        
        if not nom or not modele:
            print("❌ Erreur: Le nom et le modèle sont obligatoires.")
            return
        
        # Vérifier si le schème existe déjà
        from src.table_hachage import Schema
        schema_existant = self.moteur.table_schemas.obtenir(nom)
        
        if schema_existant:
            print(f"⚠️  Le schème '{nom}' existe déjà.")
            print(f"   Modèle actuel: {schema_existant.modele}")
            
            choix = input("Remplacer? (o/n): ").strip().lower()
            if choix != 'o':
                print("❌ Ajout annulé.")
                return
        
        # Créer et ajouter le schème
        nouveau_schema = Schema(nom, modele, description)
        self.moteur.table_schemas.ajouter(nouveau_schema)
        
        print(f"\n✅ Schème '{nom}' ajouté avec succès!")
        print(f"   Modèle: {modele}")
        if description:
            print(f"   Description: {description}")
        
        print("─" * 50)
    
    def generer_mot(self):
        """Interface pour générer un mot."""
        print("\n" + "─" * 50)
        print("🔧 GÉNÉRATION D'UN MOT DÉRIVÉ")
        print("─" * 50)
        
        print("\nℹ️  Format requis:")
        print("  • Racine: 3 lettres arabes (ex: 'كتب', 'فعل')")
        print("  • Schème: nom du schème (ex: 'فاعل', 'مفعول')")
        print("  Exemple: كتب + فاعل → كاتب (écrivain)")
        print("─" * 20)
        
        racine = input("📥 Entrez la racine: ").strip()
        schema = input("📥 Entrez le schème: ").strip()
        
        if not racine or not schema:
            print("❌ Erreur: Veuillez entrer une racine ET un schème.")
            return
        
        print("\n🔨 Génération en cours...")
        mot, message = self.moteur.generer_mot(racine, schema)
        
        if mot:
            print(f"\n🎉 RÉSULTAT:")
            print(f"   Racine: {racine}")
            print(f"   Schème: {schema}")
            print(f"   Mot généré: {mot}")
            print(f"   Statut: {message}")
            
            # Demander si l'utilisateur veut enregistrer
            sauvegarder = input("\n💾 Ajouter ce mot aux dérivés validés? (o/n): ").strip().lower()
            if sauvegarder == 'o':
                # Déjà fait par generer_mot(), on confirme juste
                print("✅ Mot ajouté aux dérivés de la racine.")
        else:
            print(f"\n❌ ÉCHEC:")
            print(f"   Message: {message}")
            print(f"   Vérifiez que la racine et le schème existent.")
        
        print("─" * 50)
    
    def valider_mot(self):
        """Interface pour valider un mot."""
        print("\n" + "─" * 50)
        print("✅ VALIDATION D'UN MOT")
        print("─" * 50)
        
        print("\nℹ️  Validez si un mot appartient à une famille morphologique.")
        print("  Exemple: Mot 'كاتب' avec racine 'كتب' → VALIDE")
        print("─" * 20)
        
        mot = input("📥 Entrez le mot à valider: ").strip()
        racine = input("📥 Entrez la racine supposée: ").strip()
        
        if not mot or not racine:
            print("❌ Erreur: Veuillez entrer un mot ET une racine.")
            return
        
        print("\n🔍 Validation en cours...")
        valide, message, schema = self.moteur.valider_mot(mot, racine)
        
        print(f"\n📋 RÉSULTAT:")
        print(f"   Mot: {mot}")
        print(f"   Racine testée: {racine}")
        
        if valide:
            print(f"   ✅ {message}")
            if schema and schema != "Schème inconnu":
                print(f"   🎯 Schème identifié: {schema}")
        else:
            print(f"   ❌ {message}")
        
        print("─" * 50)
    
    def charger_fichiers_personnalises(self):
        """Interface pour charger des fichiers personnalisés."""
        print("\n" + "─" * 50)
        print("📂 CHARGEMENT DEPUIS FICHIERS")
        print("─" * 50)
        
        print("\nℹ️  Fichiers par défaut:")
        print("  • Racines: data/racines.txt")
        print("  • Schèmes: data/schemas.txt")
        print("─" * 20)
        
        print("Options:")
        print("  1. Charger depuis fichiers par défaut")
        print("  2. Charger depuis fichiers personnalisés")
        print("  3. Annuler")
        
        choix = input("\n📝 Votre choix (1-3): ").strip()
        
        if choix == "1":
            print("\n🔧 Chargement des fichiers par défaut...")
            self.moteur.charger_racines_fichier()
            self.moteur.charger_schemas_fichier()
            print("✅ Chargement terminé.")
            
        elif choix == "2":
            print("\n🎯 Chargement personnalisé:")
            fichier_racines = input("Chemin vers le fichier des racines: ").strip()
            fichier_schemas = input("Chemin vers le fichier des schèmes: ").strip()
            
            if fichier_racines:
                self.moteur.charger_racines_fichier(fichier_racines)
            if fichier_schemas:
                self.moteur.charger_schemas_fichier(fichier_schemas)
            
            print("✅ Chargement terminé.")
        
        elif choix == "3":
            print("❌ Chargement annulé.")
        
        else:
            print("❌ Choix invalide.")
        
        print("─" * 50)
    
    def sauvegarder_donnees(self):
        """Sauvegarde les données dans des fichiers."""
        print("\n" + "─" * 50)
        print("💾 SAUVEGARDE DES DONNÉES")
        print("─" * 50)
        
        print("\nOptions de sauvegarde:")
        print("  1. Sauvegarder les racines uniquement")
        print("  2. Sauvegarder les schèmes uniquement")
        print("  3. Sauvegarder tout")
        print("  4. Annuler")
        
        choix = input("\n📝 Votre choix (1-4): ").strip()
        
        if choix == "1":
            self._sauvegarder_racines()
        elif choix == "2":
            self._sauvegarder_schemas()
        elif choix == "3":
            self._sauvegarder_racines()
            self._sauvegarder_schemas()
        elif choix == "4":
            print("❌ Sauvegarde annulée.")
        else:
            print("❌ Choix invalide.")
        
        print("─" * 50)
    
    def _sauvegarder_racines(self, chemin="data/racines.txt"):
        """Sauvegarde toutes les racines dans un fichier."""
        try:
            # Collecter toutes les racines
            racines = []
            self._collecter_racines(self.moteur.arbre_racines.racine, racines)
            
            # Écrire dans le fichier
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write("# Racines arabes - Généré automatiquement\n")
                f.write("# Format: une racine par ligne\n")
                f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for racine in racines:
                    f.write(f"{racine}\n")
            
            print(f"✅ {len(racines)} racines sauvegardées dans {chemin}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur de sauvegarde: {e}")
            return False
    
    def _collecter_racines(self, noeud, liste):
        """Collecte récursivement toutes les racines."""
        if noeud:
            self._collecter_racines(noeud.gauche, liste)
            liste.append(noeud.racine)
            self._collecter_racines(noeud.droit, liste)
    
    def _sauvegarder_schemas(self, chemin="data/schemas.txt"):
        """Sauvegarde tous les schèmes dans un fichier."""
        try:
            # Collecter tous les schèmes
            schemas = []
            for bucket in self.moteur.table_schemas.table:
                for nom, schema in bucket:
                    schemas.append((schema.nom, schema.modele, schema.description if hasattr(schema, 'description') else ""))
            
            # Écrire dans le fichier
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write("# Schèmes morphologiques arabes\n")
                f.write("# Format: nom:modele:description\n")
                f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for nom, modele, desc in schemas:
                    desc_part = f":{desc}" if desc else ""
                    f.write(f"{nom}:{modele}{desc_part}\n")
            
            print(f"✅ {len(schemas)} schèmes sauvegardés dans {chemin}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur de sauvegarde: {e}")
            return False
    
    def afficher_aide(self):
        """Affiche l'aide et des exemples."""
        print("\n" + "═" * 60)
        print("🆘 AIDE ET EXEMPLES")
        print("═" * 60)
        
        print("\n📚 QU'EST-CE QUE C'EST?")
        print("  Un moteur morphologique pour la langue arabe basé sur")
        print("  le système racine-schème (Root-Pattern).")
        
        print("\n🎯 COMMENT ÇA MARCHE?")
        print("  1. Les racines (ex: كتب K-T-B) sont stockées dans un arbre")
        print("  2. Les schèmes (ex: فاعل 1a23) sont dans une table de hachage")
        print("  3. Combinaison → mots (ex: كاتب 'écrivain')")
        
        print("\n🔧 EXEMPLES DE GÉNÉRATION:")
        print("  ┌──────────┬─────────┬──────────────┬──────────────────┐")
        print("  │ Racine   │ Schème  │ Mot généré   │ Signification    │")
        print("  ├──────────┼─────────┼──────────────┼──────────────────┤")
        print("  │ كتب      │ فاعل    │ كاتب        │ écrivain         │")
        print("  │ كتب      │ مفعول   │ مكتوب       │ écrit            │")
        print("  │ كتب      │ مفعل    │ مكتبة       │ bibliothèque     │")
        print("  │ فعل      │ فاعل    │ فاعل        │ agent/faiseur    │")
        print("  │ فعل      │ مفعول   │ مفعول       │ objet de l'action│")
        print("  └──────────┴─────────┴──────────────┴──────────────────┘")
        
        print("\n➕ AJOUT DYNAMIQUE:")
        print("  • Menu 3: Ajouter une nouvelle racine (3 lettres arabes)")
        print("  • Menu 4: Ajouter un nouveau schème (nom + modèle)")
        print("  • Les ajouts sont immédiatement disponibles")
        
        print("\n📁 FICHIERS DE DONNÉES:")
        print("  • data/racines.txt : Une racine par ligne")
        print("  • data/schemas.txt : Format 'nom:modele:description'")
        print("  • Menu 8: Sauvegarder les données modifiées")
        
        print("\n⚙️  STRUCTURES DE DONNÉES:")
        print("  • Arbre Binaire de Recherche (ABR) → Racines (recherche O(log n))")
        print("  • Table de Hachage → Schèmes (accès O(1))")
        print("  • Sets Python → Dérivés (vérification O(1))")
        
        print("\n💡 ASTUCES:")
        print("  • Utilisez 'Ajouter une racine' pour enrichir la base")
        print("  • Testez avec les exemples ci-dessus pour comprendre")
        print("  • Explorez les familles de mots (même racine)")
        print("  • Sauvegardez vos modifications pour les garder")
        
        print("═" * 60)