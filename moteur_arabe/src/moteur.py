# -*- coding: utf-8 -*-
class MoteurMorphologique:
    """Moteur principal pour générer et valider les mots"""
    
    def __init__(self):
        self.arbre_racines = None
        self.table_schemes = None
    
    def initialiser(self, arbre, table):
        """Initialise avec les structures de données"""
        self.arbre_racines = arbre
        self.table_schemes = table
    
    def generer_mot(self, racine, scheme_cle):
        """Génère un mot à partir d'une racine et d'un schème"""
        # Vérifier si la racine existe
        noeud = self.arbre_racines.rechercher(self.arbre_racines.racine, racine)
        if not noeud:
            print(f"❌ Racine '{racine}' non trouvée")
            return None
        
        # Vérifier si le schème existe
        scheme = self.table_schemes.rechercher(scheme_cle)
        if not scheme:
            print(f"❌ Schème '{scheme_cle}' non trouvé")
            return None
        
        if len(racine) < 3:
            print("❌ Racine doit avoir au moins 3 caractères")
            return None
        
        # Générer le mot
        pattern = scheme.pattern
        mot_generé = pattern.replace('C1', racine[0])\
                            .replace('C2', racine[1])\
                            .replace('C3', racine[2])
        
        print(f"✅ Mot généré: {mot_generé}")
        
        # Ajouter aux dérivés et à l'index inverse
        if mot_generé not in noeud.derivees:
            noeud.derivees.append(mot_generé)
            # MET À JOUR L'INDEX INVERSE (TRÈS IMPORTANT !)
            self.arbre_racines.index_inverse[mot_generé] = racine
        
        return mot_generé
    
    def valider_mot(self, mot, racine):
        """Vérifie si un mot vient d'une racine donnée"""
        print(f"\n🔍 Validation : mot='{mot}', racine='{racine}'")
        
        # VÉRIFICATION RAPIDE AVEC INDEX INVERSE (O(1) !)
        racine_trouvee = self.arbre_racines.trouver_racine_du_mot(mot)
        if racine_trouvee:
            if racine_trouvee == racine:
                print(f"✅✅✅ Mot '{mot}' déjà validé! (via index inverse)")
                return True, "déjà connu"
            else:
                print(f"❌ Mot '{mot}' appartient à la racine '{racine_trouvee}', pas à '{racine}'")
                return False, None
        
        # Si pas dans l'index inverse, vérifie normalement
        noeud = self.arbre_racines.rechercher(self.arbre_racines.racine, racine)
        if not noeud:
            print(f"❌ Racine '{racine}' non trouvée")
            return False, None
        
        # Si le mot est déjà dans les dérivés validés
        if mot in noeud.derivees:
            print(f"✅ Mot '{mot}' déjà validé pour la racine '{racine}'")
            return True, "déjà connu"
        
        # Extraire les consonnes de la racine
        if len(racine) >= 3:
            c1, c2, c3 = racine[0], racine[1], racine[2]
        else:
            return False, None
        
        # Chercher dans tous les schèmes
        scheme_trouve = None
        
        for i in range(self.table_schemes.taille):
            entree = self.table_schemes.table[i]
            while entree:
                pattern = entree.pattern
                
                # Générer le mot avec ce pattern
                mot_test = pattern.replace('C1', c1)\
                                   .replace('C2', c2)\
                                   .replace('C3', c3)
                
                if mot_test == mot:
                    scheme_trouve = entree.cle
                    break
                
                entree = entree.suivant
            
            if scheme_trouve:
                break
        
        if scheme_trouve:
            # Ajouter aux dérivés validés
            noeud.derivees.append(mot)
            # AJOUTER À L'INDEX INVERSE
            self.arbre_racines.index_inverse[mot] = racine
            
            print(f"✅ Mot '{mot}' validé! Schème: {scheme_trouve}")
            return True, scheme_trouve
        else:
            print(f"❌ Mot '{mot}' ne correspond à aucun schème pour la racine '{racine}'")
            return False, None
    
    def afficher_famille(self, racine):
        """Affiche tous les dérivés d'une racine"""
        noeud = self.arbre_racines.rechercher(self.arbre_racines.racine, racine)
        if not noeud:
            print(f"❌ Racine '{racine}' non trouvée")
            return
        
        print(f"\n=== FAMILLE MORPHOLOGIQUE DE '{racine}' ===")
        if noeud.derivees:
            for i, mot in enumerate(noeud.derivees, 1):
                print(f"{i}. {mot}")
        else:
            print("Aucun dérivé enregistré")
        
        print(f"\nTotal: {len(noeud.derivees)} mot(s)")
    
    def generer_tous_dérivés(self, racine):
        """Génère tous les dérivés possibles pour une racine"""
        noeud = self.arbre_racines.rechercher(self.arbre_racines.racine, racine)
        if not noeud:
            print(f"❌ Racine '{racine}' non trouvée")
            return []
        
        print(f"\n=== GÉNÉRATION DE TOUS LES DÉRIVÉS POUR '{racine}' ===")
        mots_generes = []
        
        # Parcourir tous les schèmes
        for i in range(self.table_schemes.taille):
            entree = self.table_schemes.table[i]
            while entree:
                mot = self.generer_mot(racine, entree.cle)
                if mot and mot not in mots_generes:
                    mots_generes.append(mot)
                entree = entree.suivant
        
        print(f"\n✅ {len(mots_generes)} dérivé(s) généré(s)")
        return mots_generes
    
    def trouver_racine_d_un_mot(self, mot):
        """Trouve la racine d'un mot donné"""
        racine = self.arbre_racines.trouver_racine_du_mot(mot)
        if racine:
            print(f"✅ Le mot '{mot}' vient de la racine: {racine}")
            return racine
        else:
            print(f"❌ Mot '{mot}' non trouvé dans la base")
            return None