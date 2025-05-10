from datetime import datetime
from app import db
from app.models import Mise

def verifier_et_finaliser_enchere(enchere):
    """Vérifie le statut et détermine le gagnant d'une enchère"""
    try:
        # Si déjà terminée, on sort
        if enchere.statut == 'terminee':
            return False

        # Si pas encore finie, on sort
        if enchere.date_fin > datetime.utcnow():
            return False

        # Requête SQL optimisée pour trouver le prix unique le plus bas
        subquery = db.session.query(
            Mise.prix_propose,
            db.func.count('*').label('count')
        ).filter(
            Mise.enchere_id == enchere.id_enchere,
            Mise.remboursee == False
        ).group_by(
            Mise.prix_propose
        ).having(
            db.func.count('*') == 1
        ).subquery()

        # Trouver la mise avec le prix unique le plus bas
        mise_gagnante = db.session.query(Mise).join(
            subquery,
            Mise.prix_propose == subquery.c.prix_propose
        ).filter(
            Mise.enchere_id == enchere.id_enchere
        ).order_by(
            Mise.prix_propose.asc()
        ).first()

        # Mettre à jour l'enchère
        enchere.statut = 'terminee'
        if mise_gagnante:
            enchere.gagnant_id = mise_gagnante.utilisateur_id
        
        db.session.commit()
        return True

    except Exception as e:
        print(f"Erreur: {str(e)}")
        db.session.rollback()
        return False