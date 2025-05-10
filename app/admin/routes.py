from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.admin.forms import AjouterEnchereForm, AjouterPackForm, AjouterProduitForm, AttribuerJetonsForm, EnvoyerNotificationForm, ModifierEnchereForm, ModifierPackForm, ModifierProduitForm
from app.models import Enchere, Mise, Notification, PackJetons, Produit, Utilisateur, Transaction
from flask_wtf import FlaskForm

from app.services.enchere_service import verifier_statut_enchere

admin = Blueprint('admin', __name__)

def check_admin_role():
    """Vérifie si l'utilisateur est admin"""
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return False
    return True

@admin.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord administrateur"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    stats = {
        'encheres': Enchere.query.options(
            db.joinedload(Enchere.produit)  # Eager load produit relationship
        ).filter(
            Enchere.date_fin > db.func.now()
        ).all(),
        
        'produits_populaires': Produit.query.order_by(
            Produit.id_produit.desc()
        ).limit(6).all(),
        
        'nombre_produits': Produit.query.count(),
        'nombre_encheres_actives': Enchere.query.filter_by(statut='ouverte').count(),
        'nombre_packs': PackJetons.query.count()
    }

    return render_template('index.html', **stats)  # Changed template path

@admin.route('/transactions')
@login_required
def transactions():
    """Gestion des transactions"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    transactions = Transaction.query.all()
    return render_template(
        'admin/transactions.html',
        title='Gestion des transactions',
        transactions=transactions
    )

@admin.route('/gestion_encheres', methods=['GET', 'POST'])
@login_required
def gestion_encheres():
    """Gestion des enchères"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    encheres_actives = Enchere.query.filter_by(statut='ouverte').all()
    for enchere in encheres_actives:
        if verifier_statut_enchere(enchere):
            enchere.determine_gagnant()

    encheres = Enchere.query.options(
        db.joinedload(Enchere.produit)
    ).order_by(Enchere.date_fin.desc()).all()
    
    form = AjouterEnchereForm()
    delete_form = FlaskForm()
    # Configuration des choix de produits pour le formulaire
    form.produit.choices = [
        (p.id_produit, p.nom_produit) 
        for p in Produit.query.all()
    ]
    
    if form.validate_on_submit():
        nouvelle_enchere = Enchere(
            produit_id=form.produit.data,
            date_debut=form.date_debut.data,
            date_fin=form.date_fin.data,
            jetons_requis=form.jetons_requis.data,
            prix_depart=form.prix_depart.data
        )
        db.session.add(nouvelle_enchere)
        db.session.commit()
        flash("Nouvelle enchère ajoutée avec succès.", "success")
        return redirect(url_for('admin.gestion_encheres'))

    return render_template(
        'admin/gestion_encheres.html',
        encheres=encheres,
        form=form,
        delete_form=delete_form
    )

@admin.route('/modifier_enchere/<int:enchere_id>', methods=['GET', 'POST'])
@login_required
def modifier_enchere(enchere_id):
    """Modification d'une enchère existante"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    enchere = Enchere.query.get_or_404(enchere_id)
    form = ModifierEnchereForm(obj=enchere)
    
    # Set initial choices for the product select field
    form.produit.choices = [
        (p.id_produit, p.nom_produit) 
        for p in Produit.query.all()
    ]

    if form.validate_on_submit():
        # Map form fields to model attributes
        field_mapping = {
            'produit': 'produit_id',  # Fix the field name mismatch
            'date_fin': 'date_fin',
            'jetons_requis': 'jetons_requis',
            'date_debut': 'date_debut',
            'prix_depart': 'prix_depart'
        }
        
        for form_field, model_field in field_mapping.items():
            setattr(enchere, model_field, getattr(form, form_field).data)
        
        db.session.commit()
        flash("Enchère modifiée avec succès.", "success")
        return redirect(url_for('admin.gestion_encheres'))

    return render_template(
        'admin/modifier_enchere.html',
        form=form,
        enchere=enchere,
        title=f'Modifier l\'enchère {enchere_id}'
    )

@admin.route('/supprimer_enchere/<int:enchere_id>', methods=['POST'])
@login_required
def supprimer_enchere(enchere_id):
    """Suppression d'une enchère avec protection CSRF"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    # Vérifier le token CSRF
    form = FlaskForm()
    if not form.validate():
        flash("Une erreur de sécurité s'est produite. Veuillez réessayer.", "danger")
        return redirect(url_for('admin.gestion_encheres'))
        
    try:
        enchere = Enchere.query.get_or_404(enchere_id)
        
        # Vérifier si l'enchère a des mises associées
        if enchere.mises:
            flash("Impossible de supprimer une enchère qui a déjà des mises.", "danger")
            return redirect(url_for('admin.gestion_encheres'))
            
        db.session.delete(enchere)
        db.session.commit()
        flash("Enchère supprimée avec succès.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "danger")
        
    return redirect(url_for('admin.gestion_encheres'))

@admin.route('/gestion_packs', methods=['GET', 'POST'])
@login_required
def gestion_packs():
    """Gestion des packs de jetons"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    packs = PackJetons.query.order_by(PackJetons.id_pack.desc()).all()
    form = AjouterPackForm()

    if form.validate_on_submit():
        nouveau_pack = PackJetons(
            nom_pack=form.nom_pack.data,
            nombre_jetons=form.nombre_jetons.data,
            prix_pack=form.prix_pack.data
        )
        db.session.add(nouveau_pack)
        db.session.commit()
        flash("Nouveau pack ajouté avec succès.", "success")
        return redirect(url_for('admin.gestion_packs'))

    return render_template(
        'admin/gestion_packs.html',
        title='Gestion des packs de jetons',
        packs=packs,
        form=form
    )

@admin.route('/modifier_pack/<int:pack_id>', methods=['GET', 'POST'])
@login_required
def modifier_pack(pack_id):
    """Modification d'un pack de jetons"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    pack = PackJetons.query.get_or_404(pack_id)
    form = ModifierPackForm(obj=pack)

    if form.validate_on_submit():
        for field in ['nom_pack', 'nombre_jetons', 'prix_pack']:
            setattr(pack, field, getattr(form, field).data)
        db.session.commit()
        flash("Pack modifié avec succès.", "success")
        return redirect(url_for('admin.gestion_packs'))

    return render_template(
        'admin/modifier_pack.html',
        form=form,
        pack=pack
    )

@admin.route('/supprimer_pack/<int:pack_id>', methods=['POST'])
@login_required
def supprimer_pack(pack_id):
    """Suppression d'un pack de jetons"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    pack = PackJetons.query.get_or_404(pack_id)
    db.session.delete(pack)
    db.session.commit()
    flash("Pack supprimé avec succès.", "success")
    return redirect(url_for('admin.gestion_packs'))

@admin.route('/gestion_produits', methods=['GET', 'POST'])
@login_required
def gestion_produits():
    """Gestion des produits"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    produits = Produit.query.order_by(Produit.id_produit.desc()).all()
    form = AjouterProduitForm()

    if form.validate_on_submit():
        nouveau_produit = Produit(
            nom_produit=form.nom_produit.data,
            description=form.description.data,
            prix_produit=form.prix_produit.data,
            categorie=form.categorie.data,
            photo_url=form.photo_url.data
        )
        db.session.add(nouveau_produit)
        db.session.commit()
        flash("Produit ajouté avec succès.", "success")
        return redirect(url_for('admin.gestion_produits'))

    return render_template(
        'admin/gestion_produits.html',
        produits=produits,
        form=form,
        title='Gestion des produits'
    )


@admin.route('/modifier_produit/<int:produit_id>', methods=['GET', 'POST'])
@login_required
def modifier_produit(produit_id):
    """Modification d'un produit existant"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    produit = Produit.query.get_or_404(produit_id)
    form = ModifierProduitForm(obj=produit)

    if form.validate_on_submit():
        for field in ['nom_produit', 'description', 'prix_produit', 
                     'categorie', 'photo_url']:
            setattr(produit, field, getattr(form, field).data)
        db.session.commit()
        flash("Produit modifié avec succès.", "success")
        return redirect(url_for('admin.gestion_produits'))

    return render_template(
        'admin/modifier_produit.html',
        form=form,
        produit=produit,
        title=f'Modifier {produit.nom_produit}'
    )

@admin.route('/supprimer_produit/<int:produit_id>', methods=['POST'])
@login_required
def supprimer_produit(produit_id):
    """Suppression d'un produit"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    produit = Produit.query.get_or_404(produit_id)
    db.session.delete(produit)
    db.session.commit()
    flash("Produit supprimé avec succès.", "success")
    return redirect(url_for('admin.gestion_produits'))

from flask_wtf import FlaskForm  # Add this import at the top

@admin.route('/gestion-utilisateurs')
@login_required
def gestion_utilisateurs():
    """Gestion des utilisateurs"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    utilisateurs = Utilisateur.query.all()
    form = FlaskForm()  # Create a basic form for CSRF protection
    
    return render_template(
        'admin/gestion_utilisateurs.html',
        utilisateurs=utilisateurs,
        form=form,  # Pass the form to the template
        title='Gestion des utilisateurs'
    )

@admin.route('/supprimer_utilisateur/<int:utilisateur_id>', methods=['POST'])
@login_required
def supprimer_utilisateur(utilisateur_id):
    """Suppression d'un utilisateur"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    db.session.delete(utilisateur)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for('admin.gestion_utilisateurs'))

@admin.route('/historique/<int:utilisateur_id>')
@login_required
def historique_utilisateur(utilisateur_id):
    """Affichage de l'historique des mises d'un utilisateur"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    mises = Mise.query.filter_by(
        utilisateur_id=utilisateur.id_utilisateur
    ).order_by(Mise.date_mise.desc()).all()
    
    return render_template(
        'admin/historique_utilisateur.html',
        utilisateur=utilisateur,
        mises=mises,
        title=f'Historique de {utilisateur.prenom}'
    )

@admin.route('/attribuer_jetons/<int:utilisateur_id>', methods=['GET', 'POST'])
@login_required
def attribuer_jetons(utilisateur_id):
    """Attribution de jetons à un utilisateur"""
    if not check_admin_role():
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    form = AttribuerJetonsForm()
    
    if form.validate_on_submit():
        nombre_jetons = form.nombre_jetons.data
        utilisateur.solde_jetons += nombre_jetons
        db.session.commit()
        flash(f"{nombre_jetons} jetons ont été attribués à {utilisateur.prenom}.", "success")
        return redirect(url_for('admin.gestion_utilisateurs'))
    
    return render_template(
        'admin/attribuer_jetons.html',
        form=form,
        utilisateur=utilisateur,
        title=f'Attribuer des jetons à {utilisateur.prenom}'
    )

@admin.route('/envoyer_notification', methods=['GET', 'POST'])
@login_required
def envoyer_notification():
    """Envoi de notifications aux utilisateurs"""
    if not check_admin_role():
        return redirect(url_for('main.index'))

    form = EnvoyerNotificationForm()
    form.utilisateurs.choices = [
        (u.id_utilisateur, u.prenom) 
        for u in Utilisateur.query.all()
    ]

    if form.validate_on_submit():
        utilisateur_ids = form.utilisateurs.data
        message = form.message.data

        if not utilisateur_ids:
            flash("Veuillez sélectionner au moins un destinataire.", "danger")
            return redirect(url_for('admin.envoyer_notification'))

        type_notification = 'groupe' if len(utilisateur_ids) > 1 else 'unique'
        
        notifications = [
            Notification(
                utilisateur_id=int(uid),
                message=message,
                type_notification=type_notification
            )
            for uid in utilisateur_ids
        ]
        
        db.session.bulk_save_objects(notifications)
        db.session.commit()
        
        flash("Message(s) envoyé(s) avec succès.", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template(
        'admin/envoyer_notification.html',
        form=form,
        title='Envoyer une notification'
    )