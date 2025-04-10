from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Utilisateur, Transaction
from app.auth.forms import InscriptionForm, ConnexionForm

auth = Blueprint('auth', __name__)

from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.auth.forms import InscriptionForm
from app.models import Utilisateur

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm()
    if form.validate_on_submit():
        print("Formulaire validé")  # Log pour vérifier si le formulaire est validé
        nouvel_utilisateur = Utilisateur(
            nom=form.nom.data,
            prenom=form.prenom.data,
            email=form.email.data,
            mot_de_passe=generate_password_hash(form.mot_de_passe.data),  # Hash le mot de passe
            adresse=form.adresse.data,
            code_postal=form.code_postal.data,
            pays=form.pays.data,
            ville=form.ville.data,
            telephone=form.telephone.data
        )
        try:
            db.session.add(nouvel_utilisateur)
            print("Utilisateur ajouté à la session")  # Log pour vérifier l'ajout
            db.session.commit()
            print("Utilisateur enregistré dans la base de données")  # Log pour vérifier l'enregistrement
            flash("Votre inscription a été effectuée avec succès !", "success")
            return redirect(url_for('auth.connexion'))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de l'inscription : {e}")  # Log pour afficher l'erreur
            flash("Une erreur s'est produite lors de l'inscription.", "danger")
    return render_template('auth/inscription.html', form=form)


@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ConnexionForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(email=form.email.data).first()
        
        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        if utilisateur and check_password_hash(utilisateur.mot_de_passe, form.mot_de_passe.data):
            login_user(utilisateur, remember=form.se_souvenir.data)
            next_page = request.args.get('next')
            
            # Rediriger selon le rôle de l'utilisateur
            if not next_page or not next_page.startswith('/'):
                if utilisateur.role == 'admin':
                    next_page = url_for('admin.dashboard')  # Vérifiez que cet endpoint existe
                elif utilisateur.role == 'client':
                    next_page = url_for('client.dashboard')  # Vérifiez que cet endpoint existe
                else:
                    next_page = url_for('main.index')  # Redirection par défaut
            
            return redirect(next_page)
        else:
            flash('Échec de connexion. Vérifiez votre email et votre mot de passe.', 'danger')
    
    return render_template('auth/connexion.html', form=form, title='Connexion')

@auth.route('/deconnexion')
def deconnexion():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))