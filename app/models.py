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
    
    # Relations
    mises = db.relationship('Mise', backref='utilisateur', lazy=True)

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
    
    def __repr__(self):
        return f"<Produit {self.nom_produit}>"

class Enchere(db.Model):
    id_enchere = db.Column(db.Integer, primary_key=True)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id_produit'), nullable=False)
    date_debut = db.Column(db.DateTime, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime, nullable=False)
    jetons_requis = db.Column(db.Integer, nullable=False)
    statut = db.Column(db.Enum('ouverte', 'terminee'), default='ouverte')
    gagnant_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=True)
    prix_depart = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relations
    produit = db.relationship('Produit', backref='encheres')
    mises = db.relationship('Mise', backref='enchere', lazy=True)
    utilisateur_gagnant = db.relationship(
        'Utilisateur', 
        foreign_keys=[gagnant_id],
        backref=db.backref('encheres_gagnees', lazy=True)
    )

    def __repr__(self):
        return f"<Enchere #{self.id_enchere} - Produit: {self.produit.nom_produit}>"


class Mise(db.Model):
    id_mise = db.Column(db.Integer, primary_key=True)
    enchere_id = db.Column(db.Integer, db.ForeignKey('enchere.id_enchere'), nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    prix_propose = db.Column(db.Numeric(10, 2), nullable=False)
    date_mise = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Mise de {self.utilisateur.prenom} sur enchère #{self.enchere_id}: {self.prix_propose}€>"


class PackJetons(db.Model):
    __tablename__ = 'packjetons'
    id_pack = db.Column(db.Integer, primary_key=True)
    nom_pack = db.Column(db.String(50), nullable=False)
    nombre_jetons = db.Column(db.Integer, nullable=False)
    prix_pack = db.Column(db.Numeric(10, 2), nullable=False)
    
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
    