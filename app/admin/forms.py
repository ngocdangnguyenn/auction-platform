from flask_wtf import FlaskForm
from wtforms import DateTimeField, SelectField, SelectMultipleField, StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class AjouterPackForm(FlaskForm):
    nom_pack = StringField('Nom du pack', validators=[DataRequired(), Length(min=2, max=100)])
    nombre_jetons = IntegerField('Nombre de jetons', validators=[DataRequired(), NumberRange(min=1)])
    prix_pack = DecimalField('Prix (€)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Ajouter')

class AjouterProduitForm(FlaskForm):
    nom_produit = StringField('Nom du produit', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=255)])
    prix_produit = DecimalField('Prix (€)', validators=[DataRequired(), NumberRange(min=0)])
    categorie = SelectField("Catégorie", choices=[
    ('Smartphones et accessoires', 'Smartphones et accessoires'),
    ('Informatique', 'Informatique'),
    ('Téléviseurs et home cinéma', 'Téléviseurs et home cinéma'),
    ('Audio', 'Audio'),
    ('Montres et objets connectés', 'Montres et objets connectés'),
    ('Gaming', 'Gaming'),
    ('Drones et photographie', 'Drones et photographie'),
    ('Réalité virtuelle et augmenté', 'Réalité virtuelle et augmentée')
], validators=[DataRequired()])
    photo_url = StringField("URL de la photo", validators=[Length(max=255)])
    submit = SubmitField('Ajouter')

from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class AjouterEnchereForm(FlaskForm):
    produit = SelectField("Produit", coerce=int, validators=[DataRequired()])
    date_debut = DateTimeField("Date de début", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    date_fin = DateTimeField("Date de fin", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    jetons_requis = IntegerField("Jetons requis", validators=[DataRequired()])
    prix_depart = DecimalField("Prix de départ (€)", validators=[DataRequired()])
    submit = SubmitField("Ajouter")

class ModifierEnchereForm(FlaskForm):
    produit = SelectField("Produit", coerce=int, validators=[DataRequired()])
    date_debut = DateTimeField("Date de début", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    date_fin = DateTimeField("Date de fin", format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    jetons_requis = IntegerField("Jetons requis", validators=[DataRequired()])
    prix_depart = DecimalField("Prix de départ (€)", validators=[DataRequired()])
    submit = SubmitField("Modifier")

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class ModifierProduitForm(FlaskForm):
    nom_produit = StringField("Nom du produit", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[DataRequired()])
    prix_produit = DecimalField("Prix (€)", validators=[DataRequired()])
    categorie = SelectField("Catégorie", choices=[
    ('Smartphones et accessoires', 'Smartphones et accessoires'),
    ('Informatique', 'Informatique'),
    ('Téléviseurs et home cinéma', 'Téléviseurs et home cinéma'),
    ('Audio', 'Audio'),
    ('Montres et objets connectés', 'Montres et objets connectés'),
    ('Gaming', 'Gaming'),
    ('Drones et photographie', 'Drones et photographie'),
    ('Réalité virtuelle et augmenté', 'Réalité virtuelle et augmentée')
], validators=[DataRequired()])
    photo_url = StringField("URL de la photo", validators=[Length(max=255)])
    submit = SubmitField("Modifier")

class ModifierPackForm(FlaskForm):
    nom_pack = StringField("Nom du pack", validators=[DataRequired(), Length(max=100)])
    nombre_jetons = IntegerField("Nombre de jetons", validators=[DataRequired()])
    prix_pack = DecimalField("Prix (€)", validators=[DataRequired()])
    submit = SubmitField("Modifier")

class AttribuerJetonsForm(FlaskForm):
    nombre_jetons = IntegerField(
        "Nombre de jetons",
        validators=[DataRequired(), NumberRange(min=1, message="Le nombre de jetons doit être au moins 1.")]
    )
    submit = SubmitField("Attribuer")

class EnvoyerNotificationForm(FlaskForm):
    utilisateurs = SelectMultipleField("Envoyer à", coerce=int)  # ID des utilisateurs
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Envoyer")