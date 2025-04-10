from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.admin.forms import AjouterEnchereForm, AttribuerJetonsForm, EnvoyerNotificationForm, ModifierEnchereForm
from app.models import Enchere, Mise, Notification, PackJetons, Produit

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    encheres = Enchere.query.filter(Enchere.date_fin > db.func.now()).all()
    produits_populaires = Produit.query.order_by(Produit.id_produit.desc()).limit(6).all()
    nombre_produits = Produit.query.count()
    nombre_encheres_actives = Enchere.query.filter_by(statut='ouverte').count()
    nombre_packs = PackJetons.query.count()

    return render_template(
        'index.html',  # Utilise le même template que pour le client
        encheres=encheres,
        produits_populaires=produits_populaires,
        nombre_produits=nombre_produits,
        nombre_encheres_actives=nombre_encheres_actives,
        nombre_packs=nombre_packs
    )

@admin.route('/utilisateurs')
@login_required
def utilisateurs():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'danger')
        return redirect(url_for('main.index'))
    
    # Exemple : récupérer tous les utilisateurs
    from app.models import Utilisateur
    utilisateurs = Utilisateur.query.all()
    return render_template('admin/utilisateurs.html', title='Gestion des utilisateurs', utilisateurs=utilisateurs)

@admin.route('/transactions')
@login_required
def transactions():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'danger')
        return redirect(url_for('main.index'))
    
    # Exemple : récupérer toutes les transactions
    from app.models import Transaction
    transactions = Transaction.query.all()
    return render_template('admin/transactions.html', title='Gestion des transactions', transactions=transactions)

@admin.route('/gestion_encheres', methods=['GET', 'POST'])
@login_required
def gestion_encheres():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))

    # Récupérer toutes les enchères
    encheres = Enchere.query.order_by(Enchere.date_fin.desc()).all()

    # Formulaire pour ajouter une nouvelle enchère
    form = AjouterEnchereForm()
    form.produit.choices = [(produit.id_produit, produit.nom_produit) for produit in Produit.query.all()]

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

    return render_template('admin/gestion_encheres.html', encheres=encheres, form=form)

@admin.route('/modifier_enchere/<int:enchere_id>', methods=['GET', 'POST'])
@login_required
def modifier_enchere(enchere_id):
    enchere = Enchere.query.get_or_404(enchere_id)
    form = ModifierEnchereForm(obj=enchere)
    form.produit.choices = [(produit.id_produit, produit.nom_produit) for produit in Produit.query.all()]

    if form.validate_on_submit():
        enchere.produit_id = form.produit.data
        enchere.date_fin = form.date_fin.data
        enchere.jetons_requis = form.jetons_requis.data
        enchere.date_debut = form.date_debut.data
        enchere.prix_depart = form.prix_depart.data
        db.session.commit()
        flash("Enchère modifiée avec succès.", "success")
        return redirect(url_for('admin.gestion_encheres'))

    return render_template('admin/modifier_enchere.html', form=form, enchere=enchere)

@admin.route('/supprimer_enchere/<int:enchere_id>', methods=['POST'])
@login_required
def supprimer_enchere(enchere_id):
    enchere = Enchere.query.get_or_404(enchere_id)
    db.session.delete(enchere)
    db.session.commit()
    flash("Enchère supprimée avec succès.", "success")
    return redirect(url_for('admin.gestion_encheres'))

@admin.route('/gestion_packs', methods=['GET', 'POST'])
@login_required
def gestion_packs():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'danger')
        return redirect(url_for('main.index'))
    
    from app.models import PackJetons
    from app.admin.forms import AjouterPackForm

    # Récupérer tous les packs
    packs = PackJetons.query.order_by(PackJetons.id_pack.desc()).all()

    # Formulaire pour ajouter un nouveau pack
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

    return render_template('admin/gestion_packs.html', title='Gestion des packs de jetons', packs=packs, form=form)

@admin.route('/modifier_pack/<int:pack_id>', methods=['GET', 'POST'])
@login_required
def modifier_pack(pack_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    from app.models import PackJetons
    from app.admin.forms import ModifierPackForm

    pack = PackJetons.query.get_or_404(pack_id)
    form = ModifierPackForm(obj=pack)

    if form.validate_on_submit():
        pack.nom_pack = form.nom_pack.data
        pack.nombre_jetons = form.nombre_jetons.data
        pack.prix_pack = form.prix_pack.data
        db.session.commit()
        flash("Pack modifié avec succès.", "success")
        return redirect(url_for('admin.gestion_packs'))

    return render_template('admin/modifier_pack.html', form=form, pack=pack)

@admin.route('/supprimer_pack/<int:pack_id>', methods=['POST'])
@login_required
def supprimer_pack(pack_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    from app.models import PackJetons

    pack = PackJetons.query.get_or_404(pack_id)
    db.session.delete(pack)
    db.session.commit()
    flash("Pack supprimé avec succès.", "success")
    return redirect(url_for('admin.gestion_packs'))

@admin.route('/gestion_produits', methods=['GET', 'POST'])
@login_required
def gestion_produits():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", 'danger')
        return redirect(url_for('main.index'))
    
    from app.models import Produit
    from app.admin.forms import AjouterProduitForm

    produits = Produit.query.order_by(Produit.id_produit.desc()).all()
    form = AjouterProduitForm()

    if form.validate_on_submit():
        nouveau_produit = Produit(
            nom_produit=form.nom_produit.data,
            description=form.description.data,
            prix_produit=form.prix_produit.data,
            categorie=form.categorie.data,  # Récupération de la catégorie
            photo_url=form.photo_url.data
        )
        db.session.add(nouveau_produit)
        db.session.commit()
        flash("Produit ajouté avec succès.", "success")
        return redirect(url_for('admin.gestion_produits'))

    return render_template('admin/gestion_produits.html', produits=produits, form=form)


@admin.route('/modifier_produit/<int:produit_id>', methods=['GET', 'POST'])
@login_required
def modifier_produit(produit_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    from app.models import Produit
    from app.admin.forms import ModifierProduitForm

    produit = Produit.query.get_or_404(produit_id)
    form = ModifierProduitForm(obj=produit)

    if form.validate_on_submit():
        produit.nom_produit = form.nom_produit.data
        produit.description = form.description.data
        produit.prix_produit = form.prix_produit.data
        produit.categorie = form.categorie.data
        produit.photo_url = form.photo_url.data
        db.session.commit()
        flash("Produit modifié avec succès.", "success")
        return redirect(url_for('admin.gestion_produits'))

    return render_template('admin/modifier_produit.html', form=form, produit=produit)

@admin.route('/supprimer_produit/<int:produit_id>', methods=['POST'])
@login_required
def supprimer_produit(produit_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    from app.models import Produit

    produit = Produit.query.get_or_404(produit_id)
    db.session.delete(produit)
    db.session.commit()
    flash("Produit supprimé avec succès.", "success")
    return redirect(url_for('admin.gestion_produits'))

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Utilisateur, Produit, Enchere, PackJetons


@admin.route('/gestion-utilisateurs')
@login_required
def gestion_utilisateurs():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    utilisateurs = Utilisateur.query.all()
    return render_template('admin/gestion_utilisateurs.html', utilisateurs=utilisateurs)

@admin.route('/modifier-utilisateur/<int:utilisateur_id>', methods=['GET', 'POST'])
@login_required
def modifier_utilisateur(utilisateur_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    if request.method == 'POST':
        utilisateur.nom = request.form['nom']
        utilisateur.email = request.form['email']
        utilisateur.role = request.form['role']
        db.session.commit()
        flash("Utilisateur modifié avec succès.", "success")
        return redirect(url_for('admin.gestion_utilisateurs'))
    
    return render_template('admin/modifier_utilisateur.html', utilisateur=utilisateur)

@admin.route('/supprimer-utilisateur/<int:utilisateur_id>', methods=['POST'])
@login_required
def supprimer_utilisateur(utilisateur_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    db.session.delete(utilisateur)
    db.session.commit()
    flash("Utilisateur supprimé avec succès.", "success")
    return redirect(url_for('admin.gestion_utilisateurs'))

@admin.route('/utilisateurs')
def liste_utilisateurs():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Accès refusé !", "danger")
        return redirect(url_for('main.index'))
    
    utilisateurs = Utilisateur.query.all()
    return render_template('utilisateurs.html', utilisateurs=utilisateurs)

@admin.route('/suspendre_utilisateur/<int:utilisateur_id>')
@login_required
def suspendre_utilisateur(utilisateur_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette action.", "danger")
        return redirect(url_for('main.index'))

    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    utilisateur.est_suspendu = not utilisateur.est_suspendu  # Change l'état
    db.session.commit()
    
    statut = "suspendu" if utilisateur.est_suspendu else "réactivé"
    flash(f"L'utilisateur {utilisateur.prenom} a été {statut} avec succès.", "success")
    return redirect(url_for('admin.utilisateurs'))

@admin.route('/historique/<int:utilisateur_id>')
def historique_utilisateur(utilisateur_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Accès refusé !", "danger")
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    mises = Mise.query.filter_by(utilisateur_id=utilisateur.id_utilisateur).all()
    return render_template('admin/historique_utilisateur.html', utilisateur=utilisateur, mises=mises)

@admin.route('/attribuer_jetons/<int:utilisateur_id>', methods=['GET', 'POST'])
@login_required
def attribuer_jetons(utilisateur_id):
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette action.", "danger")
        return redirect(url_for('main.index'))
    
    utilisateur = Utilisateur.query.get_or_404(utilisateur_id)
    form = AttribuerJetonsForm()
    
    if form.validate_on_submit():
        nombre_jetons = form.nombre_jetons.data
        utilisateur.solde_jetons += nombre_jetons
        db.session.commit()
        flash(f"{nombre_jetons} jetons ont été attribués à {utilisateur.prenom}.", "success")
        return redirect(url_for('admin.utilisateurs'))
    
    return render_template('admin/attribuer_jetons.html', form=form, utilisateur=utilisateur)

@admin.route('/envoyer_notification', methods=['GET', 'POST'])
@login_required
def envoyer_notification():
    if current_user.role != 'admin':
        flash("Vous n'avez pas l'autorisation d'accéder à cette page.", "danger")
        return redirect(url_for('main.index'))

    from app.models import Notification, Utilisateur
    from app.admin.forms import EnvoyerNotificationForm

    form = EnvoyerNotificationForm()
    form.utilisateurs.choices = [(u.id_utilisateur, u.prenom) for u in Utilisateur.query.all()]

    if request.method == 'POST':  # Traite les données soumises
        message = request.form.get('message')
        utilisateur_ids = request.form.getlist('utilisateurs')  # Récupère les utilisateurs sélectionnés

        if utilisateur_ids:
            for utilisateur_id in utilisateur_ids:
                nouvelle_notification = Notification(
                    utilisateur_id=int(utilisateur_id),  # Convertit l'ID en entier
                    message=message,
                    type_notification='groupe' if len(utilisateur_ids) > 1 else 'unique'
                )
                db.session.add(nouvelle_notification)

            db.session.commit()
            flash("Message(s) envoyé(s) avec succès.", "success")
        else:
            flash("Veuillez sélectionner au moins un destinataire.", "danger")

        return redirect(url_for('admin.dashboard'))

    return render_template('admin/envoyer_notification.html', form=form)



