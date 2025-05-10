from app import db
from app.models import Mise, Notification, Enchere
from sqlalchemy import func
from datetime import datetime
from decimal import Decimal
import traceback

def verifier_statut_enchere(enchere):
    """
    Vérifie et met à jour le statut d'une enchère si elle est terminée.
    Retourne True si l'enchère est terminée, False sinon.
    """
    try:
        now = datetime.utcnow()
        
        # Si déjà terminée
        if enchere.statut == 'terminee':
            return True
            
        # Si la date de fin est dépassée
        if enchere.date_fin <= now:
            enchere.statut = 'terminee'
            db.session.commit()
            print(f"Enchère {enchere.id_enchere} marquée comme terminée")
            return True
            
        return False

    except Exception as e:
        print(f"Erreur lors de la vérification du statut: {e}")
        db.session.rollback()
        return False

def get_mises_valides(enchere):
    """
    Récupère toutes les mises valides (non remboursées) pour une enchère.
    """
    try:
        mises = Mise.query.filter_by(
            enchere_id=enchere.id_enchere,
            remboursee=False
        ).order_by(Mise.prix_propose).all()
        return mises
    except Exception as e:
        print(f"Erreur lors de la récupération des mises: {e}")
        return []

def trouver_prix_unique_plus_bas(mises):
    """
    Trouve la mise avec le prix unique le plus bas parmi toutes les mises.
    """
    try:
        if not mises:
            return None

        # Compter les occurrences de chaque prix
        prix_uniques = {}
        for mise in mises:
            prix_uniques[mise.prix_propose] = prix_uniques.get(mise.prix_propose, 0) + 1

        # Trouver la première mise avec un prix unique
        for mise in mises:  # Les mises sont déjà triées par prix croissant
            if prix_uniques[mise.prix_propose] == 1:
                return mise
        return None
    except Exception as e:
        print(f"Erreur lors de la recherche du prix unique: {e}")
        return None

def enregistrer_gagnant(enchere, mise_gagnante):
    try:
        with db.session.begin_nested():  # Utiliser une transaction imbriquée
            # Mettre à jour l'enchère
            enchere.statut = 'terminee'
            enchere.prix_gagnant = mise_gagnante.prix_propose  # Pas besoin de conversion Decimal
            enchere.gagnant_id = mise_gagnante.utilisateur_id
            db.session.flush()  # Forcer la mise à jour
            
            # Créer et ajouter la notification
            notification = Notification(
                utilisateur_id=mise_gagnante.utilisateur_id,
                message=f"Félicitations ! Vous avez gagné l'enchère sur le produit '{enchere.produit.nom_produit}' pour {mise_gagnante.prix_propose}€.",
                type_notification='success',
                lue=False,
                date_creation=datetime.utcnow()
            )
            db.session.add(notification)
            db.session.flush()
            
        # Commit final
        db.session.commit()
        
        # Vérification post-commit
        db.session.refresh(enchere)
        if not enchere.prix_gagnant or not enchere.gagnant_id:
            raise ValueError("Prix gagnant ou gagnant_id manquant après commit")
            
        print(f"Gagnant enregistré - Enchère {enchere.id_enchere}:")
        print(f"  - Prix: {enchere.prix_gagnant}€")
        print(f"  - Gagnant ID: {enchere.gagnant_id}")
        return True
            
    except Exception as e:
        print(f"Erreur d'enregistrement du gagnant: {str(e)}")
        traceback.print_exc()
        db.session.rollback()
        return False

    
def determiner_gagnant_enchere(enchere):
    try:
        if enchere.gagnant_id is not None:
            print(f"L'enchère {enchere.id_enchere} a déjà un gagnant (prix: {enchere.prix_gagnant}€)")
            return False

        mises = get_mises_valides(enchere)
        if not mises:
            print(f"Aucune mise pour l'enchère {enchere.id_enchere}")
            enchere.statut = 'terminee'
            db.session.commit()
            return False

        mise_gagnante = trouver_prix_unique_plus_bas(mises)
        if mise_gagnante:
            print(f"Mise gagnante trouvée: {mise_gagnante.prix_propose}€")
            return enregistrer_gagnant(enchere, mise_gagnante)

        print(f"Pas de prix unique pour l'enchère {enchere.id_enchere}")
        enchere.statut = 'terminee'
        db.session.commit()
        return False

    except Exception as e:
        print(f"Erreur détermination gagnant: {e}")
        traceback.print_exc()
        db.session.rollback()
        return False