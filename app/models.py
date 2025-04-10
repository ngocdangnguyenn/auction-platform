from datetime import datetime, timezone
datetime.now(timezone.utc)
from flask_login import UserMixin
from sqlalchemy import func
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Utilisateur(db.Model, UserMixin):
    id_utilisateur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    adresse = db.Column(db.Text)
    code_postal = db.Column(db.String(10))
    pays = db.Column(db.String(100), default="France")
    ville = db.Column(db.String(100))
    telephone = db.Column(db.String(20), nullable=False)
    solde_jetons = db.Column(db.Integer, default=5)  # 5 jetons offerts à l'inscription
    role = db.Column(db.Enum('client', 'admin'), default='client')
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    est_suspendu = db.Column(db.Boolean, default=False)
    
    # Relations
    mises = db.relationship('Mise', backref='utilisateur', lazy=True)
    transactions = db.relationship('Transaction', backref='utilisateur', lazy=True)
    encheres_gagnees = db.relationship('Enchere', backref='gagnant', lazy=True, foreign_keys='Enchere.gagnant_id')

    def get_id(self):
        return str(self.id_utilisateur)
    
    def __repr__(self):
        return f"<Utilisateur {self.prenom} {self.nom}>"
    
    def set_password(self, password):
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)


class Produit(db.Model):
    __tablename__ = 'produit'
    id_produit = db.Column(db.Integer, primary_key=True)
    nom_produit = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    prix_produit = db.Column(db.Numeric(10, 2), nullable=False)
    photo_url = db.Column(db.String(255))
    categorie = db.Column(db.String(50), nullable=False)  # Ajout d'une catégorie pour filtrer les produits
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Produit {self.nom_produit}>"

from datetime import datetime
from sqlalchemy import func
# Assure-toi que Notification et Mise sont importés ou disponibles dans le module

class Enchere(db.Model):
    id_enchere = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id_produit'), nullable=False)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime, nullable=False)
    jetons_requis = db.Column(db.Integer, nullable=False)  # Changé en Integer pour simplifier
    statut = db.Column(
    db.Enum('ouverte', 'terminee', 'annulee', name="statut_enum"),
    default='ouverte',
    nullable=False)
    gagnant_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    prix_gagnant = db.Column(db.Numeric(10, 2), nullable=True)
    prix_depart = db.Column(db.Numeric(10, 2), nullable=False)  # Prix proposé par le gagnant
    
    # Relations
    produit = db.relationship('Produit', backref='encheres')
    mises = db.relationship('Mise', backref='enchere', lazy=True)
    
    def __repr__(self):
        return f"<Enchere #{self.id_enchere} - Produit: {self.produit.nom_produit}>"
    
    def determine_gagnant(self):
        """Détermine le gagnant de l'enchère (prix unique le plus bas)."""
        try:
            # Étape 1 : Trouver les prix uniques proposés
            subquery = db.session.query(
                Mise.prix_propose,
                func.count(Mise.prix_propose).label('count')
            ).filter(Mise.enchere_id == self.id_enchere).group_by(Mise.prix_propose).subquery()

            # Étape 2 : Sélectionner le prix unique le plus bas
            unique_min_price = db.session.query(subquery.c.prix_propose)\
                .filter(subquery.c.count == 1)\
                .order_by(subquery.c.prix_propose)\
                .first()

            if unique_min_price:
                # Étape 3 : Trouver l'utilisateur qui a proposé ce prix
                mise_gagnante = Mise.query.filter_by(
                    enchere_id=self.id_enchere, 
                    prix_propose=unique_min_price[0]
                ).first()

                # Vérification pour éviter les erreurs
                if not mise_gagnante:
                    print(f"Aucune mise gagnante trouvée pour l'enchère {self.id_enchere}.")
                    self.statut = 'terminee'
                    db.session.commit()
                    return False

                # Étape 4 : Mettre à jour les champs de l'enchère
                self.gagnant_id = mise_gagnante.utilisateur_id
                self.prix_gagnant = mise_gagnante.prix_propose
                self.statut = 'terminee'

                # Étape 5 : Créer une notification pour le gagnant
                notification = Notification(
                    utilisateur_id=mise_gagnante.utilisateur_id,
                    message=f"Félicitations ! Vous avez gagné l'enchère sur le produit '{self.produit.nom_produit}'.",
                    date_creation=datetime.utcnow(),
                    lue=False,
                    type_notification='unique'
                )
                db.session.add(notification)
                db.session.commit()

                print(f"Notification créée pour l'utilisateur {mise_gagnante.utilisateur_id} : {notification.message}")
                # Retourne l'ID du gagnant pour faciliter le débogage
                return mise_gagnante.utilisateur_id
            else:
                # Aucun prix unique trouvé
                print(f"Aucun prix unique trouvé pour l'enchère {self.id_enchere}.")
                self.statut = 'terminee'
                db.session.commit()
                return False

        except Exception as e:
            print(f"Erreur lors de la détermination du gagnant pour l'enchère {self.id_enchere} : {e}")
            return False

def verifier_encheres_terminees():
    """Parcourt toutes les enchères qui devraient être terminées et détermine leur gagnant."""
    now = datetime.utcnow()
    encheres_terminees = Enchere.query.filter(
        Enchere.date_fin < now,
        Enchere.statut == 'ouverte'
    ).all()
    
    for enchere in encheres_terminees:
        result = enchere.determine_gagnant()
        if result:
            print(f"Enchère {enchere.id_enchere} : Gagnant déterminé (ID utilisateur {result}).")
        else:
            print(f"Enchère {enchere.id_enchere} : Aucun gagnant ou erreur lors de la détermination.")

class Mise(db.Model):
    id_mise = db.Column(db.Integer, primary_key=True)
    enchere_id = db.Column(db.Integer, db.ForeignKey('enchere.id_enchere'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    prix_propose = db.Column(db.Numeric(10, 2), nullable=False)
    date_mise = db.Column(db.DateTime, default=datetime.utcnow)
    jetons_utilises = db.Column(db.Integer, nullable=False)
    remboursee = db.Column(db.Boolean, default=False)  # Pour suivre si la mise a été remboursée
    
    def __repr__(self):
        return f"<Mise de {self.utilisateur.prenom} sur enchère #{self.enchere_id}: {self.prix_propose}€>"

class PackJetons(db.Model):
    __tablename__ = 'packjetons'
    id_pack = db.Column(db.Integer, primary_key=True)
    nom_pack = db.Column(db.String(50), nullable=False)
    nombre_jetons = db.Column(db.Integer, nullable=False)
    prix_pack = db.Column(db.Numeric(10, 2), nullable=False)
    actif = db.Column(db.Boolean, default=True)  # Pour permettre de désactiver un pack
    
    # Relations
    transactions = db.relationship('Transaction', backref='pack', lazy=True)
    
    def __repr__(self):
        return f"<PackJetons {self.nom_pack}: {self.nombre_jetons} jetons pour {self.prix_pack}€>"

class Transaction(db.Model):
    id_transaction = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    pack_id = db.Column(db.Integer, db.ForeignKey('packjetons.id_pack'), nullable=True)  # Peut être null pour les jetons gratuits
    date_transaction = db.Column(db.DateTime, default=datetime.utcnow)
    nombre_jetons = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Numeric(10, 2), nullable=True)  # Peut être null pour les jetons gratuits
    type_transaction = db.Column(db.Enum('achat', 'utilisation', 'remboursement', 'offert'), nullable=False)
    
    def __repr__(self):
        return f"<Transaction {self.type_transaction} de {self.nombre_jetons} jetons pour {self.utilisateur.prenom}>"

class Remboursement(db.Model):
    id_remboursement = db.Column(db.Integer, primary_key=True)
    enchere_id = db.Column(db.Integer, db.ForeignKey('enchere.id_enchere'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    montant_jetons = db.Column(db.Integer, nullable=False)
    date_remboursement = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    enchere = db.relationship('Enchere')
    utilisateur = db.relationship('Utilisateur')
    
    def __repr__(self):
        return f"<Remboursement de {self.montant_jetons} jetons à {self.utilisateur.prenom} pour l'enchère #{self.enchere_id}>"
    
class Notification(db.Model):
    id_notification = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date_creation = db.Column(db.DateTime, default=db.func.now())
    lue = db.Column(db.Boolean, default=False)  # False = Non lue
    type_notification = db.Column(db.Enum('unique', 'groupe', 'tous'), nullable=False, default='unique')

    def __repr__(self):
        return f"<Notification pour {self.utilisateur_id}: {self.message}>"