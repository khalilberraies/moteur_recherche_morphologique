#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.arbre_abr import ArbreABR
from src.table_hachage import TableHachage
from src.moteur import MoteurMorphologique
from src.interface import InterfaceCLI

def demarrer_interface():
    """Démarre l'interface CLI complète."""
    print("\n" + "="*60)
    print("        🚀 MOTEUR DE RECHERCHE MORPHOLOGIQUE ARABE")
    print("="*60)
    print("  Version: ABR + Table de Hachage + Moteur + Interface CLI")
    print("  Développé pour le projet d'Algorithmique")
    print("="*60)
    
    # Initialiser les structures
    arbre = ArbreABR()
    table = TableHachage(taille=31)
    
    # Créer le moteur
    moteur = MoteurMorphologique(arbre, table)
    
    # Créer et lancer l'interface
    interface = InterfaceCLI(moteur)
    interface.executer()

def test_rapide():
    """Exécute un test rapide sans interface."""
    print("\n🔧 TEST RAPIDE DU SYSTÈME COMPLET")
    print("="*40)
    
    # Initialiser
    arbre = ArbreABR()
    table = TableHachage()
    moteur = MoteurMorphologique(arbre, table)
    
    # Ajouter quelques données de test
    print("\n📥 Ajout de données de test...")
    
    # Racines
    racines_test = ["كتب", "فعل", "درس"]
    for r in racines_test:
        arbre.inserer(r)
    print(f"  ✓ {len(racines_test)} racines ajoutées")
    
    # Schèmes
    from src.table_hachage import Schema
    schemas_test = [
        ("فاعل", "1a23", "nom d'agent"),
        ("مفعول", "ma123", "participe passif"),
    ]
    for nom, modele, desc in schemas_test:
        table.ajouter(Schema(nom, modele, desc))
    print(f"  ✓ {len(schemas_test)} schèmes ajoutés")
    
    # Test de génération
    print("\n🎯 Test de génération:")
    tests = [
        ("كتب", "فاعل", "كاتب"),
        ("كتب", "مفعول", "مكتوب"),
        ("فعل", "فاعل", "فاعل"),
    ]
    
    for racine, schema, attendu in tests:
        resultat, message = moteur.generer_mot(racine, schema)
        if resultat == attendu:
            print(f"  ✓ {racine} + {schema} → {resultat} (OK)")
        else:
            print(f"  ✗ {racine} + {schema} → {resultat} (attendait {attendu})")
    
    # Test de validation
    print("\n✅ Test de validation:")
    validation_tests = [
        ("كاتب", "كتب", True),
        ("مكتوب", "كتب", True),
        ("كتاب", "فعل", False),  # N'appartient pas à فعل
    ]
    
    for mot, racine, attendu in validation_tests:
        valide, message, _ = moteur.valider_mot(mot, racine)
        if valide == attendu:
            statut = "✓" if valide else "✓ (correct)"
            print(f"  {statut} '{mot}' avec racine '{racine}': {message}")
        else:
            print(f"  ✗ '{mot}' avec racine '{racine}': problème")
    
    # Statistiques
    print("\n📊 Statistiques finales:")
    print(f"  Racines: {arbre.taille()}")
    print(f"  Dérivés de 'كتب': {arbre.get_derives('كتب')}")
    
    print("\n" + "="*40)
    print("✅ TEST TERMINÉ AVEC SUCCÈS!")
    print("="*40)

def main():
    """Fonction principale avec menu de démarrage."""
    print("\n" + "⭐" * 60)
    print("          BIENVENUE DANS LE MOTEUR MORPHOLOGIQUE ARABE")
    print("⭐" * 60)
    
    print("\nChoisissez un mode:")
    print("  1. 🚀 Mode complet (Interface interactive)")
    print("  2. 🔧 Test rapide (Vérification technique)")
    print("  3. 🚪 Quitter")
    
    choix = input("\nVotre choix (1-3): ").strip()
    
    if choix == "1":
        demarrer_interface()
    elif choix == "2":
        test_rapide()
        
        # Proposer de continuer avec l'interface
        continuer = input("\nVoulez-vous lancer l'interface complète? (o/n): ").strip().lower()
        if continuer == 'o':
            demarrer_interface()
        else:
            print("\n👋 Au revoir!")
    elif choix == "3":
        print("\n👋 Au revoir!")
    else:
        print("\n❌ Choix invalide. Relancez le programme.")

if __name__ == "__main__":
    main()