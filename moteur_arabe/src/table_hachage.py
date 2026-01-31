# -*- coding: utf-8 -*-
class EntreeScheme:
    """Une entrée dans la table de hachage"""
    
    def __init__(self, cle, pattern, description):
        self.cle = cle          # Nom du schème (ex: "فاعل")
        self.pattern = pattern  # Pattern (ex: "C1اC2C3")
        self.description = description
        self.suivant = None     # Pour chaînage

class TableHachage:
    """Table de hachage pour les schèmes morphologiques"""
    
    def __init__(self, taille=31):
        self.taille = taille
        self.table = [None] * taille
    
    def hachage(self, cle):
        """Fonction de hachage simple"""
        total = 0
        for char in cle:
            total += ord(char)
        return total % self.taille
    
    def inserer(self, cle, pattern, description):
        """Insère un nouveau schème"""
        index = self.hachage(cle)
        nouvelle_entree = EntreeScheme(cle, pattern, description)
        
        if self.table[index] is None:
            self.table[index] = nouvelle_entree
        else:
            nouvelle_entree.suivant = self.table[index]
            self.table[index] = nouvelle_entree
        
        print(f"✅ Schème '{cle}' ajouté")
    
    def rechercher(self, cle):
        """Recherche un schème par sa clé"""
        index = self.hachage(cle)
        entree = self.table[index]
        
        while entree:
            if entree.cle == cle:
                return entree
            entree = entree.suivant
        
        return None
    
    def afficher_tous(self):
        """Affiche tous les schèmes"""
        print("\n=== SCHÈMES DISPONIBLES ===")
        count = 0
        
        for i in range(self.taille):
            entree = self.table[i]
            while entree:
                print(f"🔸 {entree.cle}: {entree.description}")
                print(f"   Pattern: {entree.pattern}")
                print()
                entree = entree.suivant
                count += 1
        
        if count == 0:
            print("Aucun schème disponible")
        else:
            print(f"Total: {count} schème(s)")
    
    def charger_depuis_fichier(self, nom_fichier):
        """Charge les schèmes depuis un fichier"""
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if not ligne or ligne.startswith('#'):
                        continue
                    
                    parts = ligne.split('|')
                    if len(parts) >= 2:
                        cle = parts[0].strip()
                        pattern = parts[1].strip()
                        description = parts[2].strip() if len(parts) > 2 else "Pas de description"
                        self.inserer(cle, pattern, description)
            
            print(f"✅ Schèmes chargés depuis '{nom_fichier}'")
        except FileNotFoundError:
            print(f"⚠️  Fichier '{nom_fichier}' non trouvé. Chargement des schèmes par défaut.")
            self.charger_schemes_par_defaut()
    
    def charger_schemes_par_defaut(self):
        """Charge les schèmes de base"""
        schemes = [
            ("فاعل", "C1اC2C3", "nom d'agent (celui qui fait l'action)"),
            ("مفعول", "مC1C2وC3", "participe passif (ce qui subit l'action)"),
            ("يفعل", "يC1C2C3", "verbe au présent"),
            ("افعل", "اC1C2C3", "impératif"),
            ("تفعيل", "تC1C2يC3", "nom d'action (masdar)"),
            ("مفعل", "مC1C2C3", "lieu ou instrument"),
            ("فعلان", "C1C2C3ان", "intensité ou expansion"),
        ]
        
        for cle, pattern, description in schemes:
            self.inserer(cle, pattern, description)