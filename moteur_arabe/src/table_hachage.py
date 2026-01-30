class Schema:
    """Représente un schème morphologique arabe"""
    def __init__(self, nom, modele, description=""):
        self.nom = nom          # Ex: "فاعل"
        self.modele = modele    # Ex: "1a23" pour représentation abstraite
        self.description = description

class TableHachage:
    """Table de hachage pour stocker les schèmes morphologiques"""
    
    def __init__(self, taille=31):
        self.taille = taille
        self.table = [[] for _ in range(taille)]  # Résolution par chaînage
    
    def _hacher(self, cle):
        """Fonction de hachage pour chaînes Unicode"""
        total = 0
        for char in cle:
            total = (total * 31 + ord(char)) % self.taille
        return total
    
    def ajouter(self, schema):
        """Ajoute ou met à jour un schème"""
        index = self._hacher(schema.nom)
        
        # Vérifie si le schème existe déjà
        for i, (nom_existant, _) in enumerate(self.table[index]):
            if nom_existant == schema.nom:
                self.table[index][i] = (schema.nom, schema)
                return
        
        # Ajoute le nouveau schème
        self.table[index].append((schema.nom, schema))
    
    def obtenir(self, nom):
        """Récupère un schème par son nom"""
        index = self._hacher(nom)
        for nom_existant, schema in self.table[index]:
            if nom_existant == nom:
                return schema
        return None
    
    def supprimer(self, nom):
        """Supprime un schème"""
        index = self._hacher(nom)
        for i, (nom_existant, _) in enumerate(self.table[index]):
            if nom_existant == nom:
                del self.table[index][i]
                return True
        return False
    
    def afficher_tous(self):
        """Affiche tous les schèmes"""
        print(f"Schèmes dans la table ({self.taille} cases):")
        compteur = 0
        for i, bucket in enumerate(self.table):
            if bucket:
                print(f"  Case {i}:")
                for nom, schema in bucket:
                    print(f"    - {schema.nom}: {schema.modele} ({schema.description})")
                    compteur += 1
        print(f"Total: {compteur} schèmes")
    
    def charger_depuis_fichier(self, chemin):
        """Charge les schèmes depuis un fichier"""
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                for ligne in f:
                    ligne = ligne.strip()
                    if ligne and not ligne.startswith('#'):
                        parts = ligne.split(':', 2)
                        if len(parts) >= 2:
                            nom = parts[0].strip()
                            modele = parts[1].strip()
                            description = parts[2].strip() if len(parts) > 2 else ""
                            self.ajouter(Schema(nom, modele, description))
            return True
        except FileNotFoundError:
            print(f"Fichier non trouvé: {chemin}")
            return False