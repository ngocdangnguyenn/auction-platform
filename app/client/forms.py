from flask_wtf import FlaskForm
from wtforms import (
    DecimalField, 
    StringField, 
    PasswordField,
    SelectField, 
    SubmitField
)
from wtforms.validators import (
    DataRequired, 
    Email, 
    Length, 
    NumberRange, 
    EqualTo,
    ValidationError
)
from app.models import Enchere

class MonCompteForm(FlaskForm):
    """Formulaire pour mettre à jour les informations personnelles de l'utilisateur."""
    nom = StringField('Nom', validators=[
        DataRequired(), 
        Length(min=2, max=100)
    ])
    prenom = StringField('Prénom', validators=[
        DataRequired(), 
        Length(min=2, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    adresse = StringField('Adresse', validators=[
        DataRequired(), 
        Length(max=200)
    ])
    code_postal = StringField('Code postal', validators=[
        DataRequired(), 
        Length(max=10)
    ])
    ville = StringField('Ville', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    pays = StringField('Pays', validators=[
        DataRequired(), 
        Length(max=100)
    ])
    telephone = StringField('Téléphone', validators=[
        DataRequired(), 
        Length(max=20)
    ])
    submit = SubmitField('Mettre à jour')


class AcheterJetonsForm(FlaskForm):
    """Formulaire pour acheter des jetons."""
    pack_jetons = SelectField('Pack de jetons', 
        coerce=int, 
        validators=[DataRequired()]
    )
    submit = SubmitField('Acheter')


class PlacerEnchereForm(FlaskForm):
    """Formulaire pour placer une enchère."""
    montant = DecimalField('Montant de l\'enchère (€)', validators=[
        DataRequired(), 
        NumberRange(min=0.01)
    ])
    submit = SubmitField('Placer l\'enchère')

    def __init__(self, enchere_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enchere_id = enchere_id

    def validate_montant(self, field):
        enchere = Enchere.query.get(self.enchere_id)
        if enchere and field.data <= enchere.prix_depart:
            raise ValidationError(
                f"Le montant doit être supérieur au prix de départ ({enchere.prix_depart} €)."
            )


class ModifierMotDePasseForm(FlaskForm):
    """Formulaire pour modifier le mot de passe."""
    mot_de_passe_actuel = PasswordField("Mot de passe actuel", validators=[
        DataRequired(),
        Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères.")
    ])
    nouveau_mot_de_passe = PasswordField("Nouveau mot de passe", validators=[
        DataRequired(),
        Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères.")
    ])
    confirmer_mot_de_passe = PasswordField("Confirmer le nouveau mot de passe", validators=[
        DataRequired(),
        EqualTo('nouveau_mot_de_passe', message="Les mots de passe ne correspondent pas.")
    ])
    submit = SubmitField("Mettre à jour le mot de passe")


class MarquerLueForm(FlaskForm):
    """Formulaire pour marquer une notification comme lue."""
    submit = SubmitField("Marquer comme lue")