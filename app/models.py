from datetime import datetime
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
    solde_jetons = db.Column(db.Integer, default=5)
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
    categorie = db.Column(db.String(50), nullable=False)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Produit {self.nom_produit}>"

class Enchere(db.Model):
    id_enchere = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id_produit'), nullable=False)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime, nullable=False)
    jetons_requis = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.Enum('ouverte', 'terminee', 'annulee'), default='ouverte')
    gagnant_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    prix_gagnant = db.Column(db.Numeric(10, 2), nullable=True)
    prix_depart = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relations
    produit = db.relationship('Produit', backref='encheres')
    mises = db.relationship('Mise', backref='enchere', lazy=True)

    def __repr__(self):
        return f"<Enchere #{self.id_enchere} - Produit: {self.produit.nom_produit}>"
    
    def determine_gagnant(self):
        """Détermine le gagnant de l'enchère"""
        from app.services.enchere_service import determiner_gagnant_enchere
        return determiner_gagnant_enchere(self)


class Mise(db.Model):
    id_mise = db.Column(db.Integer, primary_key=True)
    enchere_id = db.Column(db.Integer, db.ForeignKey('enchere.id_enchere'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    prix_propose = db.Column(db.Numeric(10, 2), nullable=False)
    date_mise = db.Column(db.DateTime, default=datetime.utcnow)
    jetons_utilises = db.Column(db.Integer, nullable=False)
    remboursee = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Mise de {self.utilisateur.prenom} sur enchère #{self.enchere_id}: {self.prix_propose}€>"


class PackJetons(db.Model):
    __tablename__ = 'packjetons'
    id_pack = db.Column(db.Integer, primary_key=True)
    nom_pack = db.Column(db.String(50), nullable=False)
    nombre_jetons = db.Column(db.Integer, nullable=False)
    prix_pack = db.Column(db.Numeric(10, 2), nullable=False)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    transactions = db.relationship('Transaction', backref='pack', lazy=True)
    
    def __repr__(self):
        return f"<PackJetons {self.nom_pack}: {self.nombre_jetons} jetons pour {self.prix_pack}€>"


class Notification(db.Model):
    id_notification = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date_creation = db.Column(db.DateTime, default=db.func.now())
    lue = db.Column(db.Boolean, default=False)
    type_notification = db.Column(db.Enum('unique', 'groupe', 'tous'), nullable=False, default='unique')

    def __repr__(self):
        return f"<Notification pour {self.utilisateur_id}: {self.message}>"
    
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