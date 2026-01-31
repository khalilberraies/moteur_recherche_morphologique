# -*- coding: utf-8 -*-
class NoeudAVL:
    """Nœud de l'arbre AVL pour une racine arabe"""
    
    def __init__(self, racine):
        self.racine = racine          # Racine arabe (ex: "كتب")
        self.derivees = []            # Liste des mots dérivés
        self.gauche = None            # Sous-arbre gauche
        self.droite = None            # Sous-arbre droit
        self.hauteur = 1              # Hauteur pour AVL

class ArbreAVL:
    """Arbre AVL pour gérer les racines arabes avec index inverse"""
    
    def __init__(self):
        self.racine = None
        self.index_inverse = {}       # mot → racine (TRÈS IMPORTANT !)
    
    def hauteur(self, noeud):
        """Retourne la hauteur d'un nœud"""
        return noeud.hauteur if noeud else 0
    
    def equilibre(self, noeud):
        """Calcule le facteur d'équilibre"""
        return self.hauteur(noeud.gauche) - self.hauteur(noeud.droite) if noeud else 0
    
    def rotation_droite(self, z):
        """Rotation droite AVL"""
        y = z.gauche
        T2 = y.droite
        y.droite = z
        z.gauche = T2
        z.hauteur = 1 + max(self.hauteur(z.gauche), self.hauteur(z.droite))
        y.hauteur = 1 + max(self.hauteur(y.gauche), self.hauteur(y.droite))
        return y
    
    def rotation_gauche(self, z):
        """Rotation gauche AVL"""
        y = z.droite
        T2 = y.gauche
        y.gauche = z
        z.droite = T2
        z.hauteur = 1 + max(self.hauteur(z.gauche), self.hauteur(z.droite))
        y.hauteur = 1 + max(self.hauteur(y.gauche), self.hauteur(y.droite))
        return y
    
    def inserer(self, noeud, racine):
        """Insère une nouvelle racine"""
        if not noeud:
            return NoeudAVL(racine)
        
        if racine < noeud.racine:
            noeud.gauche = self.inserer(noeud.gauche, racine)
        elif racine > noeud.racine:
            noeud.droite = self.inserer(noeud.droite, racine)
        else:
            return noeud  # Racine déjà présente
        
        noeud.hauteur = 1 + max(self.hauteur(noeud.gauche), 
                               self.hauteur(noeud.droite))
        
        balance = self.equilibre(noeud)
        
        # Cas Gauche-Gauche
        if balance > 1 and racine < noeud.gauche.racine:
            return self.rotation_droite(noeud)
        
        # Cas Droite-Droite
        if balance < -1 and racine > noeud.droite.racine:
            return self.rotation_gauche(noeud)
        
        # Cas Gauche-Droite
        if balance > 1 and racine > noeud.gauche.racine:
            noeud.gauche = self.rotation_gauche(noeud.gauche)
            return self.rotation_droite(noeud)
        
        # Cas Droite-Gauche
        if balance < -1 and racine < noeud.droite.racine:
            noeud.droite = self.rotation_droite(noeud.droite)
            return self.rotation_gauche(noeud)
        
        return noeud
    
    def rechercher(self, noeud, racine):
        """Recherche une racine dans l'arbre"""
        if not noeud or racine == noeud.racine:
            return noeud
        
        if racine < noeud.racine:
            return self.rechercher(noeud.gauche, racine)
        
        return self.rechercher(noeud.droite, racine)
    
    def ajouter_derive(self, racine, mot, scheme=None):
        """Ajoute un dérivé à une racine"""
        noeud = self.rechercher(self.racine, racine)
        if not noeud:
            return False
        
        # Ajoute à la liste des dérivés
        if mot not in noeud.derivees:
            noeud.derivees.append(mot)
            
            # MET À JOUR L'INDEX INVERSE (IMPORTANT !)
            self.index_inverse[mot] = racine
            
            return True
        return False
    
    def trouver_racine_du_mot(self, mot):
        """
        Trouve la racine d'un mot
        Complexité O(1) grâce à index_inverse !
        """
        return self.index_inverse.get(mot)
    
    def afficher_infixe(self, noeud):
        """Affiche toutes les racines triées"""
        if noeud:
            self.afficher_infixe(noeud.gauche)
            print(f"  - {noeud.racine} ({len(noeud.derivees)} dérivés)")
            self.afficher_infixe(noeud.droite)
    
    def charger_depuis_fichier(self, nom_fichier):
        """Charge les racines depuis un fichier texte"""
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    racine = ligne.strip()
                    if racine and len(racine) >= 3:
                        self.racine = self.inserer(self.racine, racine)
            print(f"✅ Racines chargées depuis '{nom_fichier}'")
        except FileNotFoundError:
            print(f"❌ Fichier '{nom_fichier}' non trouvé")
    
    def compter_noeuds(self, noeud):
        """Compte le nombre de racines"""
        if not noeud:
            return 0
        return 1 + self.compter_noeuds(noeud.gauche) + self.compter_noeuds(noeud.droite)
    def trouver_min(self, noeud):
        """Trouve le nœud avec la valeur minimale"""
        current = noeud
        while current.gauche:
            current = current.gauche
        return current
    
    def supprimer(self, noeud, racine):
        """Supprime une racine de l'arbre AVL"""
        if not noeud:
            return noeud
        
        # Étape 1 : suppression standard BST
        if racine < noeud.racine:
            noeud.gauche = self.supprimer(noeud.gauche, racine)
        elif racine > noeud.racine:
            noeud.droite = self.supprimer(noeud.droite, racine)
        else:
            # Nœud à supprimer trouvé
            
            # Supprimer de l'index inverse tous les dérivés
            for mot in noeud.derivees:
                if mot in self.index_inverse:
                    del self.index_inverse[mot]
            
            # Nœud avec un seul enfant ou sans enfant
            if not noeud.gauche:
                temp = noeud.droite
                noeud = None
                return temp
            elif not noeud.droite:
                temp = noeud.gauche
                noeud = None
                return temp
            
            # Nœud avec deux enfants
            temp = self.trouver_min(noeud.droite)
            noeud.racine = temp.racine
            noeud.derivees = temp.derivees
            noeud.droite = self.supprimer(noeud.droite, temp.racine)
        
        if not noeud:
            return noeud
        
        # Étape 2 : mettre à jour la hauteur
        noeud.hauteur = 1 + max(self.hauteur(noeud.gauche),
                               self.hauteur(noeud.droite))
        
        # Étape 3 : rééquilibrer l'arbre
        balance = self.equilibre(noeud)
        
        # Cas Gauche-Gauche
        if balance > 1 and self.equilibre(noeud.gauche) >= 0:
            return self.rotation_droite(noeud)
        
        # Cas Gauche-Droite
        if balance > 1 and self.equilibre(noeud.gauche) < 0:
            noeud.gauche = self.rotation_gauche(noeud.gauche)
            return self.rotation_droite(noeud)
        
        # Cas Droite-Droite
        if balance < -1 and self.equilibre(noeud.droite) <= 0:
            return self.rotation_gauche(noeud)
        
        # Cas Droite-Gauche
        if balance < -1 and self.equilibre(noeud.droite) > 0:
            noeud.droite = self.rotation_droite(noeud.droite)
            return self.rotation_gauche(noeud)
        
        return noeud