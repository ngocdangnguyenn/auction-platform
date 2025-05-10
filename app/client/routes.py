from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.client.forms import (
    AcheterJetonsForm, 
    MarquerLueForm, 
    MonCompteForm, 
    PlacerEnchereForm,
    ModifierMotDePasseForm
)
from app.models import Enchere, Mise, Notification, PackJetons, Produit

client = Blueprint('client', __name__)

def check_client_role():
    """Vérifie si l'utilisateur a le rôle client"""
    if current_user.role != 'client':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'danger')
        return False
    return True

def get_unread_notifications_count():
    """Retourne le nombre de notifications non lues"""
    return Notification.query.filter_by(
        utilisateur_id=current_user.id_utilisateur, 
        lue=False
    ).count()

@client.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord du client"""
    if not check_client_role():
        return redirect(url_for('main.index'))
    
    # Eager load the produit relationship for all queries
    encheres_en_cours = Enchere.query.options(
        db.joinedload(Enchere.produit)
    ).filter(
        Enchere.date_fin > db.func.now()
    ).all()

    encheres_gagnees = Enchere.query.options(
        db.joinedload(Enchere.produit)
    ).filter_by(
        gagnant_id=current_user.id_utilisateur
    ).all()

    encheres = Enchere.query.options(
        db.joinedload(Enchere.produit)
    ).filter(
        Enchere.date_fin > db.func.now()
    ).all()

    produits_populaires = Produit.query.order_by(
        Produit.id_produit.desc()
    ).limit(6).all()

    return render_template(
        'index.html',
        title='Tableau de bord',
        encheres_en_cours=encheres_en_cours,
        encheres_gagnees=encheres_gagnees,
        encheres=encheres,
        produits_populaires=produits_populaires,
        notifications_count=get_unread_notifications_count()
    )

@client.route('/historique')
@login_required
def historique():
    """Historique des enchères de l'utilisateur"""
    encheres_gagnees = Enchere.query.filter_by(
        gagnant_id=current_user.id_utilisateur
    ).all()

    encheres_perdues = Enchere.query.join(Mise).filter(
        Mise.utilisateur_id == current_user.id_utilisateur,
        Enchere.gagnant_id != current_user.id_utilisateur
    ).all()

    return render_template(
        'client/historique.html',
        encheres_gagnees=encheres_gagnees,
        encheres_perdues=encheres_perdues
    )

@client.route('/mon_compte', methods=['GET', 'POST'])
@login_required
def mon_compte():
    """Gestion du compte utilisateur"""
    if not check_client_role():
        return redirect(url_for('main.index'))
    
    form = MonCompteForm()
    if form.validate_on_submit():
        for field in ['nom', 'prenom', 'email', 'adresse', 
                     'code_postal', 'ville', 'pays', 'telephone']:
            setattr(current_user, field, getattr(form, field).data)
        
        db.session.commit()
        flash('Vos informations ont été mises à jour avec succès.', 'success')
        return redirect(url_for('client.mon_compte'))

    return render_template(
        'client/mon_compte.html', 
        utilisateur=current_user,
        notifications_count=get_unread_notifications_count(),
        form=form
    )

@client.route('/mes_encheres')
@login_required
def mes_encheres():
    """Récupère les enchères et les mises associées pour l'utilisateur connecté"""
    if not check_client_role():
        return redirect(url_for('main.index'))

    # Query encheres with their associated mises
    results = db.session.query(Enchere, Mise).options(
        db.joinedload(Enchere.produit)
    ).join(
        Mise, 
        Mise.enchere_id == Enchere.id_enchere
    ).filter(
        Mise.utilisateur_id == current_user.id_utilisateur
    ).order_by(Enchere.date_fin.desc()).all()
    
    current_time = datetime.utcnow()
    
    return render_template(
        'client/mes_encheres.html',
        encheres=results,  # This will now be a list of (Enchere, Mise) tuples
        current_time=current_time,
        title='Mes enchères'
    )

@client.route('/acheter_jetons', methods=['GET', 'POST'])
@login_required
def acheter_jetons():
    form = AcheterJetonsForm()
    # Ajouter les choix pour le champ pack_jetons
    form.pack_jetons.choices = [(pack.id_pack, f"{pack.nombre_jetons} jetons - {pack.prix_pack} €") for pack in PackJetons.query.all()]
    if form.validate_on_submit():
        pack = PackJetons.query.get(form.pack_jetons.data)
        if pack:
            current_user.solde_jetons += pack.nombre_jetons
            db.session.commit()
            flash(f"Vous avez acheté {pack.nombre_jetons} jetons avec succès.", 'success')
            return redirect(url_for('client.acheter_jetons'))
    return render_template('client/acheter_jetons.html', form=form)

@client.route('/placer_enchere/<int:enchere_id>', methods=['POST'])
@login_required
def placer_enchere(enchere_id):
    enchere = Enchere.query.get_or_404(enchere_id)
    form = PlacerEnchereForm(enchere_id=enchere_id)

    if form.validate_on_submit():
        montant = form.montant.data

        # Vérifier que le montant est supérieur ou égal au prix de départ
        if montant <= enchere.prix_depart:
            flash(f"Le montant doit être supérieur au prix de départ ({enchere.prix_depart} €).", "danger")
            return redirect(url_for('main.detail_enchere', enchere_id=enchere.id_enchere))

        # Vérifier que l'utilisateur a suffisamment de jetons
        if current_user.solde_jetons < enchere.jetons_requis:
            flash("Vous n'avez pas assez de jetons pour placer cette enchère.", "danger")
            return redirect(url_for('main.detail_enchere', enchere_id=enchere.id_enchere))

        # Déduire les jetons requis
        current_user.solde_jetons -= enchere.jetons_requis

        # Ajouter une mise (SUPPRESSION de la mise à jour du gagnant_id)
        mise = Mise(
            enchere_id=enchere.id_enchere,
            utilisateur_id=current_user.id_utilisateur,
            prix_propose=montant,
            jetons_utilises=enchere.jetons_requis
        )
        db.session.add(mise)
        db.session.commit()

        flash("Votre enchère a été placée avec succès.", "success")
        return redirect(url_for('main.detail_enchere', enchere_id=enchere.id_enchere))

    flash("Erreur lors de la soumission de l'enchère.", "danger")
    return redirect(url_for('main.detail_enchere', enchere_id=enchere.id_enchere))

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.client.forms import ModifierMotDePasseForm

@client.route('/modifier_mot_de_passe', methods=['GET', 'POST'])
@login_required
def modifier_mot_de_passe():
    form = ModifierMotDePasseForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.mot_de_passe_actuel.data):
            flash("Le mot de passe actuel est incorrect.", "danger")
        else:
            current_user.set_password(form.nouveau_mot_de_passe.data)
            db.session.commit()
            flash("Votre mot de passe a été mis à jour avec succès.", "success")
            return redirect(url_for('client.mon_compte'))
    return render_template('client/modifier_mot_de_passe.html', form=form)

@client.route('/mes_notifications', methods=['GET'])
@login_required
def mes_notifications():
    # Récupère les notifications
    from app.models import Notification
    notifications = Notification.query.filter_by(utilisateur_id=current_user.id_utilisateur).order_by(Notification.date_creation.desc()).all()
    form = MarquerLueForm()
    return render_template('client/mes_notifications.html', notifications=notifications, form=form)

@client.route('/marquer_lue/<int:notification_id>', methods=['POST'])
@login_required
def marquer_lue(notification_id):
    form = MarquerLueForm()
    if form.validate_on_submit():  # Valide le CSRF ici
        notification = Notification.query.get_or_404(notification_id)
        if notification.utilisateur_id != current_user.id_utilisateur:
            flash("Vous ne pouvez pas accéder à cette notification.", "danger")
            return redirect(url_for('client.mes_notifications'))

        notification.lue = True
        db.session.commit()
        flash("Notification marquée comme lue.", "success")
        return redirect(url_for('client.mes_notifications'))
    flash("Action non autorisée.", "danger")
    return redirect(url_for('client.mes_notifications'))

