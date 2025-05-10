from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Utilisateur
from app.auth.forms import InscriptionForm, ConnexionForm

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """Gestion de l'inscription des utilisateurs"""
    # Rediriger si déjà connecté
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = InscriptionForm()
    if form.validate_on_submit():
        try:
            nouvel_utilisateur = Utilisateur(
                nom=form.nom.data,
                prenom=form.prenom.data,
                email=form.email.data,
                mot_de_passe=generate_password_hash(form.mot_de_passe.data),
                adresse=form.adresse.data,
                code_postal=form.code_postal.data,
                pays=form.pays.data,
                ville=form.ville.data,
                telephone=form.telephone.data
            )
            
            db.session.add(nouvel_utilisateur)
            db.session.commit()
            
            flash("Votre inscription a été effectuée avec succès !", "success")
            return redirect(url_for('auth.connexion'))
            
        except Exception as e:
            db.session.rollback()
            flash("Une erreur s'est produite lors de l'inscription.", "danger")
            
    return render_template('auth/inscription.html', 
                         form=form,
                         title='Inscription')

@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    """Gestion de la connexion des utilisateurs"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = ConnexionForm()
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(email=form.email.data).first()
        
        if utilisateur and check_password_hash(utilisateur.mot_de_passe, form.mot_de_passe.data):
            login_user(utilisateur, remember=form.se_souvenir.data)
            next_page = request.args.get('next')
            
            # Redirection basée sur le rôle
            if not next_page or not next_page.startswith('/'):
                next_page = url_for(f'{utilisateur.role}.dashboard' 
                                  if utilisateur.role in ['admin', 'client'] 
                                  else 'main.index')
            
            return redirect(next_page)
            
        flash('Échec de connexion. Vérifiez votre email et votre mot de passe.', 'danger')
    
    return render_template('auth/connexion.html', 
                         form=form,
                         title='Connexion')

@auth.route('/deconnexion')
def deconnexion():
    """Déconnexion de l'utilisateur"""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))