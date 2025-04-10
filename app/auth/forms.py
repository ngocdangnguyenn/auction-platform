from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class InscriptionForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=50)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirmation_mot_de_passe = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), EqualTo('mot_de_passe', message='Les mots de passe doivent correspondre.')
    ])
    adresse = StringField('Adresse', validators=[DataRequired(), Length(max=100)])
    code_postal = StringField('Code postal', validators=[DataRequired(), Length(max=10)])
    ville = StringField('Ville', validators=[DataRequired(), Length(max=50)])
    pays = StringField('Pays', validators=[DataRequired(), Length(max=50)])
    telephone = StringField('Téléphone', validators=[DataRequired(), Length(max=15)])
    submit = SubmitField('S\'inscrire')

class ConnexionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    se_souvenir = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')