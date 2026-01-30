class NoeudABR:
    """Nœud pour l'arbre binaire de recherche stockant une racine arabe"""
    def __init__(self, racine):
        self.racine = racine  # Chaîne de 3 caractères arabes
        self.gauche = None
        self.droit = None
        self.derives = []  # Liste des mots dérivés validés
        self.freq = 0      # Fréquence d'apparition (optionnel)


class ArbreABR:
    """Arbre Binaire de Recherche pour l'indexation des racines arabes"""
    
    def __init__(self):
        self.racine = None
    
    def inserer(self, racine_str):
        """Insère une nouvelle racine dans l'arbre (itératif)"""
        nouveau_noeud = NoeudABR(racine_str)
        
        if self.racine is None:
            self.racine = nouveau_noeud
            return
        
        courant = self.racine
        parent = None
        
        while courant is not None:
            parent = courant
            # Comparaison lexicographique arabe
            if racine_str < courant.racine:
                courant = courant.gauche
            elif racine_str > courant.racine:
                courant = courant.droit
            else:
                # Racine déjà présente
                return
        
        # Insère à la bonne position
        if racine_str < parent.racine:
            parent.gauche = nouveau_noeud
        else:
            parent.droit = nouveau_noeud
    
    def rechercher(self, racine_str):
        """Recherche une racine dans l'arbre (itératif)"""
        courant = self.racine
        
        while courant is not None:
            if racine_str == courant.racine:
                return courant
            elif racine_str < courant.racine:
                courant = courant.gauche
            else:
                courant = courant.droit
        
        return None  # Non trouvé
    
    # CORRECTION DES MÉTHODES RÉCURSIVES
    
    def _afficher_infixe(self, noeud):
        """Méthode interne récursive"""
        if noeud:
            self._afficher_infixe(noeud.gauche)
            print(f"Racine: {noeud.racine}, Dérivés: {len(noeud.derives)}")
            self._afficher_infixe(noeud.droit)
    
    def afficher_infixe(self):
        """Parcours infixe pour afficher les racines triées"""
        print("Racines dans l'arbre (triées) :")
        self._afficher_infixe(self.racine)
    
    def _afficher_arbre(self, noeud, prefix="", est_gauche=True):
        """Méthode interne pour affichage hiérarchique"""
        if noeud is None:
            return
        
        if noeud.droit:
            self._afficher_arbre(noeud.droit, prefix + ("│   " if est_gauche else "    "), False)
        
        print(prefix + ("└── " if est_gauche else "┌── ") + noeud.racine)
        
        if noeud.gauche:
            self._afficher_arbre(noeud.gauche, prefix + ("    " if est_gauche else "│   "), True)
    
    def afficher_arbre(self):
        """Affiche l'arbre de manière hiérarchique (pour debug)"""
        if self.racine is None:
            print("Arbre vide")
            return
        self._afficher_arbre(self.racine)
    
    def ajouter_derive(self, racine_str, mot_derive):
        """Ajoute un mot dérivé à une racine"""
        noeud = self.rechercher(racine_str)
        if noeud:
            if mot_derive not in noeud.derives:
                noeud.derives.append(mot_derive)
                noeud.freq += 1
            return True
        return False
    
    def get_derives(self, racine_str):
        """Récupère la liste des dérivés d'une racine"""
        noeud = self.rechercher(racine_str)
        if noeud:
            return noeud.derives.copy()  # Retourne une copie
        return []
    
    def _hauteur(self, noeud):
        """Méthode interne récursive"""
        if noeud is None:
            return 0
        return 1 + max(self._hauteur(noeud.gauche), self._hauteur(noeud.droit))
    
    def hauteur(self):
        """Calcule la hauteur de l'arbre"""
        return self._hauteur(self.racine)
    
    def _taille(self, noeud):
        """Méthode interne récursive"""
        if noeud is None:
            return 0
        return 1 + self._taille(noeud.gauche) + self._taille(noeud.droit)
    
    def taille(self):
        """Compte le nombre de nœuds dans l'arbre"""
        return self._taille(self.racine)
    
    def _parcours_prefixe(self, noeud):
        """Méthode interne"""
        if noeud:
            print(noeud.racine, end=" ")
            self._parcours_prefixe(noeud.gauche)
            self._parcours_prefixe(noeud.droit)
    
    def parcours_prefixe(self):
        """Parcours préfixe (racine, gauche, droit)"""
        self._parcours_prefixe(self.racine)
    
    def _parcours_postfixe(self, noeud):
        """Méthode interne"""
        if noeud:
            self._parcours_postfixe(noeud.gauche)
            self._parcours_postfixe(noeud.droit)
            print(noeud.racine, end=" ")
    
    def parcours_postfixe(self):
        """Parcours postfixe (gauche, droit, racine)"""
        self._parcours_postfixe(self.racine)