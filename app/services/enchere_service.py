from datetime import datetime
from app import db
from app.models import Mise, Enchere

def verifier_et_finaliser_enchere(enchere):
    """Vérifie le statut et détermine le gagnant d'une enchère"""
    try:
        # 1. Vérifier si l'enchère peut être traitée
        if enchere.date_fin > datetime.utcnow():
            print(f"Enchère {enchere.id_enchere} pas encore terminée")
            return False

        # 2. Forcer une actualisation de l'enchère depuis la base
        db.session.refresh(enchere)
        
        if enchere.statut == 'terminee' and enchere.gagnant_id is not None:
            print(f"Enchère {enchere.id_enchere} déjà finalisée")
            return False

        print(f"\n=== Traitement enchère {enchere.id_enchere} ===")

        # 3. Récupérer toutes les mises valides avec FOR UPDATE pour verrouiller
        mises = db.session.query(Mise).filter(
            Mise.enchere_id == enchere.id_enchere,
        ).order_by(Mise.prix_propose.asc()).with_for_update().all()

        if not mises:
            print("Aucune mise trouvée")
            enchere.statut = 'terminee'
            enchere.gagnant_id = None
            db.session.commit()
            return True

        # 4. Trouver le prix unique le plus bas
        prix_counts = {}
        for mise in mises:
            prix = float(mise.prix_propose)
            if prix not in prix_counts:
                prix_counts[prix] = []
            prix_counts[prix].append(mise)

        # 5. Identifier les prix uniques
        prix_uniques = []
        for prix, mises_prix in prix_counts.items():
            if len(mises_prix) == 1:
                prix_uniques.append((prix, mises_prix[0]))

        # 6. Déterminer le gagnant et mettre à jour l'enchère
        if prix_uniques:
            prix_gagnant, mise_gagnante = min(prix_uniques, key=lambda x: x[0])
            print(f"Prix gagnant: {prix_gagnant}€")
            print(f"Utilisateur gagnant: {mise_gagnante.utilisateur_id}")
            
            # Mise à jour atomique
            enchere.statut = 'terminee'
            enchere.gagnant_id = mise_gagnante.utilisateur_id
        else:
            print("Aucun prix unique trouvé")
            enchere.statut = 'terminee'
            enchere.gagnant_id = None

        # 7. Commit avec gestion des erreurs
        try:
            db.session.commit()
            print("Enchère finalisée avec succès")
            return True
        except Exception as commit_error:
            print(f"Erreur lors du commit: {str(commit_error)}")
            db.session.rollback()
            return False

    except Exception as e:
        print(f"Erreur générale: {str(e)}")
        db.session.rollback()
        return False
