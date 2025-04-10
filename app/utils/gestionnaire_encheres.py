from datetime import datetime
from app import db
from app.models import Enchere, Utilisateur

def verifier_encheres_expirees():
    """
    Vérifie les enchères expirées et met à jour les gagnants.
    """
    # Récupérer toutes les enchères expirées
    enchères_expirées = Enchere.query.filter(Enchere.date_fin < datetime.utcnow(), Enchere.gagnant_id == None).all()

    for enchere in enchères_expirées:
        # Déterminer le gagnant (si applicable)
        if enchere.prix_actuel > 0:
            # Supposons que le gagnant est déterminé par une relation avec l'utilisateur
            gagnant = Utilisateur.query.get(enchere.gagnant_id)
            enchere.gagnant_id = gagnant.id_utilisateur
            db.session.add(enchere)
            print(f"Enchère {enchere.id} gagnée par l'utilisateur {gagnant.nom} {gagnant.prenom}.")
        else:
            print(f"Enchère {enchere.id} n'a pas de gagnant.")

    # Appliquer les changements à la base de données
    db.session.commit()
    print("Mise à jour des enchères expirées terminée.")

def annuler_enchere(enchere_id):
    """
    Annule une enchère spécifique.
    """
    enchere = Enchere.query.get(enchere_id)
    if enchere:
        db.session.delete(enchere)
        db.session.commit()
        print(f"Enchère {enchere_id} annulée avec succès.")
    else:
        print(f"Aucune enchère trouvée avec l'ID {enchere_id}.")