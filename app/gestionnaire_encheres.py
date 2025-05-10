from datetime import datetime
from app import db
from app.models import Enchere
from app.services.enchere_service import verifier_statut_enchere, determiner_gagnant_enchere

def verifier_toutes_encheres():
    """
    Vérifie et met à jour le statut de toutes les enchères.
    Détermine les gagnants pour les enchères terminées.
    """
    try:
        # Récupérer les enchères non terminées
        encheres_actives = Enchere.query.filter(
            Enchere.statut != 'terminee'
        ).all()

        for enchere in encheres_actives:
            if verifier_statut_enchere(enchere):
                determiner_gagnant_enchere(enchere)
                print(f"Enchère {enchere.id_enchere} traitée")

        print("Vérification des enchères terminée")
        return True

    except Exception as e:
        print(f"Erreur lors de la vérification des enchères : {e}")
        db.session.rollback()
        return False