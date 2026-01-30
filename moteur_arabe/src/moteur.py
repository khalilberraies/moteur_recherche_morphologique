#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MoteurMorphologique:
    """
    Moteur principal pour la génération et validation morphologique arabe.
    Combine un arbre ABR (racines) et une table de hachage (schèmes).
    """
    
    def __init__(self, arbre_racines, table_schemas):
        """
        Initialise le moteur avec les structures de données.
        
        Args:
            arbre_racines: Instance de ArbreABR pour les racines
            table_schemas: Instance de TableHachage pour les schèmes
        """
        self.arbre_racines = arbre_racines
        self.table_schemas = table_schemas
        
        # Cache pour les résultats de génération fréquents
        self.cache_generation = {}
    
    def generer_mot(self, racine_str, schema_nom):
        """
        Génère un mot arabe à partir d'une racine et d'un schème.
        
        Args:
            racine_str (str): Racine trilitère arabe (ex: "كتب")
            schema_nom (str): Nom du schème (ex: "فاعل")
        
        Returns:
            tuple: (mot_généré ou None, message_d'erreur)
        """
        # Vérifier le cache d'abord
        cache_key = (racine_str, schema_nom)
        if cache_key in self.cache_generation:
            return self.cache_generation[cache_key], " (depuis cache)"
        
        # 1. Vérifier que la racine existe
        racine_node = self.arbre_racines.rechercher(racine_str)
        if not racine_node:
            return None, "❌ Racine non trouvée dans l'arbre"
        
        # 2. Vérifier que le schème existe
        schema = self.table_schemas.obtenir(schema_nom)
        if not schema:
            return None, "❌ Schème non trouvé dans la table"
        
        # 3. Générer le mot selon le modèle
        mot_genere = self._appliquer_modele(racine_str, schema.modele)
        
        if not mot_genere:
            return None, "❌ Échec de la génération du mot"
        
        # 4. Ajouter aux dérivés de la racine
        self.arbre_racines.ajouter_derive(racine_str, mot_genere)
        
        # 5. Mettre en cache
        self.cache_generation[cache_key] = mot_genere
        
        return mot_genere, "✅ Mot généré avec succès"
    
    def _appliquer_modele(self, racine, modele):
        """
        Applique un modèle abstrait à une racine trilitère.
        
        Exemples:
            racine="كتب", modele="1a23" → "كاتب"
            racine="كتب", modele="ma123" → "مكتوب"
        
        Args:
            racine (str): Racine de 3 lettres arabes
            modele (str): Modèle abstrait (ex: "1a23", "ma123")
        
        Returns:
            str: Mot généré
        """
        if len(racine) != 3:
            # Pour l'instant, on suppose racines trilittères
            # Plus tard: gérer racines bilittères, quadrilittères
            return racine
        
        # Dictionnaire de correspondances modèle → lettres arabes
        correspondances = {
            '1': racine[0],  # Première consonne de la racine
            '2': racine[1],  # Deuxième consonne
            '3': racine[2],  # Troisième consonne
            'a': 'ا',        # Alif
            'i': 'ي',        # Ya
            'u': 'و',        # Waw
            'm': 'م',        # Mim
            't': 'ت',        # Ta
            'n': 'ن',        # Nun
            's': 'س',        # Sin
            'y': 'ي',        # Ya (variante)
            'w': 'و',        # Waw (variante)
        }
        
        # Construire le mot caractère par caractère
        resultat = []
        for char in modele:
            if char in correspondances:
                resultat.append(correspondances[char])
            else:
                # Caractère littéral (peut-être une voyelle diacritique)
                resultat.append(char)
        
        return ''.join(resultat)
    
    def valider_mot(self, mot, racine_str):
        """
        Valide si un mot appartient morphologiquement à une racine.
        
        Args:
            mot (str): Mot arabe à valider
            racine_str (str): Racine supposée
        
        Returns:
            tuple: (bool_validité, message, nom_schème_identifié)
        """
        # 1. Vérifier que la racine existe
        racine_node = self.arbre_racines.rechercher(racine_str)
        if not racine_node:
            return False, "❌ Racine non trouvée", None
        
        # 2. Vérifier si le mot est déjà dans les dérivés validés
        if mot in racine_node.derives:
            return True, "✅ Mot déjà validé (dans les dérivés)", "Schème inconnu"
        
        # 3. Essayer d'identifier le schème
        schema_trouve = self._identifier_schema(mot, racine_str)
        if schema_trouve:
            # Ajouter aux dérivés
            self.arbre_racines.ajouter_derive(racine_str, mot)
            return True, f"✅ Mot validé - Schème: {schema_trouve.nom}", schema_trouve.nom
        
        return False, "❌ Mot non reconnu comme dérivé de cette racine", None
    
    def _identifier_schema(self, mot, racine):
        """
        Tente d'identifier le schème utilisé pour former un mot.
        Version simplifiée pour commencer.
        
        Args:
            mot (str): Mot à analyser
            racine (str): Racine supposée (3 lettres)
        
        Returns:
            Schema ou None: Schème identifié
        """
        if len(racine) != 3 or len(mot) < 3:
            return None
        
        # Pour chaque schème dans la table, essayer de l'appliquer
        for bucket in self.table_schemas.table:
            for _, schema in bucket:
                # Générer le mot avec ce schème
                mot_test = self._appliquer_modele(racine, schema.modele)
                if mot_test == mot:
                    return schema
        
        return None
    
    def charger_racines_fichier(self, chemin="data/racines.txt"):
        """
        Charge les racines depuis un fichier texte.
        
        Args:
            chemin (str): Chemin vers le fichier
        
        Returns:
            bool: Succès ou échec
        """
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                compteur = 0
                for ligne in f:
                    racine = ligne.strip()
                    # Ignorer lignes vides et commentaires
                    if racine and not racine.startswith('#'):
                        self.arbre_racines.inserer(racine)
                        compteur += 1
                print(f"✅ {compteur} racines chargées depuis {chemin}")
                return True
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {chemin}")
            return False
        except Exception as e:
            print(f"❌ Erreur de lecture: {e}")
            return False
    
    def charger_schemas_fichier(self, chemin="data/schemas.txt"):
        """
        Charge les schèmes depuis un fichier texte.
        
        Args:
            chemin (str): Chemin vers le fichier
        
        Returns:
            bool: Succès ou échec
        """
        from src.table_hachage import Schema
        
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                compteur = 0
                for ligne in f:
                    ligne = ligne.strip()
                    # Ignorer lignes vides et commentaires
                    if ligne and not ligne.startswith('#'):
                        parts = ligne.split(':', 2)
                        if len(parts) >= 2:
                            nom = parts[0].strip()
                            modele = parts[1].strip()
                            description = parts[2].strip() if len(parts) > 2 else ""
                            self.table_schemas.ajouter(Schema(nom, modele, description))
                            compteur += 1
                print(f"✅ {compteur} schèmes chargés depuis {chemin}")
                return True
        except FileNotFoundError:
            print(f"❌ Fichier non trouvé: {chemin}")
            return False
        except Exception as e:
            print(f"❌ Erreur de lecture: {e}")
            return False
    
    def afficher_statistiques(self):
        """Affiche les statistiques du système."""
        print("\n" + "="*50)
        print("STATISTIQUES DU SYSTÈME")
        print("="*50)
        
        # Racines
        nb_racines = self.arbre_racines.taille()
        hauteur_arbre = self.arbre_racines.hauteur()
        print(f"📊 Racines: {nb_racines}")
        print(f"📐 Hauteur de l'arbre: {hauteur_arbre}")
        
        # Schèmes
        nb_schemas = 0
        for bucket in self.table_schemas.table:
            nb_schemas += len(bucket)
        print(f"🎯 Schèmes: {nb_schemas}")
        
        # Cache
        print(f"💾 Entrées en cache: {len(self.cache_generation)}")
        
        print("="*50)